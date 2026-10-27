import os
import sys
import re
import json
import argparse

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Compiler for HyperFrames Scene Timestamps")
    parser.add_argument("--scenes-dir", required=True, help="Directory containing source HTML scenes")
    parser.add_argument("--timestamps", required=True, help="Path to word_timestamps.json")
    parser.add_argument("--out-dir", required=True, help="Directory to save compiled HTML scenes")
    args = parser.parse_args()

    with open(args.timestamps, "r", encoding="utf-8") as f:
        timestamps = json.load(f)

    os.makedirs(args.out_dir, exist_ok=True)

    pattern = re.compile(r"\{\{t:([^}]+)\}\}")

    for filename in os.listdir(args.scenes_dir):
        if not filename.endswith(".html"):
            continue
        
        in_path = os.path.join(args.scenes_dir, filename)
        out_path = os.path.join(args.out_dir, filename)

        with open(in_path, "r", encoding="utf-8") as f:
            content = f.read()

        def replacer(match):
            key = match.group(1).strip().lower()
            # Try exact phrase match
            if key in timestamps:
                return str(timestamps[key])
            # Try single word
            words = key.split()
            if words and words[0] in timestamps:
                return str(timestamps[words[0]])
            print(f"⚠️ Warning: Timestamp key '{{t:{key}}}' not found in word_timestamps.json, defaulting to 0.0")
            return "0.0"

        compiled_content = pattern.sub(replacer, content)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(compiled_content)

        print(f"✅ Compiled scene: {filename} -> {out_path}")

if __name__ == "__main__":
    main()
