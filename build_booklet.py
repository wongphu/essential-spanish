#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Essential Spanish booklet as HTML and PDF."""

from __future__ import annotations

import asyncio
import hashlib
import html as html_lib
import os
import re
from io import BytesIO
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from booklet_content import SECTIONS, SUBTITLE, TAGLINE, TITLE

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(ROOT, "docs")
HTML_PATH = os.path.join(DOCS_DIR, "index.html")
PDF_PATH = os.path.join(DOCS_DIR, "essential-spanish.pdf")
AUDIO_DIR = os.path.join(DOCS_DIR, "audio")
# Microsoft Edge neural TTS at build time (clips are cached MP3s).
# Roberto is Panamanian Spanish. Rate is slightly under 1.0 so the
# phrases are easier to catch. Needs internet only while generating.
TTS_MODEL = os.environ.get("EDGE_TTS_MODEL", "edge-tts")
TTS_VOICE = os.environ.get("EDGE_TTS_VOICE", "es-PA-RobertoNeural")
TTS_RATE = os.environ.get("EDGE_TTS_RATE", "-5%")
TTS_ATTEMPTS = int(os.environ.get("EDGE_TTS_ATTEMPTS", "5"))

# id -> spoken Spanish, filled while building HTML
UTTERANCES = {}
# section id -> PDF page, filled on the first layout pass
SECTION_PAGES = {}

TEAL = colors.HexColor("#0C5F5F")
TEAL_DARK = colors.HexColor("#084848")
CORAL = colors.HexColor("#B94A3C")
INK = colors.HexColor("#1A2424")
INK_SOFT = colors.HexColor("#3A4747")
SAND = colors.HexColor("#E8DCC8")
PAPER = colors.HexColor("#F6F0E6")
CARD = colors.HexColor("#FFFBF5")
TIP_BG = colors.HexColor("#E4F1EE")
PANAMA_BG = colors.HexColor("#F8E6D8")
GOLD = colors.HexColor("#A67C2D")
RULE = colors.HexColor("#CDBFA8")
HEADER_BG = colors.HexColor("#DCECEA")

FONT_DIR = "/System/Library/Fonts/Supplemental"


def register_fonts():
    pdfmetrics.registerFont(TTFont("Georgia", os.path.join(FONT_DIR, "Georgia.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", os.path.join(FONT_DIR, "Georgia Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", os.path.join(FONT_DIR, "Georgia Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-BoldItalic", os.path.join(FONT_DIR, "Georgia Bold Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Verdana", os.path.join(FONT_DIR, "Verdana.ttf")))
    pdfmetrics.registerFont(TTFont("Verdana-Bold", os.path.join(FONT_DIR, "Verdana Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Verdana-Italic", os.path.join(FONT_DIR, "Verdana Italic.ttf")))
    pdfmetrics.registerFontFamily(
        "Georgia",
        normal="Georgia",
        bold="Georgia-Bold",
        italic="Georgia-Italic",
        boldItalic="Georgia-BoldItalic",
    )
    pdfmetrics.registerFontFamily(
        "Verdana",
        normal="Verdana",
        bold="Verdana-Bold",
        italic="Verdana-Italic",
        boldItalic="Verdana-Bold",
    )


def make_styles():
    return {
        "kicker": ParagraphStyle(
            "kicker",
            fontName="Verdana-Bold",
            fontSize=9,
            leading=12,
            textColor=CORAL,
            spaceAfter=4,
            tracking=0.6,
            keepWithNext=True,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName="Georgia-Bold",
            fontSize=22,
            leading=26,
            textColor=TEAL_DARK,
            spaceAfter=10,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="Georgia-Bold",
            fontSize=14,
            leading=18,
            textColor=TEAL,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h2_compact": ParagraphStyle(
            "h2_compact",
            fontName="Georgia-Bold",
            fontSize=12.5,
            leading=16,
            textColor=TEAL,
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "intro": ParagraphStyle(
            "intro",
            fontName="Georgia-Italic",
            fontSize=12,
            leading=17,
            textColor=INK_SOFT,
            spaceAfter=10,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Georgia",
            fontSize=11.5,
            leading=16.5,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "body_left": ParagraphStyle(
            "body_left",
            fontName="Georgia",
            fontSize=11.5,
            leading=16.5,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "cell": ParagraphStyle(
            "cell",
            fontName="Georgia",
            fontSize=10.5,
            leading=14.5,
            textColor=INK,
        ),
        "cell_es": ParagraphStyle(
            "cell_es",
            fontName="Georgia-Bold",
            fontSize=10.5,
            leading=14.5,
            textColor=TEAL_DARK,
        ),
        "cell_head": ParagraphStyle(
            "cell_head",
            fontName="Verdana-Bold",
            fontSize=8.5,
            leading=12,
            textColor=TEAL_DARK,
        ),
        "cell_compact": ParagraphStyle(
            "cell_compact",
            fontName="Georgia",
            fontSize=9.5,
            leading=12.5,
            textColor=INK,
        ),
        "cell_es_compact": ParagraphStyle(
            "cell_es_compact",
            fontName="Georgia-Bold",
            fontSize=9.5,
            leading=12.5,
            textColor=TEAL_DARK,
        ),
        "tip_title": ParagraphStyle(
            "tip_title",
            fontName="Verdana-Bold",
            fontSize=9,
            leading=12,
            textColor=TEAL_DARK,
            spaceAfter=3,
        ),
        "tip_body": ParagraphStyle(
            "tip_body",
            fontName="Georgia",
            fontSize=10.5,
            leading=15,
            textColor=INK,
        ),
        "panama_title": ParagraphStyle(
            "panama_title",
            fontName="Verdana-Bold",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#7A3E16"),
            spaceAfter=3,
        ),
        "list": ParagraphStyle(
            "list",
            fontName="Georgia",
            fontSize=11.5,
            leading=16,
            textColor=INK,
            leftIndent=0,
        ),
        "pair_es": ParagraphStyle(
            "pair_es",
            fontName="Georgia-Bold",
            fontSize=12,
            leading=16,
            textColor=TEAL_DARK,
        ),
        "pair_en": ParagraphStyle(
            "pair_en",
            fontName="Georgia-Italic",
            fontSize=11.5,
            leading=16,
            textColor=INK_SOFT,
        ),
        "toc_page": ParagraphStyle(
            "toc_page",
            fontName="Verdana",
            fontSize=10,
            leading=14,
            textColor=TEAL_DARK,
            alignment=TA_RIGHT,
        ),
        "note": ParagraphStyle(
            "note",
            fontName="Georgia",
            fontSize=10.5,
            leading=15,
            textColor=INK,
        ),
        "toc_kicker": ParagraphStyle(
            "toc_kicker",
            fontName="Verdana",
            fontSize=8,
            leading=11,
            textColor=CORAL,
        ),
        "toc_item": ParagraphStyle(
            "toc_item",
            fontName="Georgia",
            fontSize=12,
            leading=16,
            textColor=TEAL_DARK,
        ),
    }


ES_TAG = re.compile(r"<es>(.*?)</es>", re.DOTALL)
BOLD_TAG = re.compile(r"<b>(.*?)</b>", re.DOTALL)
BR_TAG = re.compile(r"<br\s*/?>", re.IGNORECASE)


def rich_to_rl(text: str) -> str:
    """Convert light markup to reportlab XML."""

    def repl_es(m):
        inner = xml_escape(m.group(1))
        return f'<font name="Georgia-Bold" color="#0C5F5F">{inner}</font>'

    parts = []
    last = 0
    work = text.replace("\n", "<br/>")
    for m in ES_TAG.finditer(work):
        parts.append(xml_escape(work[last:m.start()]).replace("&lt;br/&gt;", "<br/>"))
        parts.append(repl_es(m))
        last = m.end()
    parts.append(xml_escape(work[last:]).replace("&lt;br/&gt;", "<br/>"))
    out = "".join(parts)
    # Restore <br/> that we escaped if they came through xml_escape of leftover
    out = out.replace("&lt;br/&gt;", "<br/>")
    return out


def tts_text(raw: str, skip_digits: bool = False) -> str:
    """Plain Spanish for the speaker: strip markup, English asides, and slashes."""
    text = ES_TAG.sub(r"\1", raw or "")
    text = re.sub(r"<[^>]+>", "", text)
    # Ellipsis is a prompt, not a comma. "¿Dónde está…?" must not become "está,?"
    text = text.replace("…", " ")
    text = re.sub(r"\.{3,}", " ", text)
    text = re.sub(r"\([^)]*\)", " ", text)

    def _expand_o_a(m):
        masc = m.group(1)
        fem = masc[:-1] + ("A" if masc[-1].isupper() else "a")
        return masc + ", " + fem

    # alérgico/a → alérgico, alérgica (before slash folding)
    text = re.sub(r"(\w+o)/a\b", _expand_o_a, text, flags=re.IGNORECASE)
    text = text.replace(" / ", ", ")
    text = text.replace("/", " ")
    text = re.sub(r"\s*\+\s*verb\b", " ", text, flags=re.I)
    text = re.sub(r"\bX\b", "treinta", text)
    if skip_digits:
        # Chapter 15 number grid: speak "cero", not "0 cero".
        text = re.sub(r"\d+(?:[.,]\d+)*", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" ,")
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\s+([?!.])", r"\1", text)
    return text.strip()


def audio_id(spoken: str) -> str:
    payload = f"{TTS_MODEL}|{TTS_VOICE}|{TTS_RATE}|{spoken}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def register_utterance(raw: str, always: bool = False, skip_digits: bool = False):
    spoken = tts_text(raw, skip_digits=skip_digits)
    if not spoken or not any(c.isalpha() for c in spoken):
        return None
    if not always and not re.search(r"[\s/¿?¡!.,;]", spoken) and len(spoken) < 8:
        return None
    uid = audio_id(spoken)
    UTTERANCES[uid] = spoken
    return uid, spoken


SPEAKER_SVG = (
    '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">'
    '<path fill="currentColor" d="M3 9v6h4l5 5V4L7 9H3z"/>'
    '<path fill="currentColor" d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>'
    '<path fill="currentColor" d="M14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>'
    "</svg>"
)


def play_wrap(raw: str, inner_html: str, always: bool = False, skip_digits: bool = False) -> str:
    info = register_utterance(raw, always=always, skip_digits=skip_digits)
    if not info:
        return inner_html
    uid, spoken = info
    label = html_lib.escape("Hear: " + spoken, quote=True)
    say = html_lib.escape(spoken, quote=True)
    return (
        f'<span class="say">'
        f'<button type="button" class="play" data-id="{uid}" data-say="{say}" '
        f'aria-label="{label}" title="{label}" aria-pressed="false">{SPEAKER_SVG}</button>'
        f"{inner_html}</span>"
    )


def split_spoken_alts(raw: str) -> list[str]:
    """Split 'hola / adiós' into two clips; ignore slashes inside parentheses."""
    parts = []
    buf = []
    depth = 0
    i = 0
    s = raw or ""
    while i < len(s):
        ch = s[i]
        if ch == "(":
            depth += 1
            buf.append(ch)
            i += 1
        elif ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
            i += 1
        elif depth == 0 and s.startswith(" / ", i):
            part = "".join(buf).strip()
            if part:
                parts.append(part)
            buf = []
            i += 3
        else:
            buf.append(ch)
            i += 1
    part = "".join(buf).strip()
    if part:
        parts.append(part)
    if len(parts) > 1:
        raw_s = (raw or "").strip()
        # Keep a single question with internal alternatives as one clip:
        # "¿Tiene algo para el dolor / el resfriado / la alergia?"
        if raw_s.count("¿") == 1 and raw_s.endswith("?") and any(not p.endswith("?") for p in parts[:-1]):
            return [raw_s]
    return parts


def play_segments(raw: str, always: bool = False, skip_digits: bool = False) -> str:
    parts = split_spoken_alts(raw)
    if len(parts) <= 1:
        return play_wrap(raw, rich_to_html(raw), always=always, skip_digits=skip_digits)
    bits = []
    for i, part in enumerate(parts):
        bits.append(play_wrap(part, rich_to_html(part), always=always, skip_digits=skip_digits))
        if i < len(parts) - 1:
            bits.append('<span class="slash"> / </span>')
    return '<span class="say-group">' + "".join(bits) + "</span>"


def resolve_audio_cols(block) -> set:
    headers = block.get("headers") or block.get("columns") or []
    rows = block.get("rows") or []
    n = len(headers) if headers else (len(rows[0]) if rows else 0)
    if "audio_cols" in block:
        return {int(i) for i in block["audio_cols"] if 0 <= int(i) < n}
    emphasis = block.get("emphasis", "first")
    if emphasis == "all":
        return set(range(n))
    if emphasis == "two-es":
        return {i for i in (0, 1) if i < n}
    if emphasis == "none":
        return set()
    first = headers[0] if headers else "Spanish"
    if first in ("Person", "", "Letter", "If it ends in…", "If English can say…"):
        return set()
    return {0} if n else set()


def rich_to_html(text: str) -> str:
    def repl_es(m):
        return f'<span lang="es">{html_lib.escape(m.group(1))}</span>'

    parts = []
    last = 0
    for m in ES_TAG.finditer(text):
        parts.append(html_lib.escape(text[last:m.start()]).replace("\n", "<br>"))
        parts.append(repl_es(m))
        last = m.end()
    parts.append(html_lib.escape(text[last:]).replace("\n", "<br>"))
    return "".join(parts)


def box_table(inner_flowables, bg, border, width):
    data = [[inner_flowables]]
    t = Table(data, colWidths=[width])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.6, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBEFORE", (0, 0), (0, -1), 5, border),
            ]
        )
    )
    t.hAlign = "LEFT"
    return t


def stacked_paragraphs(items, styles):
    flow = []
    for i, p in enumerate(items):
        sp = 0 if i == len(items) - 1 else 4
        flow.append(Paragraph(p, styles["tip_body"]))
        if sp:
            flow.append(Spacer(1, sp))
    return flow


def cell_style_for(headers, col_index, styles, emphasis, audio_cols=None, compact=False):
    es = styles["cell_es_compact"] if compact else styles["cell_es"]
    body = styles["cell_compact"] if compact else styles["cell"]
    if audio_cols is not None:
        return es if col_index in audio_cols else body
    if emphasis == "all":
        return es
    if emphasis == "two-es":
        return es if col_index < 2 else body
    if emphasis == "none":
        return body
    first = headers[0] if headers else "Spanish"
    if first in ("Person", ""):
        return body if col_index == 0 else es
    if first in ("Use", "Start with", "Pattern", "When"):
        return es if col_index == 0 else body
    if col_index == 0:
        return es
    return body


def make_grid(headers, rows, styles, width, emphasis="first", hide_header=False, audio_cols=None, compact=False):
    n = len(headers) if headers else (len(rows[0]) if rows else 1)
    if n == 0:
        return Spacer(1, 1)
    first = headers[0] if headers else ""
    audio_set = set(audio_cols) if audio_cols is not None else None
    if n == 2:
        if first in ("Person", "Letter"):
            weights = [0.28, 0.72]
        else:
            weights = [0.48, 0.52]
    elif n == 3:
        if emphasis == "two-es":
            weights = [0.32, 0.32, 0.36]
        else:
            weights = [0.34, 0.28, 0.38]
    elif n == 4:
        if audio_set == {0, 2}:
            weights = [0.28, 0.22, 0.28, 0.22]
        else:
            weights = [0.25, 0.25, 0.25, 0.25]
    elif n == 5:
        weights = [0.24, 0.19, 0.19, 0.19, 0.19]
    else:
        weights = [1 / n] * n
    col_w = [width * w for w in weights]
    pad_x = 5 if compact else 7
    pad_y = 3 if compact else 5

    data = []
    if headers and not hide_header:
        data.append([Paragraph(rich_to_rl(h) if h else " ", styles["cell_head"]) for h in headers])
    for row in rows:
        cells = []
        for i in range(n):
            val = row[i] if i < len(row) else ""
            style = cell_style_for(headers, i, styles, emphasis, audio_cols=audio_set, compact=compact)
            cells.append(Paragraph(rich_to_rl(str(val)), style))
        data.append(cells)

    repeat = 0 if hide_header or not headers else 1
    t = Table(data, colWidths=col_w, repeatRows=repeat)
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), pad_x),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad_x),
        ("TOPPADDING", (0, 0), (-1, -1), pad_y),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad_y),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
    ]
    start_body = 0
    if headers and not hide_header:
        style_cmds.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), TEAL_DARK),
                ("FONTNAME", (0, 0), (-1, 0), "Verdana-Bold"),
            ]
        )
        start_body = 1
    for i in range(start_body, len(data)):
        if (i - start_body) % 2 == 1:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), CARD))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), colors.white))
    t.setStyle(TableStyle(style_cmds))
    t.hAlign = "LEFT"
    return t


def pair_table(items, styles, width):
    data = []
    for es, en in items:
        data.append(
            [
                Paragraph(rich_to_rl(es), styles["pair_es"]),
                Paragraph(rich_to_rl(en), styles["pair_en"]),
            ]
        )
    t = Table(data, colWidths=[width * 0.52, width * 0.48])
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ]
    t.setStyle(TableStyle(cmds))
    t.hAlign = "LEFT"
    return t


def render_block_pdf(block, styles, width, compact=False):
    btype = block["type"]
    bits = []
    if btype == "p":
        bits.append(Paragraph(rich_to_rl(block["text"]), styles["body"]))
    elif btype == "h2":
        bits.append(Paragraph(rich_to_rl(block["text"]), styles["h2_compact"] if compact else styles["h2"]))
    elif btype == "tip":
        inner = [
            Paragraph(xml_escape(block["title"]), styles["tip_title"]),
            Paragraph(rich_to_rl(block["text"]), styles["tip_body"]),
        ]
        bits.append(Spacer(1, 6))
        bits.append(box_table(inner, TIP_BG, TEAL, width))
        bits.append(Spacer(1, 8))
    elif btype == "panama":
        inner = [
            Paragraph(xml_escape(block["title"]), styles["panama_title"]),
            Paragraph(rich_to_rl(block["text"]), styles["tip_body"]),
        ]
        bits.append(Spacer(1, 6))
        bits.append(box_table(inner, PANAMA_BG, GOLD, width))
        bits.append(Spacer(1, 8))
    elif btype == "callout":
        inner = [
            Paragraph(xml_escape(block["title"]), styles["tip_title"]),
            Paragraph(rich_to_rl(block["text"]), styles["tip_body"]),
        ]
        bits.append(Spacer(1, 6))
        bits.append(box_table(inner, SAND, GOLD, width))
        bits.append(Spacer(1, 8))
    elif btype == "ul":
        items = []
        for item in block["items"]:
            items.append(ListItem(Paragraph(rich_to_rl(item), styles["list"]), leftIndent=12, bulletColor=TEAL))
        bits.append(
            ListFlowable(
                items,
                bulletType="bullet",
                start="•",
                leftIndent=18,
                bulletFontName="Georgia",
                bulletFontSize=11,
                spaceBefore=2,
                spaceAfter=8,
            )
        )
    elif btype == "ol":
        if block.get("title"):
            bits.append(Paragraph(xml_escape(block["title"]), styles["h2"]))
        items = []
        for item in block["items"]:
            items.append(ListItem(Paragraph(rich_to_rl(item), styles["list"]), leftIndent=14, bulletColor=TEAL))
        bits.append(
            ListFlowable(
                items,
                bulletType="1",
                leftIndent=20,
                bulletFontName="Verdana-Bold",
                bulletFontSize=10,
                spaceBefore=2,
                spaceAfter=8,
            )
        )
    elif btype == "table":
        bits.append(
            make_grid(
                block["headers"],
                block["rows"],
                styles,
                width,
                emphasis=block.get("emphasis", "first"),
                hide_header=block.get("hide_header", False),
                audio_cols=resolve_audio_cols(block),
                compact=compact,
            )
        )
        bits.append(Spacer(1, 6 if compact else 10))
    elif btype == "pairs":
        if block.get("title"):
            bits.append(Paragraph(xml_escape(block["title"]), styles["h2"]))
        bits.append(pair_table(block["items"], styles, width))
        bits.append(Spacer(1, 6 if compact else 10))
    elif btype == "phrases":
        bits.append(
            make_grid(
                block["columns"],
                block["rows"],
                styles,
                width,
                audio_cols=resolve_audio_cols(block),
                compact=compact,
            )
        )
        bits.append(Spacer(1, 6 if compact else 10))
    elif btype == "note":
        note_text = rich_to_rl(block["text"].replace("\n\n", "<br/><br/>").replace("\n", "<br/>"))
        inner = [Paragraph(note_text, styles["note"])]
        bits.append(Spacer(1, 4))
        bits.append(box_table(inner, CARD, TEAL, width))
        bits.append(Spacer(1, 8))
    return bits


def draw_cover(canvas, doc):
    w, h = letter
    canvas.saveState()
    canvas.setFillColor(TEAL_DARK)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # cream panel
    canvas.setFillColor(PAPER)
    canvas.roundRect(0.55 * inch, 0.55 * inch, w - 1.1 * inch, h - 1.1 * inch, 8, fill=1, stroke=0)
    # teal header block
    canvas.setFillColor(TEAL)
    canvas.rect(0.55 * inch, h - 4.35 * inch, w - 1.1 * inch, 3.25 * inch, fill=1, stroke=0)
    # gold rule
    canvas.setFillColor(GOLD)
    canvas.rect(0.55 * inch, h - 4.42 * inch, w - 1.1 * inch, 0.07 * inch, fill=1, stroke=0)

    canvas.setFillColor(colors.HexColor("#E8DCC8"))
    canvas.setFont("Verdana", 10)
    canvas.drawCentredString(w / 2, h - 1.55 * inch, "A KITCHEN-TABLE GUIDE")

    canvas.setFillColor(colors.white)
    canvas.setFont("Georgia-Bold", 32)
    canvas.drawCentredString(w / 2, h - 2.22 * inch, "Essential")
    canvas.drawCentredString(w / 2, h - 2.75 * inch, "Spanish")

    canvas.setFont("Georgia-Italic", 12)
    canvas.setFillColor(SAND)
    canvas.drawCentredString(w / 2, h - 3.35 * inch, "For English-speaking retirees")
    canvas.drawCentredString(w / 2, h - 3.58 * inch, "living in Panama")

    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1)
    canvas.line(2.4 * inch, h - 5.15 * inch, w - 2.4 * inch, h - 5.15 * inch)

    canvas.setFillColor(TEAL_DARK)
    canvas.setFont("Georgia-Italic", 16)
    canvas.drawCentredString(w / 2, h - 5.6 * inch, TAGLINE)

    canvas.setFont("Georgia", 11.5)
    canvas.setFillColor(INK_SOFT)
    lines = [
        "Not a textbook. A practical booklet you can keep on the table,",
        "open at the farmacia, and sneak a look at in the taxi.",
        "",
        "Latin American Spanish  ·  Usted-friendly  ·  Panama examples",
    ]
    y = h - 6.25 * inch
    for line in lines:
        canvas.drawCentredString(w / 2, y, line)
        y -= 18

    # decorative waves
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.4)
    y_wave = 1.35 * inch
    path = canvas.beginPath()
    path.moveTo(1.1 * inch, y_wave)
    x = 1.1 * inch
    while x < w - 1.1 * inch:
        path.curveTo(x + 18, y_wave + 7, x + 36, y_wave - 7, x + 54, y_wave)
        x += 54
    canvas.drawPath(path, stroke=1, fill=0)
    canvas.setStrokeColor(GOLD)
    path2 = canvas.beginPath()
    y_wave2 = 1.18 * inch
    path2.moveTo(1.1 * inch, y_wave2)
    x = 1.1 * inch
    while x < w - 1.1 * inch:
        path2.curveTo(x + 18, y_wave2 - 6, x + 36, y_wave2 + 6, x + 54, y_wave2)
        x += 54
    canvas.drawPath(path2, stroke=1, fill=0)

    canvas.setFillColor(TEAL)
    canvas.setFont("Verdana", 8)
    canvas.drawCentredString(w / 2, 0.78 * inch, "Keep it close. Use what you need. Nobody is giving you a quiz.")
    canvas.bookmarkPage("cover")
    try:
        canvas.addOutlineEntry("Cover", "cover", level=0, closed=False)
    except ValueError:
        pass
    canvas.restoreState()


def draw_body_page(canvas, doc):
    w, h = letter
    canvas.saveState()
    # cream background
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # top bar
    canvas.setFillColor(TEAL)
    canvas.rect(0, h - 0.38 * inch, w, 0.38 * inch, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, h - 0.44 * inch, w, 0.06 * inch, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Verdana", 8)
    canvas.drawString(0.7 * inch, h - 0.25 * inch, "ESSENTIAL SPANISH")
    canvas.drawRightString(w - 0.7 * inch, h - 0.25 * inch, "Life in Panama")
    # footer
    canvas.setFillColor(SAND)
    canvas.rect(0, 0, w, 0.48 * inch, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0.48 * inch, w, 0.035 * inch, fill=1, stroke=0)
    canvas.setFillColor(TEAL_DARK)
    canvas.setFont("Verdana", 8)
    canvas.drawString(0.7 * inch, 0.22 * inch, "A friendly booklet for retirees in Panama")
    canvas.drawRightString(w - 0.7 * inch, 0.22 * inch, str(doc.page))
    canvas.restoreState()


def draw_toc_page(canvas, doc):
    draw_body_page(canvas, doc)


class SectionMarker(Flowable):
    """Zero-size marker: PDF page number, bookmark, and outline entry."""

    def __init__(self, sid, title):
        Flowable.__init__(self)
        self.sid = sid
        self.title = title

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        canv = self.canv
        SECTION_PAGES[self.sid] = canv.getPageNumber()
        canv.bookmarkPage(self.sid)
        try:
            canv.addOutlineEntry(self.title, self.sid, level=0, closed=False)
        except ValueError:
            pass


FOLLOW_H2 = {"table", "pairs", "phrases"}
KEEP_TYPES = {"table", "pairs", "phrases", "tip", "panama", "callout", "note"}


def group_pdf_blocks(blocks):
    groups = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        if b["type"] == "h2":
            group = [b]
            j = i + 1
            if j < n and blocks[j]["type"] == "p":
                group.append(blocks[j])
                j += 1
            if j < n and blocks[j]["type"] in FOLLOW_H2:
                group.append(blocks[j])
                groups.append(group)
                i = j + 1
                continue
        groups.append([b])
        i += 1
    return groups


def build_pdf():
    os.makedirs(DOCS_DIR, exist_ok=True)
    SECTION_PAGES.clear()
    _write_pdf(BytesIO())
    return _write_pdf(PDF_PATH)


def _write_pdf(dest):
    register_fonts()
    styles = make_styles()
    margin_l = 0.7 * inch
    margin_r = 0.7 * inch
    margin_t = 0.7 * inch
    margin_b = 0.7 * inch
    width = letter[0] - margin_l - margin_r

    doc = BaseDocTemplate(
        dest,
        pagesize=letter,
        leftMargin=margin_l,
        rightMargin=margin_r,
        topMargin=margin_t,
        bottomMargin=margin_b,
        title=TITLE,
        author="Essential Spanish",
        subject=SUBTITLE,
    )
    cover_frame = Frame(0, 0, letter[0], letter[1], id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    body_frame = Frame(margin_l, margin_b, width, letter[1] - margin_t - margin_b, id="body")
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=cover_frame, onPage=draw_cover),
            PageTemplate(id="body", frames=body_frame, onPage=draw_body_page),
        ]
    )

    story = [NextPageTemplate("body"), PageBreak()]

    # TOC
    story.append(SectionMarker("contents", "Contents"))
    story.append(Paragraph("CONTENTS", styles["kicker"]))
    story.append(Paragraph("What's inside", styles["h1"]))
    story.append(
        Paragraph(
            "Skip around. The booklet is built for looking things up, not for reading cover to cover.",
            styles["intro"],
        )
    )
    toc_rows = []
    page_col = 0.5 * inch
    for sec in SECTIONS:
        page_no = SECTION_PAGES.get(sec["id"])
        toc_rows.append(
            [
                Paragraph(xml_escape(sec["kicker"]), styles["toc_kicker"]),
                Paragraph(xml_escape(sec["title"]), styles["toc_item"]),
                Paragraph(str(page_no) if page_no else "00", styles["toc_page"]),
            ]
        )
    toc = Table(toc_rows, colWidths=[1.55 * inch, width - 1.55 * inch - page_col, page_col])
    toc.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (2, 0), (2, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
            ]
        )
    )
    story.append(toc)
    story.append(PageBreak())

    for sec in SECTIONS:
        compact = bool(sec.get("compact"))
        if sec.get("newpage"):
            story.append(PageBreak())
        header = [
            Paragraph(xml_escape(sec["kicker"].upper()), styles["kicker"]),
            Paragraph(xml_escape(sec["title"]), styles["h1"]),
        ]
        if sec.get("intro"):
            header.append(Paragraph(rich_to_rl(sec["intro"]), styles["intro"]))
        groups = group_pdf_blocks(list(sec["blocks"]))
        story.append(CondPageBreak(2.2 * inch))
        first_flow = []
        rest_groups = groups
        if groups:
            for block in groups[0]:
                first_flow.extend(render_block_pdf(block, styles, width, compact=compact))
            rest_groups = groups[1:]
        story.append(KeepTogether([SectionMarker(sec["id"], sec["title"])] + header + first_flow))
        for group in rest_groups:
            flow = []
            for block in group:
                flow.extend(render_block_pdf(block, styles, width, compact=compact))
            keep = len(group) > 1 or group[0]["type"] in KEEP_TYPES
            if keep:
                story.append(KeepTogether(flow))
            else:
                story.extend(flow)
        story.append(Spacer(1, 4 if compact else 8))

    doc.build(story)
    return dest if isinstance(dest, str) else None


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

CSS = r"""
:root {
  --paper: #f6f0e6;
  --ink: #1a2424;
  --ink-soft: #3a4747;
  --teal: #0c5f5f;
  --teal-dark: #084848;
  --coral: #b94a3c;
  --sand: #e8dcc8;
  --gold: #a67c2d;
  --card: #fffbf5;
  --tip: #e4f1ee;
  --panama: #f8e6d8;
  --rule: #cdbfa8;
  --header-bg: #dcecea;
  --shadow: 0 10px 30px rgba(26, 36, 36, 0.08);
  --radius: 14px;
  --max: 46rem;
  --sidebar: 16.5rem;
}
* { box-sizing: border-box; }
html { font-size: 18px; scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Georgia, "Palatino Linotype", Palatino, "Times New Roman", serif;
  color: var(--ink);
  background: var(--paper);
  line-height: 1.6;
}
a { color: var(--teal); }
a:focus-visible, button:focus-visible {
  outline: 3px solid var(--gold);
  outline-offset: 2px;
}
.skip {
  position: absolute; left: -999px; top: 0;
  background: var(--teal); color: white; padding: 0.6rem 1rem;
}
.skip:focus { left: 0.5rem; top: 0.5rem; z-index: 50; }
.hero {
  background: var(--teal-dark);
  color: white;
  padding: 0 1.25rem 3rem;
  position: relative;
  overflow: hidden;
}
.hero-inner {
  max-width: 52rem;
  margin: 0 auto;
  padding-top: 4.5rem;
  text-align: center;
}
.hero .eyebrow {
  font-family: Verdana, Geneva, sans-serif;
  letter-spacing: 0.16em;
  font-size: 0.78rem;
  color: var(--sand);
  text-transform: uppercase;
  margin: 0 0 1rem;
}
.hero h1 {
  font-size: clamp(2.2rem, 6vw, 3.4rem);
  line-height: 1.1;
  margin: 0 0 0.6rem;
  font-weight: 700;
}
.hero .sub {
  font-style: italic;
  font-size: 1.15rem;
  color: var(--sand);
  margin: 0 0 1.4rem;
}
.hero .tag {
  display: inline-block;
  border-top: 1px solid var(--gold);
  border-bottom: 1px solid var(--gold);
  padding: 0.7rem 1.2rem;
  font-size: 1.15rem;
  font-style: italic;
}
.hero p.lead {
  max-width: 36rem;
  margin: 1.4rem auto 0;
  color: #e8dcc8;
  font-size: 1.02rem;
}
.waves {
  height: 42px;
  width: 100%;
  display: block;
  margin-top: 2rem;
}
.toolbar {
  position: fixed;
  top: 0.7rem;
  right: 0.7rem;
  z-index: 40;
  display: flex;
  gap: 0.35rem;
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: 999px;
  padding: 0.25rem;
  box-shadow: var(--shadow);
}
.toolbar button {
  font-family: Verdana, Geneva, sans-serif;
  border: 0;
  background: transparent;
  color: var(--teal-dark);
  min-width: 2.6rem;
  min-height: 2.6rem;
  border-radius: 999px;
  font-size: 0.95rem;
  cursor: pointer;
}
.toolbar button:hover { background: var(--header-bg); }
.layout {
  display: grid;
  grid-template-columns: var(--sidebar) minmax(0, 1fr);
  gap: 1.5rem;
  max-width: 72rem;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 4rem;
}
nav.toc {
  position: sticky;
  top: 4.2rem;
  align-self: start;
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: var(--radius);
  padding: 1rem 0.9rem 1.1rem;
  max-height: calc(100vh - 5rem);
  overflow: auto;
  box-shadow: var(--shadow);
}
nav.toc h2 {
  font-family: Verdana, Geneva, sans-serif;
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--coral);
  margin: 0 0 0.7rem;
}
nav.toc ol { list-style: none; margin: 0; padding: 0; }
nav.toc li { margin: 0; }
nav.toc a {
  display: block;
  text-decoration: none;
  color: var(--teal-dark);
  padding: 0.32rem 0.4rem;
  border-radius: 8px;
  font-size: 0.92rem;
  line-height: 1.3;
}
nav.toc a:hover, nav.toc a.current { background: var(--header-bg); }
nav.toc a.current { font-weight: 700; }
nav.toc .k {
  display: block;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 0.68rem;
  color: var(--coral);
  letter-spacing: 0.04em;
}
.toc-mobile { display: none; }
main { min-width: 0; max-width: 48rem; }
section.chapter {
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: var(--radius);
  padding: 1.4rem 1.4rem 1.5rem;
  margin: 0 0 1.25rem;
  box-shadow: var(--shadow);
}
.kicker {
  font-family: Verdana, Geneva, sans-serif;
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--coral);
  margin: 0 0 0.35rem;
}
h2.chapter-title {
  font-size: 1.85rem;
  line-height: 1.2;
  color: var(--teal-dark);
  margin: 0 0 0.6rem;
}
.intro {
  font-style: italic;
  color: var(--ink-soft);
  font-size: 1.05rem;
  margin: 0 0 1rem;
}
h3 {
  font-size: 1.2rem;
  color: var(--teal);
  margin: 1.3rem 0 0.5rem;
}
p { margin: 0 0 0.85rem; }
span[lang="es"], td[lang="es"], .es {
  color: var(--teal-dark);
  font-weight: 700;
}
.audio-hint {
  background: var(--tip);
  border: 1px solid var(--rule);
  border-left: 6px solid var(--teal);
  border-radius: 12px;
  padding: 0.85rem 1rem;
  margin: 0 0 1.15rem;
  font-size: 1.05rem;
}
.audio-hint code {
  font-family: Verdana, Geneva, sans-serif;
  font-size: 0.9em;
}
.say {
  display: inline-flex;
  align-items: flex-start;
  gap: 0.45rem;
  max-width: 100%;
}
.say-group {
  display: inline-flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 0.35rem 0.2rem;
  max-width: 100%;
}
.slash {
  color: var(--ink-soft);
  font-weight: 400;
  padding: 0.55rem 0.05rem 0;
}
button.play {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.55rem;
  height: 1.55rem;
  min-width: 1.55rem;
  min-height: 1.55rem;
  margin: 0.15rem 0 0;
  padding: 0;
  border: 0;
  border-radius: 999px;
  background: var(--teal);
  color: #fff;
  cursor: pointer;
  line-height: 1;
}
button.play:hover { background: var(--teal-dark); }
button.play.playing { background: var(--coral); }
td[lang="es"] .say, .pairs .es .say { width: 100%; }
.box {
  border-radius: 12px;
  padding: 0.9rem 1rem 0.95rem;
  margin: 0.9rem 0 1rem;
  border: 1px solid var(--rule);
  border-left-width: 6px;
}
.box h4 {
  font-family: Verdana, Geneva, sans-serif;
  font-size: 0.85rem;
  margin: 0 0 0.35rem;
}
.tip { background: var(--tip); border-left-color: var(--teal); }
.tip h4 { color: var(--teal-dark); }
.panama { background: var(--panama); border-left-color: var(--gold); }
.panama h4 { color: #7a3e16; }
.callout { background: var(--sand); border-left-color: var(--gold); }
.callout h4 { color: var(--teal-dark); }
.note {
  background: var(--paper);
  border: 1px dashed var(--teal);
  border-radius: 12px;
  padding: 1rem 1.1rem;
  white-space: pre-wrap;
  font-size: 0.98rem;
  margin: 0.8rem 0 1rem;
}
table.data {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  margin: 0.4rem 0 1rem;
  background: var(--card);
}
table.data th {
  text-align: left;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 0.75rem;
  letter-spacing: 0.03em;
  background: var(--header-bg);
  color: var(--teal-dark);
  padding: 0.5rem 0.6rem;
  border: 1px solid var(--rule);
}
table.data td {
  padding: 0.48rem 0.6rem;
  border: 1px solid var(--rule);
  vertical-align: top;
}
table.data td[lang="es"] { color: var(--teal-dark); font-weight: 700; }
table.data.plain td:first-child { font-weight: 400; color: var(--ink); }
table.data.es-all td { color: var(--teal-dark); font-weight: 700; }
table.data.two-es td:nth-child(1),
table.data.two-es td:nth-child(2) { color: var(--teal-dark); font-weight: 700; }
.pairs {
  width: 100%;
  border-collapse: collapse;
  margin: 0.3rem 0 1rem;
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: 10px;
  overflow: hidden;
}
.pairs td { padding: 0.45rem 0.7rem; border-bottom: 1px solid var(--rule); vertical-align: top; }
.pairs tr:last-child td { border-bottom: 0; }
.pairs .es { width: 52%; }
.pairs .en { font-style: italic; color: var(--ink-soft); }
ol.nice, ul.nice { margin: 0.2rem 0 1rem; padding-left: 1.3rem; }
ol.nice li, ul.nice li { margin: 0.3rem 0; }
.sound { font-family: Verdana, Geneva, sans-serif; font-size: 0.82rem; color: var(--ink-soft); }
footer.site {
  max-width: 48rem;
  margin: 0 auto 3rem;
  padding: 0 1.25rem;
  color: var(--ink-soft);
  font-style: italic;
}
@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; padding-top: 1rem; }
  nav.toc { display: none; }
  .toc-mobile { display: block; margin: 1rem 0 1.1rem; }
  .toc-mobile details {
    background: var(--card);
    border: 1px solid var(--rule);
    border-radius: var(--radius);
    padding: 0.4rem 0.8rem 0.6rem;
  }
  .toc-mobile summary {
    font-family: Verdana, Geneva, sans-serif;
    font-size: 0.95rem;
    color: var(--teal-dark);
    cursor: pointer;
    padding: 0.5rem 0;
    min-height: 2.6rem;
  }
  .toc-mobile ol { list-style: none; padding: 0; margin: 0 0 0.4rem; }
  .toc-mobile a { display: block; padding: 0.4rem 0; text-decoration: none; }
  section.chapter { padding: 1.15rem 1rem 1.2rem; }
  table.data, .pairs { font-size: 0.9rem; }
  .hero-inner { padding-top: 5rem; }
}
@media print {
  .toolbar, .skip, .toc-mobile, button.play, .audio-hint { display: none !important; }
  nav.toc { display: none; }
  .layout { display: block; max-width: none; }
  .hero { break-after: page; }
  section.chapter { box-shadow: none; break-inside: auto; }
  h2.chapter-title, h3 { break-after: avoid; }
  body { background: white; }
}
"""

JS = r"""
(function () {
  const root = document.documentElement;
  const key = "es-booklet-type";
  const legacy = localStorage.getItem("es-grammar-type");
  let size = parseInt(localStorage.getItem(key) || legacy || "18", 10);
  if (isNaN(size)) size = 18;
  size = Math.max(18, Math.min(26, size));
  function apply() {
    root.style.fontSize = size + "px";
    localStorage.setItem(key, String(size));
  }
  apply();
  document.getElementById("type-down").addEventListener("click", function () {
    size = Math.max(18, size - 1);
    apply();
  });
  document.getElementById("type-up").addEventListener("click", function () {
    size = Math.min(26, size + 1);
    apply();
  });

  let current = null;
  function idle(btn) {
    if (!btn) return;
    btn.classList.remove("playing");
    btn.setAttribute("aria-pressed", "false");
  }
  function pickVoice() {
    const voices = window.speechSynthesis ? speechSynthesis.getVoices() : [];
    const prefer = ["es-MX", "es-US", "es-419", "es-PA", "es-CR", "es-CO", "es-AR", "es-ES", "es"];
    for (let i = 0; i < prefer.length; i++) {
      const p = prefer[i].toLowerCase();
      for (let j = 0; j < voices.length; j++) {
        const lang = (voices[j].lang || "").replace("_", "-").toLowerCase();
        if (lang === p || lang.indexOf(p) === 0) return voices[j];
      }
    }
    return null;
  }
  function speakFallback(text, btn) {
    if (!window.speechSynthesis) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    const v = pickVoice();
    if (v) u.voice = v;
    u.lang = (v && v.lang) || "es-MX";
    u.rate = 0.88;
    u.onend = function () { idle(btn); current = null; };
    u.onerror = function () { idle(btn); current = null; };
    current = { stop: function () { speechSynthesis.cancel(); }, btn: btn };
    speechSynthesis.speak(u);
  }
  function stopCurrent() {
    if (!current) return;
    try { current.stop(); } catch (e) {}
    idle(current.btn);
    current = null;
  }
  document.addEventListener("click", function (e) {
    const btn = e.target.closest("button.play");
    if (!btn) return;
    if (current && current.btn === btn) {
      stopCurrent();
      return;
    }
    stopCurrent();
    btn.classList.add("playing");
    btn.setAttribute("aria-pressed", "true");
    const src = "audio/" + btn.getAttribute("data-id") + ".mp3";
    const audio = new Audio(src);
    audio.preload = "auto";
    current = {
      stop: function () { audio.pause(); audio.currentTime = 0; },
      btn: btn
    };
    audio.onended = function () { idle(btn); if (current && current.btn === btn) current = null; };
    audio.onerror = function () { speakFallback(btn.getAttribute("data-say") || "", btn); };
    const playPromise = audio.play();
    if (playPromise && playPromise.catch) {
      playPromise.catch(function () { speakFallback(btn.getAttribute("data-say") || "", btn); });
    }
  });
  if (window.speechSynthesis) speechSynthesis.getVoices();

  const tocLinks = document.querySelectorAll("nav.toc a");
  const chapters = document.querySelectorAll("section.chapter");
  if (tocLinks.length && chapters.length && "IntersectionObserver" in window) {
    const byId = {};
    tocLinks.forEach(function (a) {
      const id = (a.getAttribute("href") || "").replace("#", "");
      if (id) byId[id] = a;
    });
    let currentId = null;
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        const id = entry.target.id;
        if (!id || !byId[id]) return;
        if (currentId && byId[currentId]) byId[currentId].classList.remove("current");
        currentId = id;
        byId[id].classList.add("current");
      });
    }, { rootMargin: "-18% 0px -70% 0px", threshold: 0.02 });
    chapters.forEach(function (sec) { io.observe(sec); });
  }
})();
"""


def toc_html():
    items = []
    for sec in SECTIONS:
        items.append(
            "<li><a href=\"#{id}\"><span class=\"k\">{kicker}</span>{title}</a></li>".format(
                id=html_lib.escape(sec["id"]),
                kicker=html_lib.escape(sec["kicker"]),
                title=html_lib.escape(sec["title"]),
            )
        )
    return "<ol>\n" + "\n".join(items) + "\n</ol>"


def table_html(headers, rows, plain_first=False, hide_header=False, extra_cls="", es_cols=1, skip_digits=False, audio_cols=None):
    cls = "data plain" if plain_first else "data"
    if extra_cls:
        cls = f"{cls} {extra_cls}"
    n = len(headers) if headers else (len(rows[0]) if rows else 0)
    if audio_cols is not None:
        es_set = set(audio_cols)
    else:
        es_set = set(range(es_cols))
    thead = ""
    if headers and not hide_header:
        thead = "<thead><tr>" + "".join(f"<th>{rich_to_html(h) if h else ''}</th>" for h in headers) + "</tr></thead>"
    body = []
    for row in rows:
        tds = []
        for i in range(n):
            val = row[i] if i < len(row) else ""
            is_es = i in es_set
            if is_es and str(val).strip():
                inner = play_segments(str(val), always=True, skip_digits=skip_digits)
            else:
                inner = rich_to_html(str(val))
            lang = ' lang="es"' if is_es else ""
            tds.append(f"<td{lang}>{inner}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f'<div style="overflow-x:auto"><table class="{cls}">{thead}<tbody>{"".join(body)}</tbody></table></div>'


def pairs_html(items, skip_digits=False):
    rows = []
    for es, en in items:
        inner = play_segments(es, always=True, skip_digits=skip_digits)
        rows.append(
            f'<tr><td class="es" lang="es">{inner}</td>'
            f'<td class="en">{rich_to_html(en)}</td></tr>'
        )
    return '<table class="pairs">' + "".join(rows) + "</table>"


def phrases_html(columns, rows, skip_digits=False):
    # mark pronunciation column
    thead = "".join(f"<th>{html_lib.escape(h)}</th>" for h in columns)
    body = []
    for row in rows:
        tds = []
        for i, col in enumerate(columns):
            val = row[i] if i < len(row) else ""
            extra = ' class="sound"' if "sound" in col.lower() else ""
            lang = ""
            if i == 0:
                inner = play_segments(str(val), always=True, skip_digits=skip_digits)
                lang = ' lang="es"'
            else:
                inner = rich_to_html(str(val))
            tds.append(f"<td{lang}{extra}>{inner}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return (
        '<div style="overflow-x:auto"><table class="data"><thead><tr>'
        + thead
        + "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table></div>"
    )


def block_html(block, skip_digits=False):
    btype = block["type"]
    if btype == "p":
        return f"<p>{rich_to_html(block['text'])}</p>"
    if btype == "h2":
        return f"<h3>{rich_to_html(block['text'])}</h3>"
    if btype == "tip":
        return (
            f'<aside class="box tip"><h4>{html_lib.escape(block["title"])}</h4>'
            f"<p>{rich_to_html(block['text'])}</p></aside>"
        )
    if btype == "panama":
        return (
            f'<aside class="box panama"><h4>{html_lib.escape(block["title"])}</h4>'
            f"<p>{rich_to_html(block['text'])}</p></aside>"
        )
    if btype == "callout":
        return (
            f'<aside class="box callout"><h4>{html_lib.escape(block["title"])}</h4>'
            f"<p>{rich_to_html(block['text'])}</p></aside>"
        )
    if btype == "ul":
        lis = "".join(f"<li>{rich_to_html(i)}</li>" for i in block["items"])
        return f'<ul class="nice">{lis}</ul>'
    if btype == "ol":
        title = f"<h3>{html_lib.escape(block['title'])}</h3>" if block.get("title") else ""
        lis = "".join(f"<li>{rich_to_html(i)}</li>" for i in block["items"])
        return f'{title}<ol class="nice">{lis}</ol>'
    if btype == "table":
        headers = block["headers"]
        emphasis = block.get("emphasis", "first")
        extra_cls = "es-all" if emphasis == "all" else ("two-es" if emphasis == "two-es" else "")
        audio_cols = resolve_audio_cols(block)
        plain = 0 not in audio_cols
        return table_html(
            headers,
            block["rows"],
            plain_first=plain,
            hide_header=block.get("hide_header", False),
            extra_cls=extra_cls,
            skip_digits=skip_digits,
            audio_cols=audio_cols,
        )
    if btype == "pairs":
        title = f"<h3>{html_lib.escape(block['title'])}</h3>" if block.get("title") else ""
        return title + pairs_html(block["items"], skip_digits=skip_digits)
    if btype == "phrases":
        return phrases_html(block["columns"], block["rows"], skip_digits=skip_digits)
    if btype == "note":
        return f'<pre class="note">{html_lib.escape(block["text"])}</pre>'
    return ""


def build_html():
    UTTERANCES.clear()
    sample = play_wrap(
        "Más despacio, por favor.",
        '<span lang="es">Más despacio, por favor.</span>',
        always=True,
    )
    chapters = []
    for sec in SECTIONS:
        skip_digits = bool(sec.get("tts_skip_digits"))
        blocks = "\n".join(block_html(b, skip_digits=skip_digits) for b in sec["blocks"])
        chapters.append(
            f'''<section class="chapter" id="{html_lib.escape(sec["id"])}">
<p class="kicker">{html_lib.escape(sec["kicker"])}</p>
<h2 class="chapter-title">{html_lib.escape(sec["title"])}</h2>
<p class="intro">{rich_to_html(sec.get("intro") or "")}</p>
{blocks}
</section>'''
        )
    toc = toc_html()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_lib.escape(TITLE)} — Panama</title>
<meta name="description" content="{html_lib.escape(SUBTITLE)}">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#content">Skip to contents</a>
<div class="toolbar" role="group" aria-label="Text size">
  <button type="button" id="type-down" title="Smaller text" aria-label="Smaller text">A−</button>
  <button type="button" id="type-up" title="Larger text" aria-label="Larger text">A+</button>
</div>
<header class="hero">
  <div class="hero-inner">
    <p class="eyebrow">A kitchen-table guide</p>
    <h1>Essential<br>Spanish</h1>
    <p class="sub">For English-speaking retirees living in Panama</p>
    <p class="tag">{html_lib.escape(TAGLINE)}</p>
    <p class="lead">Not a textbook. A practical booklet you can keep on the table,
    open at the farmacia, and sneak a look at in the taxi.</p>
  </div>
  <svg class="waves" viewBox="0 0 1440 42" preserveAspectRatio="none" aria-hidden="true">
    <path fill="#f6f0e6" d="M0,20 C180,40 360,0 540,18 C720,36 900,4 1080,20 C1260,36 1380,10 1440,18 L1440,42 L0,42 Z"></path>
  </svg>
</header>
<div class="layout">
  <nav class="toc" aria-label="Table of contents">
    <h2>Contents</h2>
    {toc}
  </nav>
  <div>
    <div class="toc-mobile">
      <details>
        <summary>Contents — jump to a chapter</summary>
        {toc}
      </details>
    </div>
    <p class="audio-hint">Tap the green speaker next to a Spanish sentence to hear how it sounds.
    Tap it again to stop. Keep the <code>audio</code> folder next to this HTML file.
    Print version: <a href="essential-spanish.pdf">essential-spanish.pdf</a>.
    Try it: {sample}</p>
    <main id="content">
      {''.join(chapters)}
    </main>
    <footer class="site">
      <p>That is enough Spanish to have a life here. The rest is repetition, curiosity,
      and the occasional cafecito with a patient neighbor. Ánimo. You've got this.</p>
    </footer>
  </div>
</div>
<script>{JS}</script>
</body>
</html>
"""
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    return HTML_PATH


def ping_edge_tts() -> None:
    try:
        import edge_tts
    except ImportError as e:
        raise RuntimeError(
            "edge-tts is not installed. python3 -m pip install --user edge-tts"
        ) from e
    voices = asyncio.run(edge_tts.list_voices())
    names = {v.get("ShortName") for v in voices if v.get("ShortName")}
    if TTS_VOICE not in names:
        raise RuntimeError(f"Edge TTS voice {TTS_VOICE!r} is not available.")


async def _edge_save(text: str, dest_mp3: str) -> None:
    import edge_tts

    last_err = None
    tmp = dest_mp3 + ".part"
    for attempt in range(1, TTS_ATTEMPTS + 1):
        try:
            comm = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE)
            await comm.save(tmp)
            if not os.path.exists(tmp) or os.path.getsize(tmp) < 400:
                raise RuntimeError("clip too small")
            os.replace(tmp, dest_mp3)
            return
        except Exception as e:
            last_err = e
            if os.path.exists(tmp):
                os.remove(tmp)
            await asyncio.sleep(min(2 ** attempt, 16))
    raise RuntimeError(f"Edge TTS failed for {text!r}: {last_err}")


def prune_unused_audio(keep_ids):
    if not os.path.isdir(AUDIO_DIR):
        return 0
    removed = 0
    keep = {uid + ".mp3" for uid in keep_ids}
    for name in os.listdir(AUDIO_DIR):
        if not name.endswith(".mp3") or name in keep:
            continue
        os.remove(os.path.join(AUDIO_DIR, name))
        removed += 1
    return removed


def build_audio():
    """Speak each unique Spanish line with Edge TTS and save MP3s."""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    try:
        ping_edge_tts()
    except Exception as e:
        print(f"Edge TTS unavailable ({e}); web page will use the browser voice as a fallback.")
        return 0

    made = 0
    skipped = 0
    failed = 0
    items = sorted(UTTERANCES.items())
    total = len(items)

    async def _run():
        nonlocal made, skipped, failed
        for i, (uid, text) in enumerate(items, 1):
            mp3 = os.path.join(AUDIO_DIR, uid + ".mp3")
            if os.path.exists(mp3) and os.path.getsize(mp3) > 400:
                skipped += 1
            else:
                try:
                    await _edge_save(text, mp3)
                    made += 1
                except Exception as e:
                    print("TTS failed:", uid, text[:70], "—", e)
                    failed += 1
                    if os.path.exists(mp3) and os.path.getsize(mp3) < 400:
                        os.remove(mp3)
            if i % 25 == 0 or i == total:
                print(f"Audio progress: {i}/{total} ({made} new, {skipped} cached, {failed} failed)")

    asyncio.run(_run())
    pruned = prune_unused_audio(UTTERANCES)
    extra = f", pruned {pruned} old" if pruned else ""
    print(
        f"Audio: {made} new, {skipped} cached, {failed} failed, "
        f"{len(UTTERANCES)} clips, model={TTS_MODEL}, voice={TTS_VOICE}, "
        f"rate={TTS_RATE}{extra}"
    )
    return made


def main():
    html_path = build_html()
    build_audio()
    pdf_path = build_pdf()
    print(f"Wrote {html_path}")
    print(f"Wrote {pdf_path}")
    print(f"Audio clips in {AUDIO_DIR}")


if __name__ == "__main__":
    main()
