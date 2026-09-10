import subprocess
import sys
from pathlib import Path

from video import burn_subtitles, create_srt, transcribe_video


def main():
    # Check if a video path was provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <video_path>", file=sys.stderr)
        sys.exit(1)

    video_path = sys.argv[1]
    video = Path(video_path)

    if not video.exists():
        print(f"The video file '{video}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if video.suffix not in (".mp4", ".mkv", ".mov"):
        print(f"Video file '{video}' is not supported", file=sys.stderr)
        sys.exit(1)

    srt_path = video.with_suffix(".srt")
    output_path = video.with_stem(video.stem + "_sub")

    try:
        segments = transcribe_video(video_path)

        create_srt(srt_path, segments)

        burn_subtitles(video_path, srt_path, output_path)

    except subprocess.CalledProcessError as error:
        print(error.returncode)

    except Exception as error:  # noqa: BLE001
        print(error, file=sys.stderr)


if __name__ == "__main__":
    main()
