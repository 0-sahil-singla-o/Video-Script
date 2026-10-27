# Voice Measurements & Registry

This registry logs tested voice presets, pacing, and tone characteristics.

| Voice Key | Model | Pace (WPM) | Pitch | Characteristics | Best Used For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `am_michael` | Kokoro | ~160 | Mid | Clear, modern, conversational tech tone | General narration |
| `am_onyx` | Kokoro | ~145 | Deep | Rich, resonant, authoritative | Intros, serious points |
| `am_michael,am_onyx` | Kokoro (Blend) | ~152 | Mid-Deep | Steady, grounded, studio tech narrator | **Default Explainer Voice** |
| `af_heart` | Kokoro | ~165 | Warm | Friendly, approachable, expressive | Product walkthroughs |
| `af_bella` | Kokoro | ~155 | Soft | Calm, gentle, educational | Deep dives, tutorials |

### Pronunciation Overrides (Phonetic Dictionary)
When Kokoro mispronounces technical terms, replace them in the spoken line:
- `Redis` -> `Red iss`
- `SQL` -> `sequel`
- `PostgreSQL` -> `postgres Q L`
- `Nginx` -> `engine X`
- `Kubernetes` -> `koober netties`
- `v1.2` -> `version one point two`
- `$5.1M` -> `five point one million dollars`
