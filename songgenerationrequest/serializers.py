from rest_framework import serializers
from .models import SongGenerationRequest

class SongGenerationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenerationRequest
        fields = ["id", "title", "request_status", "estimated_duration"]