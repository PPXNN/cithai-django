from __future__ import annotations

from django.conf import settings

from .base import SongGenerationStrategy
from .mock import MockSongGeneratorStrategy
from .suno import SunoSongGeneratorStrategy


def get_song_generation_strategy() -> SongGenerationStrategy:
    raw = getattr(settings, "GENERATOR_STRATEGY", "mock") or "mock"
    name = str(raw).strip().lower()
    if name == "suno":
        return SunoSongGeneratorStrategy(api_key=getattr(settings, "SUNO_API_KEY", "") or "")
    return MockSongGeneratorStrategy()
