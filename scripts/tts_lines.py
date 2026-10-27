import os
import sys
import json
import argparse
import numpy as np
import soundfile as sf

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def trim_silence(audio, threshold=0.01, pad_start=240, pad_end=1200):
    """Trims leading and trailing silence from synthesized audio."""
    non_zero = np.where(np.abs(audio) > threshold)[0]
    if len(non_zero) == 0:
        return audio
    start = max(0, non_zero[0] - pad_start)
    end = min(len(audio), non_zero[-1] + pad_end)
    return audio[start:end]

def parse_script_lines(script_path):
    """Extracts spoken lines from script.md (ignores headers and > directions)."""
    with open(script_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()
    
    spoken_lines = []
    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(">"):
            continue
        spoken_lines.append(line)
    return spoken_lines

def main():
    parser = argparse.ArgumentParser(description="Kokoro TTS Line-by-Line Synthesis")
    parser.add_argument("--script", required=True, help="Path to script.md")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    parser.add_argument("--voice", default="am_michael,am_onyx", help="Voice or blend e.g. am_michael,am_onyx")
    parser.add_argument("--speed", type=float, default=1.05, help="Speech rate")
    parser.add_argument("--gap", type=float, default=0.25, help="Pause gap between sentences in seconds")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    lines = parse_script_lines(args.script)
    if not lines:
        print("[Error] No spoken lines found in script.md")
        sys.exit(1)

    print(f"[Kokoro TTS] Synthesizing {len(lines)} lines (Voice: {args.voice}, Speed: {args.speed})...")

    # Load Kokoro ONNX
    try:
        from kokoro_onnx import Kokoro
        model_dir = os.path.join(os.path.expanduser("~"), ".cache", "kokoro")
        model_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
        voices_path = os.path.join(model_dir, "voices-v1.0.bin")

        if not os.path.exists(model_path) or not os.path.exists(voices_path):
            print(f"[Error] Kokoro model files missing in {model_dir}")
            sys.exit(1)

        kokoro = Kokoro(model_path, voices_path)
    except Exception as e:
        print(f"[Error] Failed to initialize Kokoro ONNX: {e}")
        sys.exit(1)

    # Resolve voice or blend
    voice_names = [v.strip() for v in args.voice.split(",")]
    if len(voice_names) > 1:
        styles = [kokoro.get_voice_style(v) for v in voice_names]
        active_voice = np.mean(styles, axis=0)
        print(f"  Blended {len(voice_names)} voices: {', '.join(voice_names)}")
    else:
        active_voice = voice_names[0]
        print(f"  Using voice: {active_voice}")

    SR = 24000
    all_audio_chunks = []
    meta = []
    current_time = 0.0

    for i, line in enumerate(lines):
        print(f"  [{i+1}/{len(lines)}] {line}")
        samples, _ = kokoro.create(line, voice=active_voice, speed=args.speed, lang="en-us")

        # Trim model silence
        samples = trim_silence(samples)
        duration = len(samples) / SR

        start_t = round(current_time, 3)
        end_t = round(current_time + duration, 3)

        meta.append({
            "index": i,
            "text": line,
            "start": start_t,
            "end": end_t
        })

        all_audio_chunks.append(samples)
        
        # Add custom pause gap between thoughts
        gap_samples = np.zeros(int(args.gap * SR), dtype=samples.dtype)
        all_audio_chunks.append(gap_samples)
        current_time = end_t + args.gap

    final_audio = np.concatenate(all_audio_chunks)
    out_wav = os.path.join(args.out_dir, "voice.wav")
    sf.write(out_wav, final_audio, SR)

    out_meta = os.path.join(args.out_dir, "line_timestamps.json")
    with open(out_meta, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"[Success] Generated voice track: {out_wav} (Duration: {round(current_time, 2)}s)")
    print(f"[Success] Line timestamps saved: {out_meta}")

if __name__ == "__main__":
    main()
