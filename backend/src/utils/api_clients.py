import logging
from pathlib import Path
from typing import cast

from src.video_types import Segment
from whisper import load_model

logger = logging.getLogger(__name__)

whisper_model = load_model("base")


def transcribe_video(video_path: Path) -> dict:
    logger.info(f"--- Attempting API call for transcription on {video_path} ---")

    result = whisper_model.transcribe(str(video_path))
    segments = cast(list[Segment], result["segments"])

    return {
        "success": True,
        "segments": segments,
    }


def transcribe_video_mock_failure(reason: str) -> dict:
    logger.warning(f"Simulating API failure due to: {reason}")
    return {
        "success": False,
        "error_message": f"API service failed because of: {reason}",
    }
