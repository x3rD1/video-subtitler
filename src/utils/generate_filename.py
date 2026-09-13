import mimetypes
import uuid
from pathlib import Path

from fastapi import UploadFile


def generate_filename(video: UploadFile) -> str:
    file_extension = ".mp4"

    if video.filename and Path(video.filename).suffix:
        file_extension = Path(video.filename).suffix

    elif video.content_type:
        guessed_ext = mimetypes.guess_extension(video.content_type)

        if guessed_ext:
            file_extension = guessed_ext

    return f"{uuid.uuid4()}{file_extension}"
