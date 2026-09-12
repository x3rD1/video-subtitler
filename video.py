import subprocess
import sys
from pathlib import Path
from typing import Any

import whisper

from utils import format_timestamp
from video_types import Segment, TranscriptionResult

model = whisper.load_model("base")


def transcribe_video(video_path: str, language=None) -> TranscriptionResult:
    segments: list[Segment] = []
    error_message: str | None

    try:
        if language is None:
            result: dict[str, Any] = model.transcribe(video_path)
        else:
            result: dict[str, Any] = model.transcribe(video_path, language=language)

        segments = result["segments"]

        error_message = None

    except Exception as e:  # noqa: BLE001
        print(
            f"🛑 WARNING: Failed to transcribe '{video_path}'. Error details:",
            file=sys.stderr,
        )
        print(e, file=sys.stderr)

        error_message = (
            f"Transcription failed due to an internal error: {type(e).__name__}."
        )

    finally:
        pass

    return {
        "success": error_message is None,
        "segments": segments,
        "error_message": error_message,
    }


def create_srt(srt_path: Path, segments: list[Segment]) -> None:

    with open(srt_path, "w", encoding="utf-8") as file:
        for i, segment in enumerate(segments):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])

            subtitle = f"{i + 1}\n{start} --> {end}\n{segment['text']}"

            file.write(subtitle + "\n\n")


def burn_subtitles(video_path: str, srt_path: Path, output_path: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-i", video_path, "-vf", f"subtitles={srt_path}", output_path],
        check=True,
    )
