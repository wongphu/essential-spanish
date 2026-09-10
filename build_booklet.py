#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Essential Spanish booklet as HTML and PDF."""

from __future__ import annotations

import hashlib
import html as html_lib
import os
import re
import subprocess
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
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
HTML_PATH = os.path.join(ROOT, "index.html")
PDF_PATH = os.path.join(ROOT, "essential-spanish.pdf")
AUDIO_DIR = os.path.join(ROOT, "audio")
# Latin American Spanish, close to what you'll hear in Panama.
TTS_VOICES = ("Eddy (Spanish (Mexico))", "Paulina")
TTS_RATE = "155"

# id -> spoken Spanish, filled while building HTML
UTTERANCES = {}

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
            fontSize=9.5,
            leading=13,
            textColor=INK,
        ),
        "cell_es": ParagraphStyle(
            "cell_es",
            fontName="Georgia-Bold",
            fontSize=9.5,
            leading=13,
            textColor=TEAL_DARK,
        ),
        "cell_head": ParagraphStyle(
            "cell_head",
            fontName="Verdana-Bold",
            fontSize=8,
            leading=11,
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
            fontSize=11,
            leading=15,
            textColor=TEAL_DARK,
        ),
        "pair_en": ParagraphStyle(
            "pair_en",
            fontName="Georgia-Italic",
            fontSize=11,
            leading=15,
            textColor=INK_SOFT,
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


def tts_text(raw: str) -> str:
    """Plain Spanish for the speaker: strip markup, English asides, and slashes."""
    text = ES_TAG.sub(r"\1", raw or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("…", ",")
    text = re.sub(r"\.{3,}", ",", text)
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace(" / ", ", ")
    text = text.replace("/", ", ")
    text = re.sub(r"\s+", " ", text).strip(" ,")
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",\s*,", ",", text)
    return text.strip()


def audio_id(spoken: str) -> str:
    return hashlib.sha1(spoken.encode("utf-8")).hexdigest()[:12]


def register_utterance(raw: str, always: bool = False):
    spoken = tts_text(raw)
    if not spoken or not any(c.isalpha() for c in spoken):
        return None
    if not always and not re.search(r"[\s/¿?¡!.,;]", spoken) and len(spoken) < 8:
        return None
    uid = audio_id(spoken)
    UTTERANCES[uid] = spoken
    return uid, spoken


SPEAKER_SVG = (
    '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">'
    '<path fill="currentColor" d="M3 9v6h4l5 5V4L7 9H3z"/>'
    '<path fill="currentColor" d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>'
    '<path fill="currentColor" d="M14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>'
    "</svg>"
)


def play_wrap(raw: str, inner_html: str, always: bool = False) -> str:
    info = register_utterance(raw, always=always)
    if not info:
        return inner_html
    uid, spoken = info
    label = html_lib.escape("Hear: " + spoken, quote=True)
    say = html_lib.escape(spoken, quote=True)
    return (
        f'<span class="say">'
        f'<button type="button" class="play" data-id="{uid}" data-say="{say}" '
        f'aria-label="{label}" title="{label}">{SPEAKER_SVG}</button>'
        f"{inner_html}</span>"
    )


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


def cell_style_for(headers, col_index, styles, emphasis):
    if emphasis == "all":
        return styles["cell_es"]
    if emphasis == "two-es":
        return styles["cell_es"] if col_index < 2 else styles["cell"]
    if emphasis == "none":
        return styles["cell"]
    first = headers[0] if headers else "Spanish"
    # Label in column 0, Spanish in the rest
    if first in ("Person", ""):
        return styles["cell"] if col_index == 0 else styles["cell_es"]
    # Mixed explainers: first column is the Spanish cue
    if first in ("Use", "Start with", "Pattern", "When"):
        return styles["cell_es"] if col_index == 0 else styles["cell"]
    # Default Spanish-English tables
    if col_index == 0:
        return styles["cell_es"]
    return styles["cell"]


def make_grid(headers, rows, styles, width, emphasis="first", hide_header=False):
    n = len(headers) if headers else (len(rows[0]) if rows else 1)
    if n == 0:
        return Spacer(1, 1)
    if n == 2:
        weights = [0.48, 0.52]
    elif n == 3:
        if emphasis == "two-es":
            weights = [0.32, 0.32, 0.36]
        else:
            weights = [0.34, 0.28, 0.38]
    elif n == 4:
        weights = [0.25, 0.25, 0.25, 0.25]
    elif n == 5:
        weights = [0.24, 0.19, 0.19, 0.19, 0.19]
    else:
        weights = [1 / n] * n
    col_w = [width * w for w in weights]

    data = []
    if headers and not hide_header:
        data.append([Paragraph(rich_to_rl(h) if h else " ", styles["cell_head"]) for h in headers])
    for row in rows:
        cells = []
        for i in range(n):
            val = row[i] if i < len(row) else ""
            style = cell_style_for(headers, i, styles, emphasis)
            cells.append(Paragraph(rich_to_rl(str(val)), style))
        data.append(cells)

    repeat = 0 if hide_header or not headers else 1
    t = Table(data, colWidths=col_w, repeatRows=repeat)
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
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


def render_block_pdf(block, styles, width):
    btype = block["type"]
    bits = []
    if btype == "p":
        bits.append(Paragraph(rich_to_rl(block["text"]), styles["body"]))
    elif btype == "h2":
        bits.append(Paragraph(rich_to_rl(block["text"]), styles["h2"]))
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
            )
        )
        bits.append(Spacer(1, 10))
    elif btype == "pairs":
        if block.get("title"):
            bits.append(Paragraph(xml_escape(block["title"]), styles["h2"]))
        bits.append(pair_table(block["items"], styles, width))
        bits.append(Spacer(1, 10))
    elif btype == "phrases":
        bits.append(make_grid(block["columns"], block["rows"], styles, width))
        bits.append(Spacer(1, 10))
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


def build_pdf():
    register_fonts()
    styles = make_styles()
    margin_l = 0.7 * inch
    margin_r = 0.7 * inch
    margin_t = 0.7 * inch
    margin_b = 0.7 * inch
    width = letter[0] - margin_l - margin_r

    doc = BaseDocTemplate(
        PDF_PATH,
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
    story.append(Paragraph("CONTENTS", styles["kicker"]))
    story.append(Paragraph("What's inside", styles["h1"]))
    story.append(
        Paragraph(
            "Skip around. The booklet is built for looking things up, not for reading cover to cover.",
            styles["intro"],
        )
    )
    toc_rows = []
    for i, sec in enumerate(SECTIONS):
        toc_rows.append(
            [
                Paragraph(xml_escape(sec["kicker"]), styles["toc_kicker"]),
                Paragraph(xml_escape(sec["title"]), styles["toc_item"]),
            ]
        )
    toc = Table(toc_rows, colWidths=[1.55 * inch, width - 1.55 * inch])
    toc.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
            ]
        )
    )
    story.append(toc)
    story.append(PageBreak())

    for sec in SECTIONS:
        if sec.get("newpage"):
            story.append(PageBreak())
        header = [
            Paragraph(xml_escape(sec["kicker"].upper()), styles["kicker"]),
            Paragraph(xml_escape(sec["title"]), styles["h1"]),
        ]
        if sec.get("intro"):
            header.append(Paragraph(rich_to_rl(sec["intro"]), styles["intro"]))
        blocks = list(sec["blocks"])
        first = []
        rest = []
        # keep heading with the first block
        if blocks:
            first = render_block_pdf(blocks[0], styles, width)
            rest_blocks = blocks[1:]
        else:
            rest_blocks = []
        story.append(CondPageBreak(2.2 * inch))
        story.append(KeepTogether(header + first))
        for block in rest_blocks:
            story.extend(render_block_pdf(block, styles, width))
        story.append(Spacer(1, 8))

    doc.build(story)
    return PDF_PATH


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
nav.toc a:hover { background: var(--header-bg); }
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
.say {
  display: inline-flex;
  align-items: flex-start;
  gap: 0.45rem;
  max-width: 100%;
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
table.data td:first-child { color: var(--teal-dark); font-weight: 700; }
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
  section.chapter { box-shadow: none; break-inside: avoid; }
  body { background: white; }
}
"""

JS = r"""
(function () {
  const root = document.documentElement;
  const key = "es-grammar-type";
  let size = parseInt(localStorage.getItem(key) || "18", 10);
  function apply() {
    root.style.fontSize = size + "px";
    localStorage.setItem(key, String(size));
  }
  apply();
  document.getElementById("type-down").addEventListener("click", function () {
    size = Math.max(16, size - 1);
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


def table_html(headers, rows, plain_first=False, hide_header=False, extra_cls="", es_cols=1):
    cls = "data plain" if plain_first else "data"
    if extra_cls:
        cls = f"{cls} {extra_cls}"
    n = len(headers) if headers else (len(rows[0]) if rows else 0)
    thead = ""
    if headers and not hide_header:
        thead = "<thead><tr>" + "".join(f"<th>{rich_to_html(h) if h else ''}</th>" for h in headers) + "</tr></thead>"
    body = []
    for row in rows:
        tds = []
        for i in range(n):
            val = row[i] if i < len(row) else ""
            is_es = i < es_cols
            inner = rich_to_html(str(val))
            if is_es and str(val).strip():
                inner = play_wrap(str(val), inner, always=True)
            lang = ' lang="es"' if is_es else ""
            tds.append(f"<td{lang}>{inner}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f'<div style="overflow-x:auto"><table class="{cls}">{thead}<tbody>{"".join(body)}</tbody></table></div>'


def pairs_html(items):
    rows = []
    for es, en in items:
        inner = play_wrap(es, rich_to_html(es), always=True)
        rows.append(
            f'<tr><td class="es" lang="es">{inner}</td>'
            f'<td class="en">{rich_to_html(en)}</td></tr>'
        )
    return '<table class="pairs">' + "".join(rows) + "</table>"


def phrases_html(columns, rows):
    # mark pronunciation column
    thead = "".join(f"<th>{html_lib.escape(h)}</th>" for h in columns)
    body = []
    for row in rows:
        tds = []
        for i, col in enumerate(columns):
            val = row[i] if i < len(row) else ""
            extra = ' class="sound"' if "sound" in col.lower() else ""
            inner = rich_to_html(str(val))
            lang = ""
            if i == 0:
                inner = play_wrap(str(val), inner, always=True)
                lang = ' lang="es"'
            tds.append(f"<td{lang}{extra}>{inner}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return (
        '<div style="overflow-x:auto"><table class="data"><thead><tr>'
        + thead
        + "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table></div>"
    )


def block_html(block):
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
        plain = headers[0] in ("", "Person", "Letter", "If it ends in…") and emphasis != "all"
        if emphasis == "all":
            es_cols = len(headers)
        elif emphasis == "two-es":
            es_cols = 2
        elif plain:
            es_cols = 0
        else:
            es_cols = 1
        return table_html(
            headers,
            block["rows"],
            plain_first=plain,
            hide_header=block.get("hide_header", False),
            extra_cls=extra_cls,
            es_cols=es_cols,
        )
    if btype == "pairs":
        title = f"<h3>{html_lib.escape(block['title'])}</h3>" if block.get("title") else ""
        return title + pairs_html(block["items"])
    if btype == "phrases":
        return phrases_html(block["columns"], block["rows"])
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
        blocks = "\n".join(block_html(b) for b in sec["blocks"])
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
  <button type="button" id="type-down" title="Smaller text">A−</button>
  <button type="button" id="type-up" title="Larger text">A+</button>
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
    Tap it again to stop. Try it: {sample}</p>
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
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    return HTML_PATH


def build_audio():
    """Speak each unique Spanish line with a Latin American voice and save MP3s."""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    voice = None
    listed = subprocess.run(["say", "-v", "?"], capture_output=True, text=True).stdout
    for candidate in TTS_VOICES:
        if candidate in listed:
            voice = candidate
            break
    if not voice:
        print("No Spanish TTS voice found; web page will use the browser voice as a fallback.")
        return 0
    made = 0
    skipped = 0
    failed = 0

    def one(item):
        uid, text = item
        mp3 = os.path.join(AUDIO_DIR, uid + ".mp3")
        if os.path.exists(mp3) and os.path.getsize(mp3) > 400:
            return "skip"
        aiff = os.path.join("/tmp", "es-booklet-" + uid + ".aiff")
        try:
            subprocess.run(
                ["say", "-v", voice, "-r", TTS_RATE, "-o", aiff, text],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "ffmpeg", "-y", "-loglevel", "error",
                    "-i", aiff,
                    "-codec:a", "libmp3lame", "-q:a", "6",
                    mp3,
                ],
                check=True,
                capture_output=True,
            )
            return "made"
        except subprocess.CalledProcessError:
            print("TTS failed:", uid, text[:70])
            return "fail"
        finally:
            if os.path.exists(aiff):
                os.remove(aiff)

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(one, sorted(UTTERANCES.items())):
            if result == "made":
                made += 1
            elif result == "skip":
                skipped += 1
            else:
                failed += 1
    print(f"Audio: {made} new, {skipped} cached, {failed} failed, {len(UTTERANCES)} clips, voice={voice}")
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
