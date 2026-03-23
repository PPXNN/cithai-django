from rest_framework import serializers
from .models import SongGenerationRequest

class SongGenerationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenerationRequest
        fields = "__all__"