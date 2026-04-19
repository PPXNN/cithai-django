from __future__ import annotations

from typing import Any, Mapping

from .base import GenerationRequest, SongGenerationStrategy

# Fixed task id so polling is deterministic without external services.
MOCK_TASK_ID = "mock-task-00000000-0000-4000-8000-000000000001"


class MockSongGeneratorStrategy(SongGenerationStrategy):
    """Offline generator: no HTTP, predictable taskId and record-info."""

    _RECORD_INFO: dict[str, Any] = {
        "code": 200,
        "msg": "success",
        "data": {
            "taskId": MOCK_TASK_ID,
            "parentMusicId": "",
            "param": "",
            "response": {
                "taskId": MOCK_TASK_ID,
                "sunoData": [
                    {
                        "id": "9dd76ea7-d70e-49af-9989-c509e091e758",
                        "audioUrl": "https://tempfile.aiquickdraw.com/r/c1873c9ba22a436eaaf7614d0deaa8c2.mp3",
                        "sourceAudioUrl": "https://cdn1.suno.ai/9dd76ea7-d70e-49af-9989-c509e091e758.mp3",
                        "streamAudioUrl": "https://musicfile.removeai.ai/OWRkNzZlYTctZDcwZS00OWFmLTk5ODktYzUwOWUwOTFlNzU4",
                        "sourceStreamAudioUrl": "https://cdn1.suno.ai/9dd76ea7-d70e-49af-9989-c509e091e758.mp3",
                        "imageUrl": "https://musicfile.removeai.ai/OWRkNzZlYTctZDcwZS00OWFmLTk5ODktYzUwOWUwOTFlNzU4.jpeg",
                        "sourceImageUrl": "https://cdn2.suno.ai/image_9dd76ea7-d70e-49af-9989-c509e091e758.jpeg",
                        "prompt": "A calm song for birthday event",
                        "modelName": "chirp-fenix",
                        "title": "test6",
                        "tags": "classical",
                        "createTime": 1776499082098,
                        "duration": 36.8,
                    },
                ],
            },
            "status": "SUCCESS",
            "type": "chirp-fenix",
            "operationType": "generate",
            "errorCode": None,
            "errorMessage": None,
            "createTime": 1776499031000,
        },
    }

    def generate(self, request: GenerationRequest) -> Mapping[str, Any]:
        _ = request
        data = self._RECORD_INFO["data"]
        return {
            "code": 200,
            "msg": "success",
            "data": {
                "taskId": data["taskId"],
                "parentMusicId": data.get("parentMusicId", ""),
                "param": data.get("param", ""),
                "response": data.get("response", {}),
            },
        }

    def get_record_info(self, task_id: str) -> Mapping[str, Any]:
        if task_id != MOCK_TASK_ID:
            return {
                "code": 404,
                "msg": "mock: unknown taskId",
                "data": None,
            }
        return self._RECORD_INFO
