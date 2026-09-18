import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from src.core.pipeline_core import process_video
from src.utils.file_deletion import delete_old_files
from src.utils.generate_video_path import generate_video_path

TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)


async def periodic_cleanup_task(interval: int = 3600) -> None:
    while True:
        try:
            delete_old_files(TEMP_DIR)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Periodic cleanup encountered an error: {e}")

        await asyncio.sleep(interval)


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_task = asyncio.create_task(periodic_cleanup_task())
    yield
    cleanup_task.cancel()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.post("/api/process-video")
async def handle_process_video(
    video: Annotated[UploadFile, File(...)],
    target_language: Annotated[str, Form()] = "en",
):
    try:
        # Save the uploaded video to a temporary location
        video_path = generate_video_path(TEMP_DIR, video)

        async with aiofiles.open(video_path, "wb") as buffer:
            while chunk := await video.read(1024 * 1024):
                await buffer.write(chunk)

        result = process_video(video_path, target_language)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        output_video_path = Path(result["output_video"])

        return FileResponse(
            path=output_video_path,
            media_type=video.content_type,
            filename=output_video_path.name,
        )

    except Exception as e:  # noqa: BLE001
        logger.error(f"Error processing video: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
