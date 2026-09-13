import logging
from pathlib import Path

from src.video_types import Segment

logger = logging.getLogger(__name__)


def transcribe_video(video_path: Path) -> dict:

    logger.info(f"--- Attempting API call for transcription on {video_path} ---")

    mock_segments: list[Segment] = [
        {"start": 0.0, "end": 1.5, "text": "Hello"},
        {"start": 1.5, "end": 3.2, "text": "world,"},
        {"start": 3.2, "end": 5.0, "text": "this is the test video."},
    ]

    return {
        "success": True,
        "segments": mock_segments,
    }


def transcribe_video_mock_failure(reason: str) -> dict:
    logger.warning(f"Simulating API failure due to: {reason}")
    return {
        "success": False,
        "error_message": f"API service failed because of: {reason}",
    }
