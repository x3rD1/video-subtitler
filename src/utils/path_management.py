import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_video_path(file_input: str) -> Path | None:
    p = Path(file_input)

    if not p.exists():
        logger.error(f"File does not exist at provided path: {file_input}")
        return None

    return p


def get_srt_path(source_path: Path) -> Path:
    return source_path.with_suffix(".srt")


def get_output_video_path(source_path: Path) -> Path:
    return source_path.with_stem(source_path.stem + "_sub")
