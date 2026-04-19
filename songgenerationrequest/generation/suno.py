from __future__ import annotations

from typing import Any, Mapping

import requests

from .base import GenerationRequest, SongGenerationStrategy

SUNO_GENERATE_URL = "https://api.sunoapi.org/api/v1/generate"
SUNO_RECORD_INFO_URL = "https://api.sunoapi.org/api/v1/generate/record-info"


def _voice_to_suno_gender(voice_type: str) -> str:
    v = voice_type.lower()
    if v == "male":
        return "m"
    if v == "female":
        return "f"
    if v == "instrumental":
        return "instru"
    return v


class SunoSongGeneratorStrategy(SongGenerationStrategy):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key or ""

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _build_body(self, request: GenerationRequest) -> dict[str, Any]:
        voice_key = _voice_to_suno_gender(request.voice_type)
        base = {
            "customMode": True,
            "model": "V5_5",
            "callBackUrl": "https://api.example.com/callback",
            "style": request.genre,
            "title": request.title,
        }
        if voice_key == "instru":
            return {
                **base,
                "instrumental": True,
                "prompt": f"A {request.mood} track for {request.occasion} event",
            }
        return {
            **base,
            "instrumental": False,
            "prompt": f"A {request.mood} song for {request.occasion} event",
            "vocalGender": voice_key,
        }

    def generate(self, request: GenerationRequest) -> Mapping[str, Any]:
        if not self._api_key:
            return {
                "code": 401,
                "msg": "SUNO_API_KEY is not set",
                "data": None,
            }
        body = self._build_body(request)
        resp = requests.post(
            SUNO_GENERATE_URL,
            json=body,
            headers=self._headers(),
            timeout=60,
        )
        try:
            return resp.json()
        except ValueError:
            return {
                "code": resp.status_code,
                "msg": resp.text or "Invalid JSON from Suno",
                "data": None,
            }

    def get_record_info(self, task_id: str) -> Mapping[str, Any]:
        if not self._api_key:
            return {
                "code": 401,
                "msg": "SUNO_API_KEY is not set",
                "data": None,
            }
        resp = requests.get(
            SUNO_RECORD_INFO_URL,
            headers=self._headers(),
            params={"taskId": task_id},
            timeout=60,
        )
        try:
            return resp.json()
        except ValueError:
            return {
                "code": resp.status_code,
                "msg": resp.text or "Invalid JSON from Suno",
                "data": None,
            }
