from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Song
from .serializers import SongSerializer

# Create your views here.
class SongViewSet(APIView):
    def get(self, request, pk=None): # Get data or search data
        if pk:
            #Get by pk
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
        else:
            songs = Song.objects.all() # List of object
            serializer = SongSerializer(songs, many=True)

        return Response(serializer.data)
    
    def post(self, request): 
        serializer = SongSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        song = Song.objects.get(pk=pk)
        serializer = SongSerializer(song, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)