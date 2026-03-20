from rest_framework import serializers
from .models import Sharelink

class SharelinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharelink
        fields = ["id", "song", "url"]