param (
    [Parameter(Mandatory=$true)]
    [string]$ProjectName
)

$baseDir = Split-Path -Parent $PSScriptRoot
$projectDir = Join-Path $baseDir "projects\$ProjectName"

if (Test-Path $projectDir) {
    Write-Warning "Project '$ProjectName' already exists at $projectDir"
    exit 1
}

New-Item -ItemType Directory -Path "$projectDir\scenes" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir\dist" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectDir\assets" -Force | Out-Null

# Create script.md template
@"
# $ProjectName

## 1. THE HOOK
> VISUAL: Dark minimal studio. Slow camera drift.
> ON SCREEN: "The Core Problem"
Every distributed system has one hidden trap.

## 2. THE EVERYDAY METAPHOR
> VISUAL: Everyday physical item appears.
> ON SCREEN: "Analogy"
Imagine trying to pick up an item at the exact same moment.

## 3. THE SOLUTION
> VISUAL: The trick in action.
> ON SCREEN: "The Fix"
Instead of fighting over one lock, separate them into tokens.
"@ | Set-Content "$projectDir\script.md"

# Create design.md template
@"
# Design System: $ProjectName

## Palette
- Primary: #FF6B4A (Coral)
- Secondary: #00758F (Blue)
- Background: #0D0F12
- Surface: #1A1E29
- Text: #FFFFFF
- Accent: #10B981 (Green)

## Safe Zones
- Canvas: 1080 x 1920
- Bottom Safe Zone: 360px
- Right Safe Zone: 130px
- Top Safe Zone: 180px
"@ | Set-Content "$projectDir\design.md"

# Create notes.md template
@"
# Project Memory & Decisions: $ProjectName

## Approved Milestones
- [ ] Script approved
- [ ] Storyboard approved
- [ ] Voice generated & checked
- [ ] 3D scenes rendered
- [ ] Audio mastered

## Fixes & Lessons Learned
- None yet.
"@ | Set-Content "$projectDir\notes.md"

# Create post-copy.md template
@"
# Social Copy: $ProjectName

## Instagram Reel
Hook: ...
Caption: ...
Tags: #systemdesign #coding #webdev #backend #softwareengineering

## X (Twitter)
Post: ...

## LinkedIn
Problem: ...
Solution: ...
Key Takeaway: ...
"@ | Set-Content "$projectDir\post-copy.md"

Write-Host "✅ Created project '$ProjectName' at $projectDir" -ForegroundColor Green
