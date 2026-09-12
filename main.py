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

    supported_suffixes = ".mp4", ".mkv", ".mov"
    if video.suffix not in supported_suffixes:
        print(
            f"Video file '{video}' is not supported, must be one of {supported_suffixes}",
            file=sys.stderr,
        )
        sys.exit(1)

    srt_path = video.with_suffix(".srt")
    output_path = video.with_stem(video.stem + "_sub")

    overall_success = True
    segments = None

    try:
        transcription_data = transcribe_video(video_path)

        if not transcription_data["success"]:
            print("\n⚠️ PROCESSING FAILED:", video_path)
            print(f"   -> Reason: {transcription_data['error_message']}")
            overall_success = False
            return

        segments = transcription_data["segments"]

        create_srt(srt_path, segments)

        burn_subtitles(video_path, srt_path, output_path)

    except ConnectionError as e:
        print(
            f"\n❌ CRITICAL FAILURE (API): Network connection failed during transcription. {e}",
            file=sys.stderr,
        )

    except PermissionError as e:
        print(
            f"\n🛑 CRITICAL SYSTEM FAILURE (Permissions): Check file system permissions. {e}",
            file=sys.stderr,
        )

    except OSError as e:
        print(
            f"\n🚨 CRITICAL FILE FAILURE: Input/Output operation failed. {e}",
            file=sys.stderr,
        )

    except subprocess.CalledProcessError as e:
        print(
            f"\n❌ CRITICAL PROCESS FAILURE (Subprocess): The external program failed with code {e.returncode}.",
            file=sys.stderr,
        )
        overall_success = False

    except Exception as e:  # noqa: BLE001
        print("\n🚨 UNPREDICTABLE SYSTEM CRASH IN PIPELINE EXECUTION.", file=sys.stderr)
        print(f"   -> Type: {type(e).__name__}", file=sys.stderr)
        print(f"   -> Message: {e}", file=sys.stderr)
        overall_success = False

    finally:
        if srt_path.exists():
            print("\n[Cleanup] Removing temporary SRT file.")
            Path(srt_path).unlink()

        if overall_success:
            print("\n✅ PIPELINE COMPLETED SUCCESSFULLY.")
        else:
            print("\n🛑 PIPELINE HALTED DUE TO FAILURE.", file=sys.stderr)


if __name__ == "__main__":
    main()
