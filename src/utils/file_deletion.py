import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)


def delete_old_files(temp_dir):
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=1)

    for file_path in temp_dir.iterdir():
        if file_path.is_file():
            file_mtime: datetime = datetime.fromtimestamp(
                file_path.stat().st_mtime, tz=timezone.utc
            )

            if file_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    logger.info(f"Deleted old file: {file_path}")
                except Exception as e:  # noqa: BLE001
                    logger.error(f"Error deleting file {file_path}: {e}")
