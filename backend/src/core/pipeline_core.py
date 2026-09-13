import logging
from pathlib import Path

from backend.src.utils.api_clients import transcribe_video
from backend.src.utils.file_system_wrappers import (
    burn_subtitles_with_ffmpeg,
    create_srt_path,
    write_srt_file,
)
from backend.src.utils.path_management import get_output_video_path

logger = logging.getLogger(__name__)


def process_video(video_path: Path) -> dict:
    logger.info(f"Starting pipeline for: {video_path}")

    transcript_result = transcribe_video(video_path)

    if not transcript_result.get("success"):
        error_msg = transcript_result.get(
            "error_message", "Unknown transcription failure"
        )
        logger.error(f"Pipeline aborted: {error_msg}")
        return {"success": False, "error": error_msg}

    segments = transcript_result["segments"]

    srt_path = create_srt_path(video_path)
    logger.info(f"Writing SRT file to {srt_path}...")

    if not write_srt_file(segments, srt_path):
        logger.error("Pipeline aborted: Failed to write SRT file.")
        return {"success": False, "error": "SRT file generation failed"}

    output_path = get_output_video_path(video_path)
    logger.info(f"Burning subtitles to {output_path}...")

    if not burn_subtitles_with_ffmpeg(video_path, srt_path, output_path):
        logger.error("Pipeline aborted: FFmpeg execution failed.")
        return {"success": False, "error": "Subtitle burning failed"}

    logger.info("✅ Pipeline completed successfully.")
    return {
        "success": True,
        "output_video": output_path,
        "srt_file": srt_path,
    }
