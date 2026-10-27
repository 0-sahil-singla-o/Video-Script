# 🎬 Code-Driven 3D Video Studio: Complete Architecture & Script Specification

> **For AI Agents (Claude Code, ChatGPT, Gemini, etc.)**:  
> This document specifies the exact architecture, data contracts, and scripting workflow of this repository. When given a topic, you will write the `script.md`, design the scenes, and orchestrate the build pipeline following these rules.

---

## 1. Core Concept: "The Studio is a Folder"
This engine generates high-retention 3D motion graphics explainer reels **without traditional video editing software** (no Premiere, no After Effects). 

- **Scenes are Web Pages**: 3D objects, animations, and transitions are written in HTML, CSS 3D (`transform-style: preserve-3d`), SVG, and GSAP.
- **Voice is Code**: Spoken audio is generated locally using open-source **Kokoro-82M TTS**.
- **Timing is Data**: Speech is aligned to millisecond clocks using **Faster-Whisper**.
- **Renderer is Headless Chrome**: **HyperFrames** seeks the GSAP timeline frame-by-frame and exports directly to MP4 via **FFmpeg**.
- **Sound is Numbers**: Audio loudness is mathematically locked to broadcast standards (**-14 LUFS**).

---

## 2. Directory Structure

```
video-editing-helper/
├── CLAUDE.md / AGY.md         # Studio rules (resolution, safe zones, loudness standards)
├── SYSTEM_SPEC.md             # This specification file
├── scripts/
│   ├── new-video.ps1          # Scaffolds a new project directory
│   ├── tts_lines.py           # Kokoro TTS: extracts plain text from script.md -> dist/voice.wav
│   ├── align_whisper.py       # Faster-Whisper: extracts word clocks -> word_timestamps.json
│   ├── build_scenes.py        # Replaces {{t:word}} placeholders with real seconds
│   ├── generate_audio_assets.py # Procedural SFX (whoosh, slam, clink, click) & BGM
│   ├── mix_audio.py           # FFmpeg EBU R128 loudness mastering (-14 LUFS)
│   ├── contact_sheet.py       # Generates 16-frame visual audit PNG
│   └── build-video.ps1        # Master orchestrator script
└── projects/
    └── <project-name>/
        ├── script.md          # SINGLE SOURCE OF TRUTH (narration + stage directions)
        ├── design.md          # Color palette, typography & safe zones
        ├── notes.md           # Project decisions & approved milestones
        ├── post-copy.md       # Social captions for Instagram, X, LinkedIn
        ├── word_timestamps.json # Generated millisecond clock
        ├── index.html         # HyperFrames 3D composition & GSAP timeline
        └── dist/              # Generated voice.wav, visuals.mp4, final_reel.mp4
```

---

## 3. The `script.md` Specification (The Single Source of Truth)

Every video starts inside `projects/<project-name>/script.md`. The pipeline parses this file with strict rules:

### Syntax Rules:
1. **Plain Text Lines** = **Spoken Narration**.
   - These are the only lines sent to the Kokoro voice model.
   - Pacing: 15–20 words per scene (~4 to 7 seconds).
   - Total length for a 60s Reel: 140–160 words across 12–16 micro-scenes.
2. **Lines starting with `>`** = **Visual Directions & On-Screen Graphics**.
   - Ignored by the voice model. Read by the visual engine.
   - `> VISUAL:` Describes the physical 3D scene, materials, lighting, and camera movement.
   - `> ON SCREEN:` Describes text overlays, code snippets, metric tickers, and badges.
3. **Lines starting with `##`** = **Scene / Act Boundaries**.
   - Marks a distinct visual transition.

### Scripting Methodology (From Sushil Kumar's Article):
- **Rule 1: Show an Everyday Metaphor First**: Never start with raw database/backend jargon. Show an everyday physical object, then reveal its software equivalent:
  - *Notebook* $\rightarrow$ Database ledger
  - *Padlock / "Occupied" Sign* $\rightarrow$ Row-level lock (`SELECT ... FOR UPDATE`)
  - *Tokens in a glass bowl* $\rightarrow$ Bounded inventory rows (`SKIP LOCKED`)
- **Rule 2: The 1-Second Hook**: Scene 1 must show a high-stakes scenario, counter-intuitive trap, or race condition in the first 3 seconds.
- **Rule 3: Micro-Scene Density (No Static Dead Stretches)**: To make the video truly informative and visually engaging, change the visual state or camera angle every **2.5 to 4 seconds**.

---

## 4. The Timestamp Placeholder Contract: `{{t:word}}`

Instead of guessing animation timings or hardcoding seconds, scenes use **dynamic timestamp placeholders**:

```html
<!-- Inside index.html / GSAP -->
tl.from("#padlock", { y: -300, duration: 0.5 }, "{{t:locks the entire row}}");
tl.to("#token-2", { color: "#00E599" }, "{{t:skips to token 2}}");
```

### How the Pipeline Resolves Timestamps:
1. `tts_lines.py` runs on `script.md` $\rightarrow$ outputs `dist/voice.wav`.
2. `align_whisper.py` runs Faster-Whisper on `dist/voice.wav` $\rightarrow$ creates `word_timestamps.json`:
   ```json
   {
     "picture": 0.0,
     "black friday": 1.32,
     "locks the entire row": 22.38,
     "tokens in a bowl": 45.66,
     "skips to token 2": 58.00
   }
   ```
3. `build_scenes.py` scans the HTML, matches `{{t:word}}` against `word_timestamps.json`, and injects the exact second:
   ```html
   tl.from("#padlock", { y: -300, duration: 0.5 }, 22.38);
   ```
If the narration is re-recorded or re-timed, **all animations automatically adjust their timing with zero manual re-editing!**

---

## 5. Word-by-Word Karaoke Subtitles

To create high-engagement reels, subtitles must highlight the **active spoken word**:

### How It Works:
1. Whisper outputs individual word start and end times:
   ```json
   [
     { "word": "Black", "start": 1.32, "end": 1.58 },
     { "word": "Friday.", "start": 1.58, "end": 2.00 }
   ]
   ```
2. Words are grouped into 4–6 word phrase cards in the vertical safe zone (above 380px from bottom):
   ```html
   <div id="phrase-1" class="sub-phrase">
     <span id="w-4" class="sub-word">it</span>
     <span id="w-5" class="sub-word">is</span>
     <span id="w-6" class="sub-word">Black</span>
     <span id="w-7" class="sub-word">Friday.</span>
   </div>
   ```
3. GSAP tweens the active word:
   - At `w.start`: Word lights up neon green (`#00E599`) or coral (`#FF6B4A`), scales up (`1.18x`), and text glows.
   - At `w.end`: Settles to solid white (`#FFFFFF`) at regular scale (`1.0x`).
   - Inactive words remain semi-transparent grey (`rgba(255, 255, 255, 0.4)`).

---

## 6. Full Informative Script Example (16 Micro-Scenes)

Below is an example of a complete, production-grade `script.md` designed for high visual density:

```markdown
# How Shopify Stops Selling the Last Hoodie Twice

## 1. THE FLASH SALE
> VISUAL: 3D calendar block landing on November 27. Particle embers emit from edges.
> ON SCREEN: "BLACK FRIDAY FLASH SALE"
Picture this. It is Black Friday.

## 2. THE 10,000 CHECKOUTS
> VISUAL: Giant interactive checkout button bombarded by thousands of cursor shockwaves.
> ON SCREEN: "10,000 Checkouts / Second"
Ten thousand shoppers smash the checkout button

## 3. THE LAST HOODIE
> VISUAL: Frosted glass showcase with rotating 3D hoodie emblem. Counter drops from 10 to 1.
> ON SCREEN: "⚡ 1 LEFT IN STOCK"
for the last remaining hoodie at the exact same millisecond.

## 4. THE QUESTION
> VISUAL: Spotlight darkens. Giant glowing question mark and freeze-frame clock 00:00:00.001.
> ON SCREEN: "Who Wins? Race Condition"
Who wins?

## 5. THE SHARED NOTEBOOK
> VISUAL: Isometric 3D ledger notebook swings open in space showing row #402.
> ON SCREEN: "Database = Shared Ledger Notebook"
Think of your database like a physical notebook.

## 6. ROW SCANNING
> VISUAL: Glowing cyan server laser scanner tracks down the ledger table to row #402.
> ON SCREEN: "Scanning: Row #402 [Stock = 1]"
To buy an item, the server has to flip to that exact row,

## 7. CELL OVERWRITE
> VISUAL: The number 1 is struck through with eraser smoke and overwritten with red 0.
> ON SCREEN: "Stock: 1 -> 0"
erase the number one, and write zero.

## 8. THE LOCKDOWN
> VISUAL: Heavy industrial red 3D padlock slams down on row #402 with screen shake.
> ON SCREEN: "SELECT ... FOR UPDATE [ROW LOCKED]"
To stop two people from buying it, databases lock the entire row.

## 9. THE TRAFFIC JAM
> VISUAL: Queue of buyer avatars build up behind the padlock with spinning loader icons.
> ON SCREEN: "Connection Queue Overflow"
But during a flash sale, thousands of shoppers queue behind that single lock,

## 10. SERVER CRASH
> VISUAL: Red warning pulse. Database cylinder platters overheat.
> ON SCREEN: "⚠️ HTTP 504 GATEWAY TIMEOUT"
causing connection timeouts, spinning wheels, and crashed servers.

## 11. THE SHOPIFY TRICK
> VISUAL: Emerald matrix grid clears the screen, revealing Shopify system blueprint.
> ON SCREEN: "Shopify Bounded Unit Pool"
Here is the genius trick Shopify uses.

## 12. ROW SHATTERING
> VISUAL: 1 bottleneck row shatters into 6 parallel independent cards: Unit #1 to Unit #6.
> ON SCREEN: "Before: 1 Row with count 6 -> After: 6 Independent Rows"
Instead of one shared counter that says six, create six separate rows, one for each individual hoodie.

## 13. TOKENS IN A BOWL
> VISUAL: The 6 rows morph into 6 3D gold coins tumbling into a frosted glass bowl.
> ON SCREEN: "6 Physical Tokens in a Bowl"
Like six physical tokens sitting in a glass bowl.

## 14. SINGLE TOKEN QUERIES
> VISUAL: Query threads arrive at the bowl side-by-side.
> ON SCREEN: "Thread A & Thread B Concurrent Queries"
Now, every checkout query asks for just one token.

## 15. SKIP LOCKED BYPASS
> VISUAL: Thread A locks Token 1. Thread B's cursor detects lock, arcs over it, and claims Token 2.
> ON SCREEN: "SKIP LOCKED: Zero Waiting, Immediate Claim"
And if another customer is touching Token 1, the query doesn't wait in line. It immediately skips to Token 2.

## 16. MASSIVE THROUGHPUT
> VISUAL: 6 parallel green execution streams process transactions simultaneously without blockage.
> ON SCREEN: "0 Deadlocks • 100% Parallel Throughput"
No queue. No deadlocks. Thousands of transactions complete in parallel,

## 17. INVENTORY INTEGRITY
> VISUAL: Production SQL terminal shows SELECT ... SKIP LOCKED (0.84ms) and green verified stamp.
> ON SCREEN: "NEVER SOLD TWICE • 100% INTEGRITY"
and Shopify never sells that last hoodie twice.
```

---

## 7. The End-to-End Build Commands

When executing this workflow in terminal:

```powershell
# 1. Create a new project folder
.\scripts\new-video.ps1 -ProjectName "my-explainer"

# 2. (Write script.md inside projects/my-explainer/script.md)

# 3. Run the automated production pipeline
.\scripts\build-video.ps1 -ProjectName "my-explainer"
```

### What `build-video.ps1` executes automatically:
1. `tts_lines.py`: Synthesizes `dist/voice.wav` using Kokoro-82M.
2. `align_whisper.py`: Extracts word timestamps to `word_timestamps.json`.
3. `generate_audio_assets.py`: Generates procedural SFX cues and ambient BGM.
4. `hyperframes check`: Validates 3D layout, contrast (WCAG AA), and motion curves.
5. `hyperframes render`: Captures frame-by-frame (1080×1920 @ 30fps) to `dist/visuals.mp4`.
6. `mix_audio.py`: Masters voice (-16 LUFS), BGM (-22 dB), and SFX to final **-14 LUFS**.
7. `contact_sheet.py`: Exports 16-frame QA contact sheet to `dist/contact_sheet.png`.

---

## 8. Summary Checklist for Any AI Agent
- [ ] Every spoken word must be plain text in `script.md`.
- [ ] Every visual scene change must use `##` and `> VISUAL:`.
- [ ] Split scripts into micro-beats every 3–4 seconds to prevent static screens.
- [ ] Synchronize GSAP animations using `{{t:word}}` or `word_timestamps.json`.
- [ ] Implement word-level karaoke subtitle highlighting inside the 80% safe zone.
- [ ] Master final audio to -14 LUFS with True Peak $\le -1.0\text{ dBFS}$.
