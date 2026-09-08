import whisper
from typing import Any
from pathlib import Path
from utils import format_timestamp
import subprocess

model = whisper.load_model("base")

def transcribe_video(video_path: str):
    result: dict[str, Any] = model.transcribe(video_path)
    segments: list[dict[str, Any]] = result["segments"]

    return segments

def create_srt(srt_path: Path, segments: list[dict[str, Any]]):
    
    with open(srt_path, "w", encoding="utf-8") as file:
        for i, segment in enumerate(segments):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])

            subtitle = f"{i + 1}\n{start} --> {end}\n{segment['text']}"

            file.write(subtitle + "\n\n")

def burn_subtitles(video_path, srt_path, output_path):
    subprocess.run([
    "ffmpeg",
    "-i", video_path,
    "-vf", f"subtitles={srt_path}",
    output_path])