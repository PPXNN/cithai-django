from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class GenerationRequest:
    """Normalized input for song generation (domain snapshot)."""

    title: str
    occasion: str
    genre: str
    mood: str
    voice_type: str


class SongGenerationStrategy(ABC):
    """
    Strategy for creating a generation task and polling Suno-shaped record info.
    Responses follow the Suno API envelope (code, msg, data) where applicable.
    """

    @abstractmethod
    def generate(self, request: GenerationRequest) -> Mapping[str, Any]:
        """Start generation; return dict shaped like Suno POST /generate JSON."""

    @abstractmethod
    def get_record_info(self, task_id: str) -> Mapping[str, Any]:
        """Return dict shaped like Suno GET /generate/record-info JSON."""
