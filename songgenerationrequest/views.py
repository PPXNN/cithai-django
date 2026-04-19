from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RequestStatus, SongGenerationRequest
from song.models import Song
from song.serializers import SongSerializer
from .serializers import SongGenerationRequestSerializer
from .generation import GenerationRequest, get_song_generation_strategy


def _http_status_for_suno_envelope(resp_json: dict) -> int:
    code = resp_json.get("code", 500)
    if code == 200:
        return status.HTTP_200_OK
    if code == 401:
        return status.HTTP_401_UNAUTHORIZED
    if code == 404:
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST


class SongGenerationRequestViewSet(APIView):
    def get(self, request, pk=None):  # Get data or search data
        if pk:
            SongGenRequest = SongGenerationRequest.objects.get(pk=pk)
            serializer = SongGenerationRequestSerializer(SongGenRequest)
        else:
            SongGenRequest = SongGenerationRequest.objects.all()
            serializer = SongGenerationRequestSerializer(SongGenRequest, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = SongGenerationRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        vd = serializer.validated_data
        gen_req = GenerationRequest(
            title=vd.get("title"),
            occasion=vd.get("occasion"),
            genre=vd.get("genre"),
            mood=vd.get("mood"),
            voice_type=str(vd.get("voice_type")).lower(),
        )

        strategy = get_song_generation_strategy()
        resp_json = dict(strategy.generate(gen_req))

        if resp_json.get("code") == 200:
            data = resp_json.get("data") or {}
            task_id = data.get("taskId")
            if task_id:
                serializer.save(taskId=task_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(resp_json, status=_http_status_for_suno_envelope(resp_json))

    def put(self, request, pk):
        SongGenRequest = SongGenerationRequest.objects.get(pk=pk)
        serializer = SongGenerationRequestSerializer(SongGenRequest, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        SongGenRequest = SongGenerationRequest.objects.get(pk=pk)
        SongGenRequest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SongGenerationRequestStatusViewSet(APIView):
    def get(self, request, taskId, userId):
        strategy = get_song_generation_strategy()
        resp_json = dict(strategy.get_record_info(taskId))

        data = resp_json.get("data")
        if not isinstance(data, dict):
            return Response(resp_json, status=_http_status_for_suno_envelope(resp_json))

        if data.get("status") == "SUCCESS":
            song_request_qs = SongGenerationRequest.objects.filter(taskId=taskId)
            if not song_request_qs.exists():
                return Response(resp_json, status=_http_status_for_suno_envelope(resp_json))

            song_request_data = song_request_qs[0]
            serializer = SongGenerationRequestSerializer(
                song_request_data,
                data={"request_status": RequestStatus.COMPLETED},
                partial=True,
            )

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            suno = (data.get("response") or {}).get("sunoData") or []
            if not suno:
                return Response(resp_json, status=_http_status_for_suno_envelope(resp_json))

            first = suno[0]
            body = {
                "title": first.get("title"),
                "description": first.get("prompt"),
                "occasion": serializer.data["occasion"],
                "genre": first.get("tags"),
                "voice_type": serializer.data["voice_type"],
                "mood": serializer.data["mood"],
                "audiofile_url": first.get("audioUrl"),
                "user": userId,
                "song_generation_request": serializer.data["id"],
            }

            song_serializer = SongSerializer(data=body)
            if song_serializer.is_valid():
                song_serializer.save()
            else:
                return Response(song_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(resp_json, status=_http_status_for_suno_envelope(resp_json))
