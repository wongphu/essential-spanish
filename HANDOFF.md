# Essential Spanish — handoff

Kitchen-table booklet for **English-speaking retirees living in Panama**. Goal: be understood in daily life (farmacia, clinic, taxi, neighbors), not pass a grammar exam.

**Date:** 2026-09-10

---

## What to give the reader

| Format | File | Use |
|---|---|---|
| **PDF (print)** | `essential-spanish.pdf` | Print or keep on a tablet. Letter size, ~34 pages. |
| **Web (phone)** | `index.html` + `audio/` | Open in a browser. Keep the `audio` folder **next to** the HTML file. Speaker buttons play each Spanish line. |

Do **not** ship `essential-spanish-grammar.pdf` — that old filename was retired when the title dropped “Grammar.”

The web page also has **A− / A+** type-size buttons and a jump-to-chapter menu. Audio is web-only (not in the PDF).

---

## How to rebuild

From this folder, on macOS:

```bash
python3 build_booklet.py
```

That regenerates:

1. `index.html`
2. MP3s in `audio/` for any **new** Spanish lines (existing clips are cached)
3. `essential-spanish.pdf`

**Needs**

- Python 3.9+ with `reportlab` and `pypdf` (`python3 -m pip install --user reportlab pypdf`)
- macOS fonts: Georgia + Verdana under `/System/Library/Fonts/Supplemental/`
- For audio: **oMLX** with **Qwen3-TTS-12Hz-1.7B-Base-8bit** (`omlx start`; `http://127.0.0.1:8000/v1/audio/speech`)
- Optional: `ffmpeg` if oMLX returns WAV instead of MP3

First audio run takes a minute or two (~386 clips). Later runs only build new hashes.

Edit **content** in `booklet_content.py`, then rebuild. Do not hand-edit `index.html` or the PDF; they are generated.

---

## Repo layout

| Path | Role |
|---|---|
| `booklet_content.py` | Source of truth: title, chapters, tables, phrases |
| `build_booklet.py` | HTML + PDF + TTS generator |
| `index.html` | Generated web booklet |
| `essential-spanish.pdf` | Generated print booklet |
| `audio/*.mp3` | Generated clips; filename is a hash of the spoken text |
| `HANDOFF.md` | This file |

---

## Content map

Tone: conversational, large type, Panama examples. `usted` is the default “you.” No *vosotros*. No *vos* (Panama does not use it).

1. **Start here** — how to use it; what actually trips English speakers  
2. **Ch. 1** — fifteen workhorse sentences (with pronunciation respelling)  
3. **Ch. 2** — sounds; vowels matter more than a rolled *rr*; coastal *s*-dropping  
4. **Ch. 3** — *el/la*; learn the article with the noun; deceptive-gender list  
5. **Ch. 4** — adjectives  
6. **Ch. 5** — pronouns; *usted* vs *tú* in Panama  
7. **Ch. 6** — *ser / estar / hay* — **estar is the one to practice**  
8. **Ch. 7** — present tense  
9. **Ch. 8** — daily verbs  
10. **Ch. 9** — *gustar* (don’t say *yo gusto*)  
11. **Ch. 10** — questions, *no*, and the magic five (*quiero / puedo / necesito / tengo que / voy a*)  
12. **Ch. 11** — two pasts; the English trap (don’t use the snapshot past for “used to / was -ing”)  
13. **Ch. 12** — commands: **formal (usted) and informal (tú)** side by side  
14. **Ch. 13** — *por / para* in daily chunks  
15. **Ch. 14** — location + personal *a*  
16. **Ch. 15** — numbers, money (USD/balboa), time  
17. **Ch. 16** — little words; *lo/la* as recognition  
18. **Ch. 17** — Panama layer (local words, building-manager note)  
19. **Ch. 18** — phrasebook (clinic, pharmacy, restaurant, home repairs, taxi, 911)  
20. **Cheat sheets** — photo page  
21. **Pocket page** — wallet card  

Chapters 12 (commands), cheat sheets, and the pocket page are the ones people will actually carry.

---

## Design and product decisions (don’t undo these lightly)

Drawn from SLA research on English speakers learning Spanish, plus a Peace Corps / El Salvador listener study:

- **Wrong *ser/estar* or wrong past** often confuses a listener. **Wrong *el/la*** almost never does. Teach gender as a lookup list, not a fear.
- English speakers **overuse *ser***. The work is **estar** (feelings, open/closed, ready/broken).
- **Subjunctive is skipped.** Textbooks love it; input is sparse; it is not needed for this audience.
- **Personal *a*** is a high-frequency classroom miss; show it, don’t lecture.
- **Pronouns** are hard in production; the booklet treats *lo/la/se lo* as *recognition first*.
- Audio uses local **Qwen3-TTS** through oMLX (`Qwen3-TTS-12Hz-1.7B-Base-8bit`, language `Spanish`). Panama coastal speech drops final *s*; the clips will sound “clearer than the taxi.”
- Chapter 15 number grid does **not** send Arabic digits (`0`, `1`, `1,000`, …) to TTS. Speaker buttons still play the Spanish word (`cero`, `mil`).

Visual: cream paper, teal + coral + gold. Cover and running header say **Essential Spanish**, not “Grammar.” Web speaker icon is a cone + two sound waves in a **small** teal circle.

---

## How content is structured

Each chapter in `booklet_content.py` is a dict:

```python
{
  "id": "commands",          # HTML anchor
  "kicker": "Chapter 12",
  "title": "Please do this: commands",
  "intro": "...",
  "newpage": True,           # optional: start on a new PDF page
  "blocks": [ ... ],
}
```

Block types: `p`, `h2`, `tip`, `panama`, `callout`, `ul`, `ol`, `table`, `pairs`, `phrases`, `note`.

Spanish in running text uses `<es>...</es>` so it renders teal/bold in both HTML and PDF.

**Tables**

- Default: first column is Spanish  
- `"emphasis": "two-es"` — first two columns Spanish (used for usted/tú commands)  
- `"emphasis": "all"` + `"hide_header": True` — number grid  

**Audio (web only)**  
Play buttons wrap Spanish cells in `pairs`, `phrases`, and Spanish table columns. Spoken text is cleaned (markup stripped, ` / ` → comma). Chapter 15 (`tts_skip_digits`) also drops Arabic numerals so `0 cero` is spoken as `cero`. Clip id = SHA-1 of `model|spoken`, first 12 hex chars. If an MP3 is missing, the page falls back to the browser’s Spanish voice.

---

## What is not done

- No Panamanian-accent TTS (Qwen3-TTS Base has no named speakers; language is set to Spanish)
- No audio in the PDF
- No app store / hosting setup — `index.html` is opened locally or dropped on any static host **with** the `audio/` folder
- No spaced-repetition drills or quizzes
- No study of long-term Panama retirees (research used classroom SLA + Central American Peace Corps data)

---

## Likely next edits

| Request | Where |
|---|---|
| Change wording or add a phrase | `booklet_content.py`, then `python3 build_booklet.py` |
| New Spanish line with audio | Same; new MP3s generate automatically |
| Different TTS model / server | `OMLX_TTS_MODEL` / `OMLX_BASE_URL` (defaults in `build_booklet.py`) |
| Force-rebuild all audio | Delete `audio/` and rebuild |
| Host the web booklet | Upload `index.html` + `audio/` together; relative `audio/{id}.mp3` paths must stay |

Keep the booklet short. If adding a topic, ask whether a retiree needs it at the farmacia this week.
