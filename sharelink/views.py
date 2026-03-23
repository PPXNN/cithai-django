from rest_framework import viewsets
from .models import Sharelink
from .serializers import SharelinkSerializer

class SharelinkViewSet(viewsets.ModelViewSet):
    queryset = Sharelink.objects.all()
    serializer_class = SharelinkSerializer