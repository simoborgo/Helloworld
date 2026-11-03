#!/usr/bin/env python3
"""Calendario settimanale A2 orizzontale (594x420 mm), da scrivere a mano."""
from reportlab.pdfgen import canvas
import os
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("R", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

W, H = 594 * mm, 420 * mm
M = 15 * mm
DAYS = ["LUNEDÌ", "MARTEDÌ", "MERCOLEDÌ", "GIOVEDÌ", "VENERDÌ", "SABATO"]
H0, H1 = 8, 19          # ore 8:00 -> 19:00
INK, GREY, LIGHT = (0.1, 0.1, 0.1), (0.55, 0.55, 0.55), (0.82, 0.82, 0.82)

c = canvas.Canvas("Calendario_settimanale_A2.pdf", pagesize=(W, H))
c.setTitle("Calendario settimanale A2")

# Intestazione
top = H - M
c.setFillColorRGB(*INK)
c.setFont("B", 44)
c.drawString(M, top - 15 * mm, "CALENDARIO SETTIMANALE")
c.setFont("R", 18)
c.drawString(M, top - 27 * mm, "Team:")
c.setStrokeColorRGB(*GREY); c.setLineWidth(0.6)
c.line(M + 18 * mm, top - 28 * mm, M + 130 * mm, top - 28 * mm)
c.drawRightString(W - M - 190 * mm, top - 27 * mm, "Settimana dal")
c.line(W - M - 185 * mm, top - 28 * mm, W - M - 105 * mm, top - 28 * mm)
c.drawString(W - M - 100 * mm, top - 27 * mm, "al")
c.line(W - M - 88 * mm, top - 28 * mm, W - M, top - 28 * mm)

# Logo Modar (se presente: logo_modar.png / .jpg accanto allo script)
here = os.path.dirname(os.path.abspath(__file__))
for ext in ("png", "jpg", "jpeg"):
    lp = os.path.join(here, f"logo_modar.{ext}")
    if os.path.exists(lp):
        img = ImageReader(lp)
        iw, ih = img.getSize()
        lh = 24 * mm
        lw = lh * iw / ih
        if lw > 90 * mm:
            lw, lh = 90 * mm, 90 * mm * ih / iw
        c.drawImage(lp, W - M - lw, top - lh, lw, lh, mask="auto")
        break

# Griglia
gx0, gx1 = M, W - M
gy1 = top - 38 * mm
note_h = 45 * mm
gy0 = M + note_h + 8 * mm
hour_w = 22 * mm
head_h = 14 * mm
ncol = len(DAYS)
col_w = (gx1 - gx0 - hour_w) / ncol
nrows = H1 - H0
row_h = (gy1 - head_h - gy0) / nrows

# Intestazioni giorni
c.setFillColorRGB(*INK)
c.rect(gx0 + hour_w, gy1 - head_h, col_w * ncol, head_h, stroke=0, fill=1)
c.setFillColorRGB(1, 1, 1)
c.setFont("B", 20)
for i, d in enumerate(DAYS):
    c.drawString(gx0 + hour_w + i * col_w + 4 * mm, gy1 - head_h + 4.5 * mm, d)
    c.setFont("R", 12)
    c.drawRightString(gx0 + hour_w + (i + 1) * col_w - 4 * mm, gy1 - head_h + 4.5 * mm, "___ / ___")
    c.setFont("B", 20)

# Righe orarie
top_rows = gy1 - head_h
for r in range(nrows):
    y = top_rows - (r + 1) * row_h
    c.setFillColorRGB(*INK); c.setFont("B", 16)
    c.drawRightString(gx0 + hour_w - 3 * mm, y + row_h - 8 * mm, f"{H0 + r}:00")
    # mezza ora tratteggiata
    c.setStrokeColorRGB(*LIGHT); c.setLineWidth(0.4); c.setDash(2, 3)
    c.line(gx0 + hour_w, y + row_h / 2, gx1, y + row_h / 2)
    c.setDash()
    # linea ora
    c.setStrokeColorRGB(*GREY); c.setLineWidth(0.7)
    c.line(gx0, y, gx1, y)
c.line(gx0, top_rows, gx1, top_rows)

# Pausa pranzo (fascia leggera 13-14)
lunch_r = 13 - H0
c.setFillColorRGB(0.94, 0.94, 0.94)
c.rect(gx0 + hour_w, top_rows - (lunch_r + 1) * row_h, col_w * ncol, row_h, stroke=0, fill=1)
# ridisegna linee e testo per la fascia
c.setStrokeColorRGB(*GREY); c.setLineWidth(0.7)
c.line(gx0, top_rows - lunch_r * row_h, gx1, top_rows - lunch_r * row_h)
c.line(gx0, top_rows - (lunch_r + 1) * row_h, gx1, top_rows - (lunch_r + 1) * row_h)

# Linee verticali
c.setStrokeColorRGB(*INK); c.setLineWidth(1.2)
for i in range(ncol + 1):
    x = gx0 + hour_w + i * col_w
    c.line(x, gy1 - head_h, x, gy0)
c.setLineWidth(1.2)
c.line(gx0, gy1 - head_h, gx0, gy0)
c.line(gx0, gy0, gx1, gy0)

# Note / priorità
ny1 = gy0 - 8 * mm
ny0 = M
c.setStrokeColorRGB(*INK); c.setLineWidth(1.2)
c.rect(gx0, ny0, gx1 - gx0, ny1 - ny0, stroke=1, fill=0)
c.setFillColorRGB(*INK); c.setFont("B", 18)
c.drawString(gx0 + 5 * mm, ny1 - 9 * mm, "NOTE / PRIORITÀ DELLA SETTIMANA")
c.setStrokeColorRGB(*LIGHT); c.setLineWidth(0.5)
y = ny1 - 20 * mm
while y > ny0 + 4 * mm:
    c.line(gx0 + 5 * mm, y, gx1 - 5 * mm, y)
    y -= 10 * mm

c.showPage(); c.save()
