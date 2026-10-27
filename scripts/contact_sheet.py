import os
import sys
import subprocess
import argparse

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_duration(video_path):
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(res.stdout.strip())
    except Exception:
        return 100.0

def main():
    parser = argparse.ArgumentParser(description="Generate 4x4 Visual QA Contact Sheet")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--out", required=True, help="Path to output contact sheet image (.png)")
    args = parser.parse_args()

    print(f"📸 Generating 4x4 Contact Sheet for {args.video}...")
    duration = get_duration(args.video)
    step = max(1.0, duration / 16.0)
    print(f"  Duration: {duration:.2f}s, sampling every {step:.2f}s across 16 frames")
    
    # Use ffmpeg fps and tile filter to sample 16 evenly spaced frames
    cmd = [
        "ffmpeg", "-y",
        "-i", args.video,
        "-vf", f"fps=1/{step:.3f},scale=270:480,tile=4x4",
        "-frames:v", "1",
        "-q:v", "2",
        args.out
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and os.path.exists(args.out):
        print(f"✅ Contact sheet generated: {args.out}")
    else:
        print(f"⚠️ Could not generate contact sheet: {res.stderr}")

if __name__ == "__main__":
    main()
