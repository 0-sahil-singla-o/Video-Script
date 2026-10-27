# Project Memory & Decisions: ip-and-dns-explained

## Decisions & Defaults
- **Audience**: Complete beginners / non-technical students.
- **Narrator**: Kokoro-82M blended voice (`am_michael,am_onyx`), speed 1.05.
- **Duration**: 108.3 seconds (255 spoken words across 22 micro-scenes, 3,249 frames @ 30fps).
- **Subtitles**: Dynamic karaoke word-level highlighting in `#00E599` (neon green active, 1.18x) and `#FF6B4A` (coral key terms) with phrase progress bar.
- **Brand CTA Handle**: `@code_explains`
- **Audio Mix**: Voice -16 LUFS, BGM -22 dB, procedural Foley SFX on scene transitions, master audio locked at -14.0 LUFS EBU R128 with True Peak <= -1.0 dBFS.

## Approved Milestones
- [x] Step 0: Toolchain checked & initial questions confirmed
- [x] Step 1: Project scaffolded & design system specified
- [x] Step 2: script.md written & user approved
- [x] Step 3: Kokoro voice synthesis (voice.wav 108.2s) & Faster-Whisper alignment verified (word_timestamps.json & transcript_words.json)
- [x] Step 4: Static storyboard preview (storyboard.html) reviewed & user approved
- [x] Step 5: 3D scenes (index.html) built with CSS 3D & GSAP (all 22 scenes and 63 phrase cards)
- [x] Step 6: HyperFrames check passed (0 errors, 45/45 WCAG AA contrast, motion valid)
- [x] Step 7: Frame-by-frame 3D render & -14 LUFS multi-track audio master (dist/visuals.mp4 & dist/final_reel.mp4)
- [x] Step 8: Visual contact sheet & post-copy generated (dist/contact_sheet.png & post-copy.md)
