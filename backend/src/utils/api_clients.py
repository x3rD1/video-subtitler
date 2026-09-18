import logging
import os
import subprocess
from pathlib import Path
from typing import Any

from deepgram import DeepgramClient, ListenV1Response
from dotenv import load_dotenv
from src.video_types import Segment

load_dotenv()

logger = logging.getLogger(__name__)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


def extract_audio(video_path: Path) -> Path:
    audio_path = video_path.with_suffix(".wav")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-vn",
            str(audio_path),
        ],
        check=True,
    )

    return audio_path


def deepgram_words_to_segments(words: list[Any]) -> list[Segment]:
    segments: list[Segment] = []
    current_words: list[str] = []
    segment_start: float | None = None
    segment_end: float | None = None
    last_word_end: float | None = None

    def flush_segment() -> None:
        nonlocal current_words, segment_start, segment_end, last_word_end

        if not current_words or segment_start is None or segment_end is None:
            current_words = []
            segment_start = None
            segment_end = None
            last_word_end = None
            return

        segments.append(
            {
                "start": segment_start,
                "end": segment_end,
                "text": " ".join(current_words).strip(),
            }
        )

        current_words = []
        segment_start = None
        segment_end = None
        last_word_end = None

    for word in words:
        text = str(word.word).strip()
        if not text:
            continue

        start = float(word.start)
        end = float(word.end)

        if segment_start is None:
            segment_start = start

        # flush before current word if there was a pause
        if last_word_end is not None and start - last_word_end > 0.6:
            flush_segment()

            # reinitialize after flush
            segment_start = start

        segment_end = end
        last_word_end = end
        current_words.append(text)

        # also flush if segment is too long or too many words
        if len(current_words) >= 10 or (segment_end - segment_start) >= 4.5:
            flush_segment()

    flush_segment()
    return segments


def transcribe_video(video_path: Path, target_language="en") -> dict:
    logger.info(f"--- Attempting Deepgram transcription for {video_path} ---")

    if not DEEPGRAM_API_KEY or not DEEPGRAM_API_KEY.strip():
        logger.error("DEEPGRAM_API_KEY is missing or empty")
        return {
            "success": False,
            "error_message": "DEEPGRAM_API_KEY is not set. Add it to your environment or Railway secret.",
        }

    try:
        audio_path = extract_audio(video_path)

        deepgram = DeepgramClient(api_key=DEEPGRAM_API_KEY)

        response = deepgram.listen.v1.media.transcribe_file(
            request=audio_path.read_bytes(),
            model="nova-3",
            smart_format=True,
            language=target_language,
            punctuate=True,
        )

        if not isinstance(response, ListenV1Response):
            request_id = getattr(response, "request_id", "unknown")
            return {
                "success": False,
                "error_message": (
                    "Deepgram accepted the transcription request but did not return final "
                    f"results yet. request_id={request_id}. "
                    "Use a callback or polling flow for async results."
                ),
            }

        words: list[dict[str, Any]] = []
        channels = getattr(response.results, "channels", []) or []
        for channel in channels:
            for alt in getattr(channel, "alternatives", []) or []:
                words.extend(getattr(alt, "words", []) or [])

        if not words:
            return {
                "success": False,
                "error_message": "Deepgram returned no transcript words",
            }

        segments = deepgram_words_to_segments(words)
        return {"success": True, "segments": segments}

    except Exception as e:
        logger.exception("Deepgram transcription failed")
        return {
            "success": False,
            "error_message": f"Deepgram transcription failed: {e!s}",
        }
