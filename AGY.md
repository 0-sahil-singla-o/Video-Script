# Studio Rules: Video Editing Helper

## 1. Output Specifications
- Format: Vertical 9:16 (1080 x 1920 pixels)
- Frame Rate: 30 fps
- Codec: H.264 (libx264) MP4 with AAC 256kbps audio
- Delivery: `+faststart` moov atom at beginning of file for instant playback

## 2. Audio Standards (By The Numbers)
- Voice Normalization: -16 LUFS (Integrated)
- Master Normalization: -14 LUFS (Integrated)
- True Peak Clamp: -1.0 dBFS maximum
- Background Music (BGM): Leveled at -20 dB to -24 dB relative to voice. NEVER aggressively duck.
- SFX Cues: Max duration 0.2s–0.4s for quick accents (pops, swooshes, clicks).

## 3. Visual & Safe Zone Standards
- Top Margin: 180px safe zone
- Bottom Margin: 360px safe zone (clear of Reels / TikTok UI)
- Right Margin: 130px safe zone (clear of platform like/share buttons)
- Consistency: Keep concept colors locked across all scenes in a video.

## 4. Voice Configuration
- Engine: Kokoro-82M
- Default Voice Blend: `am_michael,am_onyx` (Deep, steady explainer tone)
- Default Speech Rate: 1.05x
- Inter-line Pause: 0.25 seconds
- Precision Clock: Word boundary extraction via Faster-Whisper
