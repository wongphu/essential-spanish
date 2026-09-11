# Essential Spanish

A kitchen-table booklet for **English-speaking retirees living in Panama**.

You don't need to be fluent. You need to be understood — at the farmacia, the clinic, the taxi, and with the neighbor who waters your plants.

This is not a grammar exam. It is a short, large-type guide with Panama examples, `usted` as the default “you,” and no *vosotros*.

## Use it

| Format | File | Notes |
|---|---|---|
| **Print / tablet** | [`essential-spanish.pdf`](essential-spanish.pdf) | Letter size, about 37 pages. |
| **Phone (with audio)** | [`index.html`](index.html) + [`audio/`](audio/) | Open the HTML in a browser. Keep the `audio` folder next to the HTML file. Speaker buttons play each Spanish line. |

The web page has **A− / A+** type-size buttons and a jump-to-chapter menu. Audio is web-only (not in the PDF).

To host the web booklet, upload `index.html` and the `audio/` folder together so the relative `audio/{id}.mp3` paths still work.

## What's inside

1. **Start here** — how to use it; what actually trips English speakers
2. Fifteen workhorse sentences (with pronunciation respelling)
3. Sounds — vowels matter more than a rolled *rr*
4. *el / la* — learn the article with the noun
5. Adjectives
6. Pronouns — *usted* vs *tú* in Panama
7. *ser / estar / hay* — **estar is the one to practice**
8. Present tense
9. Daily verbs
10. *gustar* (don't say *yo gusto*)
11. Questions, *no*, and the magic five (*quiero / puedo / necesito / tengo que / voy a*)
12. Two pasts
13. Commands: formal (*usted*) and informal (*tú*) side by side
14. *por / para* in daily chunks
15. Location + personal *a*
16. Numbers, money (USD/balboa), time
17. Little words; *lo / la* as recognition
18. Panama layer (local words)
19. Phrasebook — clinic, pharmacy, restaurant, home repairs, taxi, 911
20. Cheat sheets (photo page) and a pocket/wallet card

Chapters 12 (commands), the cheat sheets, and the pocket page are the ones people actually carry.

## Rebuild

Content lives in `booklet_content.py`. Do not hand-edit `index.html` or the PDF; they are generated.

From this folder, on macOS:

```bash
python3 -m pip install --user reportlab pypdf
python3 build_booklet.py
```

That regenerates:

1. `index.html`
2. MP3s in `audio/` for any **new** Spanish lines (existing clips are cached)
3. `essential-spanish.pdf`

**Needs**

- Python 3.9+ with `reportlab` and `pypdf`
- macOS fonts: Georgia and Verdana under `/System/Library/Fonts/Supplemental/`
- For audio: **oMLX** running locally with **Qwen3-TTS-12Hz-1.7B-Base-8bit** (`omlx start`, default `http://127.0.0.1:8000`)
- Optional: `ffmpeg` if oMLX returns WAV instead of MP3

The first audio run takes several minutes (~480 clips). Later runs only build new hashes. Clip ids include the TTS model name, so switching models regenerates audio.

| Request | Where |
|---|---|
| Change wording or add a phrase | `booklet_content.py`, then `python3 build_booklet.py` |
| New Spanish line with audio | Same; new MP3s generate automatically |
| Different TTS model / server | `OMLX_TTS_MODEL` / `OMLX_BASE_URL` (or the constants in `build_booklet.py`) |
| Force-rebuild all audio | Delete `audio/` and rebuild |

## Layout

| Path | Role |
|---|---|
| `booklet_content.py` | Source of truth: title, chapters, tables, phrases |
| `build_booklet.py` | HTML + PDF + TTS generator |
| `index.html` | Generated web booklet |
| `essential-spanish.pdf` | Generated print booklet |
| `audio/*.mp3` | Generated clips; filename is a hash of the spoken text |
| `HANDOFF.md` | Maintainer notes (design decisions, content structure, known gaps) |

Keep the booklet short. If adding a topic, ask whether a retiree needs it at the farmacia this week.
