from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from .models import Sharelink
from .serializers import SharelinkSerializer


def _build_public_share_url(request, sharelink_id: int) -> str:
    return request.build_absolute_uri(
        reverse("sharelinks:public_sharelink", kwargs={"pk": sharelink_id})
    )


def public_sharelink_redirect(request, pk):
    sharelink = Sharelink.objects.filter(pk=pk, is_active=True).first()
    if not sharelink:
        raise Http404("Share link is not active")
    audio_url = (sharelink.song.audiofile_url or "").strip()
    if not audio_url:
        raise Http404("Song audio URL not found")
    return redirect(audio_url)


class SharelinkViewSet(APIView):
    def get(self, request, pk=None):  # Get data or search data
        if pk:
            # Get by pk
            sharelink = Sharelink.objects.get(pk=pk)
            serializer = SharelinkSerializer(sharelink)
        else:
            sharelinks = Sharelink.objects.all()  # List of object
            serializer = SharelinkSerializer(sharelinks, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = SharelinkSerializer(data=request.data)

        if serializer.is_valid():
            sharelink = serializer.save()
            # Force share URL to be app-controlled so is_active can gate access.
            sharelink.url = _build_public_share_url(request, sharelink.id)
            sharelink.save(update_fields=["url"])
            return Response(
                SharelinkSerializer(sharelink).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        sharelink = Sharelink.objects.get(pk=pk)
        serializer = SharelinkSerializer(sharelink, data=request.data)

        if serializer.is_valid():
            saved = serializer.save()
            saved.url = _build_public_share_url(request, saved.id)
            saved.save(update_fields=["url"])
            return Response(SharelinkSerializer(saved).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        sharelink = Sharelink.objects.get(pk=pk)
        sharelink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)