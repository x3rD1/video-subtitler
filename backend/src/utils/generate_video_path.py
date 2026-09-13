import mimetypes
import secrets
from pathlib import Path

from fastapi import UploadFile


def generate_video_path(temp_dir: Path, video: UploadFile):
    original_name = video.filename or "uploaded_video.mp4"

    target_file_path: Path = temp_dir / original_name

    if target_file_path.is_file() and video.content_type:
        unique_id = secrets.token_hex(4)
        extension = mimetypes.guess_extension(video.content_type)
        original_name = f"{target_file_path.stem}-{unique_id}{extension}"

    return temp_dir / original_name
