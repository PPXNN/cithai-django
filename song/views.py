from rest_framework import viewsets
from .models import Song
from .serializers import SongSerializer

# Create your views here.
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer