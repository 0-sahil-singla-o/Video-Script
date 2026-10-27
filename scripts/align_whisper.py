import os
import sys
import json
import difflib
import argparse

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def clean_word(w):
    return "".join(c for c in w.lower() if c.isalnum())

def main():
    parser = argparse.ArgumentParser(description="Word-level alignment using Faster-Whisper")
    parser.add_argument("--audio", required=True, help="Path to voice.wav")
    parser.add_argument("--script", required=True, help="Path to script.md")
    parser.add_argument("--out", required=True, help="Output word_timestamps.json")
    parser.add_argument("--model-size", default="base.en", help="Whisper model size (tiny.en, base.en, small.en)")
    args = parser.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("❌ faster-whisper not installed.")
        sys.exit(1)

    print(f"👂 Loading Faster-Whisper ({args.model_size}) on CPU...")
    model = WhisperModel(args.model_size, device="cpu", compute_type="int8")

    print(f"⏱️ Transcribing {args.audio} with word-level timestamps...")
    segments, info = model.transcribe(args.audio, word_timestamps=True)

    whisper_words = []
    for segment in segments:
        for word in segment.words:
            whisper_words.append({
                "word": word.word.strip(),
                "clean": clean_word(word.word),
                "start": round(word.start, 3),
                "end": round(word.end, 3)
            })

    # Read original script words for validation
    with open(args.script, "r", encoding="utf-8") as f:
        script_text = " ".join([l.strip() for l in f if l.strip() and not l.startswith("#") and not l.startswith(">")])

    script_words = [clean_word(w) for w in script_text.split() if clean_word(w)]

    # Pronunciation check: compare script words vs detected words
    detected_words = [w["clean"] for w in whisper_words]
    diff = list(difflib.ndiff(script_words, detected_words))
    mismatches = [d for d in diff if d.startswith("+ ") or d.startswith("- ")]
    if mismatches:
        print("⚠️ Pronunciation / Transcription differences detected:")
        for m in mismatches[:10]:
            print(f"   {m}")
        print("   (Note: Phonetic respellings like 'Red iss' vs 'Redis' are expected)")

    # Build word timestamp map (supports both single words and consecutive 2-3 word phrases)
    word_map = {}
    for i, w in enumerate(whisper_words):
        cleaned = w["clean"]
        if cleaned and cleaned not in word_map:
            word_map[cleaned] = w["start"]

        # 2-word phrase
        if i + 1 < len(whisper_words):
            phrase2 = f"{cleaned} {whisper_words[i+1]['clean']}"
            if phrase2 not in word_map:
                word_map[phrase2] = w["start"]

        # 3-word phrase (e.g. "called skip locked")
        if i + 2 < len(whisper_words):
            phrase3 = f"{cleaned} {whisper_words[i+1]['clean']} {whisper_words[i+2]['clean']}"
            if phrase3 not in word_map:
                word_map[phrase3] = w["start"]

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(word_map, f, indent=2)

    print(f"✅ Generated {len(word_map)} word/phrase timestamps into: {args.out}")

if __name__ == "__main__":
    main()
