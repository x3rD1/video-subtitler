import logging
import subprocess
from pathlib import Path

from backend.src.utils.format_timestamp import format_timestamp
from backend.src.video_types import Segment

logger = logging.getLogger(__name__)


def create_srt_path(video_path: Path) -> Path:
    return video_path.with_suffix(".srt")


def write_srt_file(segments: list[Segment], srt_path: Path) -> bool:

    logger.info(f"Attempting to write SRT file to {srt_path}")

    try:
        with open(srt_path, "w", encoding="utf-8") as file:
            for i, segment in enumerate(segments):
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])

                subtitle = f"{i + 1}\n{start} --> {end}\n{segment['text']}"

                file.write(subtitle + "\n\n")

        return True

    except OSError as e:
        logger.error(f"Failed to write SRT file due to IO Error: {e}")
        return False


def burn_subtitles_with_ffmpeg(
    video_path: Path, srt_path: Path, output_path: Path
) -> bool:

    try:
        command = [
            "ffmpeg",
            "-i",
            str(video_path),
            "-vf",
            f"subtitles={srt_path!s}",
            str(output_path),
        ]

        subprocess.run(command, check=True)

        logger.info(f"Successfully simulated burning subtitles to {output_path}")
        return True

    except Exception as e:  # noqa: BLE001
        logger.error(f"FFmpeg execution failed or path error: {e}")
        return False
