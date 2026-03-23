from rest_framework import viewsets
from .models import SongGenerationRequest
from .serializers import SongGenerationRequestSerializer

class SongGenerationRequestViewSet(viewsets.ModelViewSet):
    queryset = SongGenerationRequest.objects.all()
    serializer_class = SongGenerationRequestSerializer