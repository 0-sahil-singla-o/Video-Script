import os
import sys
import subprocess
import argparse
import json

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_cmd(cmd):
    print(f"  Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ Error executing command:\n{res.stderr}")
        sys.exit(res.returncode)

def main():
    parser = argparse.ArgumentParser(description="Sound Engineering & Mastering by Numbers (Step 6)")
    parser.add_argument("--visuals", required=True, help="Rendered visuals.mp4")
    parser.add_argument("--voice", required=True, help="voice.wav")
    parser.add_argument("--bgm", help="Path to background music")
    parser.add_argument("--sfx-dir", default="projects/shopify-tokens/assets/sfx", help="Directory containing SFX wav files")
    parser.add_argument("--out", required=True, help="Final mastered reel MP4")
    args = parser.parse_args()

    out_dir = os.path.dirname(args.out)
    temp_voice_norm = os.path.join(out_dir, "temp_voice_norm.wav")
    temp_sfx_mix = os.path.join(out_dir, "temp_sfx_mix.wav")

    # Step 1: Normalize voice narration to -16 LUFS (Broadcast standard)
    print("🎚️ Normalizing voice track to -16 LUFS...")
    cmd_norm_voice = [
        "ffmpeg", "-y",
        "-i", args.voice,
        "-af", "loudnorm=I=-16:TP=-1.0:LRA=11",
        temp_voice_norm
    ]
    run_cmd(cmd_norm_voice)

    # Step 2: Layer SFX cues if available
    sfx_whoosh = os.path.join(args.sfx_dir, "whoosh.wav")
    sfx_slam = os.path.join(args.sfx_dir, "slam.wav")
    sfx_clink = os.path.join(args.sfx_dir, "clink.wav")
    sfx_click = os.path.join(args.sfx_dir, "click.wav")

    has_sfx = all(os.path.exists(f) for f in [sfx_whoosh, sfx_slam, sfx_clink, sfx_click])
    
    if has_sfx and args.bgm and os.path.exists(args.bgm):
        cue_list = []
        line_ts_file = os.path.join(out_dir, "line_timestamps.json")
        if os.path.exists(line_ts_file):
            try:
                with open(line_ts_file, "r", encoding="utf-8") as f:
                    lines_data = json.load(f)
                for item in lines_data:
                    idx = item.get("index", 0)
                    st_ms = int(item.get("start", 0) * 1000)
                    if idx in [0, 1, 6, 8, 10, 14, 17]:
                        cue_list.append(("whoosh", 1, st_ms, 0.35))
                    elif idx in [5, 13, 19]:
                        cue_list.append(("slam", 2, st_ms, 0.45))
                    elif idx in [2, 12, 15, 21]:
                        cue_list.append(("clink", 3, st_ms, 0.35))
                    else:
                        cue_list.append(("click", 4, st_ms, 0.35))
            except Exception as e:
                print(f"Warning parsing line_timestamps: {e}")
        
        if not cue_list:
            cue_list = [
                ("whoosh", 1, 10400, 0.4),
                ("whoosh", 1, 19800, 0.4),
                ("whoosh", 1, 33600, 0.4),
                ("whoosh", 1, 46200, 0.4),
                ("whoosh", 1, 58700, 0.4),
                ("slam", 2, 21000, 0.6),
                ("clink", 3, 35000, 0.4),
                ("click", 4, 49200, 0.45),
            ]

        print(f"🎛️ Assembling multi-track Foley mix (BGM + {len(cue_list)} SFX cues + Voice)...")
        filter_parts = []
        for i, (name, in_idx, delay_ms, vol) in enumerate(cue_list):
            filter_parts.append(f"[{in_idx}:a]adelay={delay_ms}|{delay_ms},volume={vol}[c{i}];")
        
        filter_parts.append("[5:a]volume=0.10[bgm];")
        cue_tags = "".join(f"[c{i}]" for i in range(len(cue_list)))
        filter_parts.append(f"{cue_tags}[bgm]amix=inputs={len(cue_list)+1}:duration=first[bed];")
        filter_parts.append("[0:a][bed]amix=inputs=2:duration=first[master_mix];")
        filter_parts.append("[master_mix]loudnorm=I=-14:TP=-1.0:LRA=11[a_final]")
        filter_str = "".join(filter_parts)

        cmd_master = [
            "ffmpeg", "-y",
            "-i", temp_voice_norm,
            "-i", sfx_whoosh,
            "-i", sfx_slam,
            "-i", sfx_clink,
            "-i", sfx_click,
            "-i", args.bgm,
            "-filter_complex", filter_str,
            "-map", "[a_final]",
            "-c:a", "pcm_s16le",
            temp_sfx_mix
        ]
        run_cmd(cmd_master)
        audio_to_merge = temp_sfx_mix
    elif args.bgm and os.path.exists(args.bgm):
        filter_str = "[1:a]volume=0.12[bgm]; [0:a][bgm]amix=inputs=2:duration=first[m]; [m]loudnorm=I=-14:TP=-1.0:LRA=11[a_final]"
        cmd_master = [
            "ffmpeg", "-y",
            "-i", temp_voice_norm,
            "-i", args.bgm,
            "-filter_complex", filter_str,
            "-map", "[a_final]",
            "-c:a", "pcm_s16le",
            temp_sfx_mix
        ]
        run_cmd(cmd_master)
        audio_to_merge = temp_sfx_mix
    else:
        audio_to_merge = temp_voice_norm

    # Step 3: Combine visuals.mp4 with mastered audio
    print(f"🎬 Multiplexing visuals with mastered audio to: {args.out}...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", args.visuals,
        "-i", audio_to_merge,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-movflags", "+faststart",
        args.out
    ]
    run_cmd(cmd_mux)

    # Clean up temp
    for tmp in [temp_voice_norm, temp_sfx_mix]:
        if os.path.exists(tmp):
            os.remove(tmp)

    print(f"🏆 Step 6 Complete: Final Mastered Explainer Reel ready at {args.out}")

if __name__ == "__main__":
    main()
