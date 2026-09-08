import sys
from pathlib import Path
from video import transcribe_video, create_srt, burn_subtitles

# Check if a video path was provided
if len(sys.argv) < 2:
    print("Usage: python main.py <video_path>")
    sys.exit(1)

video_path = sys.argv[1]
video = Path(video_path)

if not video.exists():
    print(f"File not found: {video}")
    sys.exit(1)
    
srt_path = video.with_suffix(".srt")
output_path = video.with_stem(video.stem + "_sub")


segments = transcribe_video(video_path)

create_srt(srt_path, segments)

burn_subtitles(video_path, srt_path, output_path)

