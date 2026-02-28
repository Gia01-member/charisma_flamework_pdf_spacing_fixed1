from flask import Flask, render_template, request, send_file
from io import BytesIO
from datetime import datetime
import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from data.content import QUESTIONS, TYPE_RULES, TYPE_COPY, ROADMAP

app = Flask(__name__)

AXES = ["A", "B", "C", "D"]
MAX_PER_AXIS = 16

# ---- Embed Noto Sans CJK properly (fix Latin spacing) ----
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "NotoSansCJK-Regular.ttc")
PDF_FONT = "NotoSansCJK"

# subfontIndex=0 is critical for proper Latin glyph rendering
pdfmetrics.registerFont(TTFont(PDF_FONT, FONT_PATH, subfontIndex=0))

def build_pdf_bytes():
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    c.setFont(PDF_FONT, 16)
    c.drawString(20*mm, h - 20*mm, "カリスマ性診断レポート（FlameWork）")

    c.setFont(PDF_FONT, 11)
    c.drawString(20*mm, h - 35*mm, "Type: バランス型")
    c.drawString(20*mm, h - 45*mm, "Created: 2026-02-28 02:58")

    c.drawString(20*mm, h - 60*mm, "A: 0 / 16")
    c.drawString(20*mm, h - 70*mm, "B: 0 / 16")
    c.drawString(20*mm, h - 80*mm, "C: 0 / 16")
    c.drawString(20*mm, h - 90*mm, "D: 0 / 16")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf

@app.route("/", methods=["GET"])
def index():
    return "<form action='/pdf' method='post'><button type='submit'>PDF確認</button></form>"

@app.route("/pdf", methods=["POST"])
def pdf():
    buf = build_pdf_bytes()
    return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name="flamework_report.pdf")

if __name__ == "__main__":
    app.run(debug=True)
