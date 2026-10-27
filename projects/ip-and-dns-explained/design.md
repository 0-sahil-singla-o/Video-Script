# Design System: ip-and-dns-explained

## 1. Palette
- **Background**: `#07090E` (Deep obsidian void with subtle `#0D1527` gradient)
- **Primary / Network Blue**: `#00D2FF` (IP addresses, network packets, digital pathways)
- **Success / Verified Green**: `#00E599` (Authoritative answers, cache hits, 200 OK)
- **Keyword / Highlight Coral**: `#FF6B4A` (DNS terms, key concepts, TTL notes)
- **Error / Miss Red**: `#EF4444` (DNS lookup failure, cache miss, offline)
- **Surface / Card Background**: `#0F172A` (Dark slate with `#1E293B` borders)
- **Text Primary**: `#F8FAFC` (High contrast pure off-white, > 7:1 ratio)
- **Text Secondary / Muted**: `#94A3B8` (WCAG AA compliant > 4.5:1)

## 2. Safe Zones (1080 × 1920 Vertical)
- **Canvas Dimensions**: 1080px × 1920px (9:16 portrait)
- **Top Safe Margin**: 180px (Reserved for status bars & search overlays)
- **Bottom Safe Margin**: 380px (Reserved for platform caption bars, profile handles, audio tags)
- **Right Safe Margin**: 130px (Reserved for like, share, and comment rails)
- **Active Visual & Caption Band**: 180px to 1540px height, centered horizontally within 880px width

## 3. Typography
- **Headlines & Banners**: Bold Geometric Grotesk (`Inter`, `system-ui`), font-weight: 900
- **Technical & Terminal**: Monospace (`ui-monospace`, `Consolas`, `SF Mono`), font-weight: 700
- **Dynamic Subtitles**: 44px font size, 700 weight, active karaoke word 1.18x scale in `#00E599` / `#FF6B4A`
