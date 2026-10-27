param (
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    [string]$Voice = "am_michael,am_onyx",
    [double]$Speed = 1.05,
    [switch]$SkipTTS
)

$baseDir = Split-Path -Parent $PSScriptRoot
$projectDir = Join-Path $baseDir "projects\$ProjectName"
$distDir = Join-Path $projectDir "dist"
$py = "C:\Users\ssingla\AppData\Local\Programs\Python\Python311\python.exe"

# Ensure bin is on PATH for ffmpeg/ffprobe
$env:Path = "$baseDir\bin;" + $env:Path

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "STARTING PRODUCTION: $ProjectName" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (-not $SkipTTS) {
    # Step 1: Kokoro TTS Voice Generation
    Write-Host "`n[1/6] Generating voice narration with Kokoro-82M ($Voice)..." -ForegroundColor Yellow
    & $py "$baseDir\scripts\tts_lines.py" `
        --script "$projectDir\script.md" `
        --out-dir "$distDir" `
        --voice "$Voice" `
        --speed $Speed

    if ($LASTEXITCODE -ne 0) { Write-Error "TTS generation failed"; exit 1 }

    # Step 2: Faster-Whisper Word-Level Alignment
    Write-Host "`n[2/6] Aligning word timestamps with Faster-Whisper..." -ForegroundColor Yellow
    & $py "$baseDir\scripts\align_whisper.py" `
        --audio "$distDir\voice.wav" `
        --script "$projectDir\script.md" `
        --out "$projectDir\word_timestamps.json"

    if ($LASTEXITCODE -ne 0) { Write-Error "Whisper alignment failed"; exit 1 }
} else {
    Write-Host "`nSkipping TTS and Alignment (using existing audio and timestamps)" -ForegroundColor DarkGray
}

# Step 3: Procedural SFX & Ambient BGM check
Write-Host "`n[3/6] Ensuring Foley and Ambient BGM tracks..." -ForegroundColor Yellow
& $py "$baseDir\scripts\generate_audio_assets.py" `
    --sfx-dir "$projectDir\assets\sfx" `
    --bgm-dir "$projectDir\assets\bgm" `
    --duration 120.0

# Step 4: Validate Scenes with HyperFrames Check
Write-Host "`n[4/6] Running HyperFrames scene QA check..." -ForegroundColor Yellow
Set-Location $baseDir
npx hyperframes check "$projectDir"

# Step 5: Render 3D Scenes to MP4
Write-Host "`n[5/6] Rendering 3D scenes to MP4 (1080x1920 at 30fps)..." -ForegroundColor Yellow
$visualsMp4 = "$distDir\visuals.mp4"
npx hyperframes render "$projectDir" -o "$visualsMp4"

if ($LASTEXITCODE -ne 0) { Write-Error "HyperFrames render failed"; exit 1 }

# Step 6: Audio Mixing & Mastering (-14 LUFS)
Write-Host "`n[6/6] Mastering final multi-track audio mix (-14 LUFS)..." -ForegroundColor Yellow
$finalReel = "$distDir\final_reel.mp4"
$bgmTrack = "$projectDir\assets\bgm\ambient_bed.wav"
$sfxDir = "$projectDir\assets\sfx"

& $py "$baseDir\scripts\mix_audio.py" `
    --visuals "$visualsMp4" `
    --voice "$distDir\voice.wav" `
    --bgm "$bgmTrack" `
    --sfx-dir "$sfxDir" `
    --out "$finalReel"

# Step 7: QA Contact Sheet
Write-Host "`nGenerating QA Contact Sheet..." -ForegroundColor Yellow
$contactSheet = "$distDir\contact_sheet.png"
& $py "$baseDir\scripts\contact_sheet.py" `
    --video "$finalReel" `
    --out "$contactSheet"

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "PRODUCTION COMPLETE!" -ForegroundColor Green
Write-Host "   Final Mastered Reel: $finalReel" -ForegroundColor Green
Write-Host "   QA Contact Sheet:    $contactSheet" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
