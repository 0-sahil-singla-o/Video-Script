import numpy as np
import soundfile as sf
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

SR = 44100

def create_whoosh(path):
    # 0.4s filtered swept noise
    t = np.linspace(0, 0.4, int(SR * 0.4))
    noise = np.random.uniform(-1, 1, len(t))
    # Smooth amplitude bell curve peaking at 0.2s
    env = np.sin(np.pi * (t / 0.4)) ** 2
    # Frequency modulate with subtle sweep
    sweep = np.sin(2 * np.pi * (300 + 400 * t) * t)
    audio = (noise * 0.7 + sweep * 0.3) * env * 0.6
    sf.write(path, audio.astype(np.float32), SR)

def create_slam(path):
    # 0.45s heavy impact: 60Hz sub-bass punch + 1.2kHz metallic strike
    t = np.linspace(0, 0.45, int(SR * 0.45))
    sub = np.sin(2 * np.pi * 65 * np.exp(-t * 8) * t) * np.exp(-t * 9)
    metal = np.sin(2 * np.pi * 1250 * t) * np.exp(-t * 22) * 0.4
    click = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 40) * 0.3
    audio = (sub + metal + click) * 0.8
    sf.write(path, audio.astype(np.float32), SR)

def create_clink(path):
    # 0.35s coin ring: dual high harmonics (2300Hz & 4600Hz)
    t = np.linspace(0, 0.35, int(SR * 0.35))
    h1 = np.sin(2 * np.pi * 2350 * t) * np.exp(-t * 12)
    h2 = np.sin(2 * np.pi * 4700 * t) * np.exp(-t * 18) * 0.5
    h3 = np.sin(2 * np.pi * 7100 * t) * np.exp(-t * 25) * 0.2
    audio = (h1 + h2 + h3) * 0.45
    sf.write(path, audio.astype(np.float32), SR)

def create_click(path):
    # 0.06s crisp UI tap
    t = np.linspace(0, 0.06, int(SR * 0.06))
    pulse = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90)
    noise = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 120) * 0.2
    audio = (pulse + noise) * 0.5
    sf.write(path, audio.astype(np.float32), SR)

def create_bgm(path, duration=70.0):
    # Clean warm lo-fi ambient electronic bed with subtle harmonic chord pad and gentle pulse
    t = np.linspace(0, duration, int(SR * duration))
    bpm = 110
    beat_sec = 60.0 / bpm
    
    # 4-chord progression: D minor (D3, F3, A3) -> Bb major -> C major -> A minor
    chords = [
        [146.83, 174.61, 220.00], # Dm
        [116.54, 146.83, 174.61], # Bb
        [130.81, 164.81, 196.00], # C
        [110.00, 130.81, 164.81], # Am
    ]
    chord_len = beat_sec * 4 # 1 bar per chord
    
    pad = np.zeros_like(t)
    for i, chord in enumerate(chords):
        # repeat across duration
        t_start = i * chord_len
        while t_start < duration:
            t_end = min(t_start + chord_len, duration)
            idx_start = int(t_start * SR)
            idx_end = int(t_end * SR)
            if idx_end > idx_start:
                sub_t = t[idx_start:idx_end]
                sub_len = (idx_end - idx_start) / SR
                env = np.sin(np.pi * (sub_t - t_start) / sub_len) ** 0.5
                chord_wave = sum(np.sin(2 * np.pi * freq * sub_t) + 0.3 * np.sin(2 * np.pi * freq * 2 * sub_t) for freq in chord)
                pad[idx_start:idx_end] += chord_wave * env * 0.12
            t_start += len(chords) * chord_len
            
    # Soft warm heartbeat low pulse on beats 1 and 3
    pulse = np.zeros_like(t)
    num_beats = int(duration / beat_sec)
    for b in range(num_beats):
        if b % 2 == 0:
            bt_start = b * beat_sec
            bt_idx = int(bt_start * SR)
            pulse_len = int(0.18 * SR)
            if bt_idx + pulse_len < len(t):
                pt = np.linspace(0, 0.18, pulse_len)
                sub_kick = np.sin(2 * np.pi * 55 * np.exp(-pt * 15) * pt) * np.exp(-pt * 12)
                pulse[bt_idx:bt_idx+pulse_len] += sub_kick * 0.18
                
    bgm = pad + pulse
    # Normalize to -24 dB
    peak = np.max(np.abs(bgm))
    if peak > 0:
        bgm = (bgm / peak) * 0.25
        
    sf.write(path, bgm.astype(np.float32), SR)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procedural SFX and Ambient BGM Generator")
    parser.add_argument("--sfx-dir", default="projects/shopify-tokens/assets/sfx", help="Output directory for SFX")
    parser.add_argument("--bgm-dir", default="projects/shopify-tokens/assets/bgm", help="Output directory for BGM")
    parser.add_argument("--duration", type=float, default=70.0, help="Duration of BGM in seconds")
    args = parser.parse_args()

    out_sfx = args.sfx_dir
    out_bgm = args.bgm_dir
    os.makedirs(out_sfx, exist_ok=True)
    os.makedirs(out_bgm, exist_ok=True)
    
    create_whoosh(os.path.join(out_sfx, "whoosh.wav"))
    create_slam(os.path.join(out_sfx, "slam.wav"))
    create_clink(os.path.join(out_sfx, "clink.wav"))
    create_click(os.path.join(out_sfx, "click.wav"))
    create_bgm(os.path.join(out_bgm, "ambient_bed.wav"), duration=args.duration)
    print(f"✓ All procedural SFX & Ambient BGM ({args.duration}s) generated successfully in {out_sfx} and {out_bgm}")
