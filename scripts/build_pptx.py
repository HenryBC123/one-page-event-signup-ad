"""短影音背景簡報：每個主題「標題頁＋重點頁」，橫式 16:9，文字全是可編輯文字框。

用法：python3 build_pptx.py <slides.json> <輸出.pptx> [white]
  加 white＝純白底；不加＝米白底。
  需要 python-pptx：pip3 install --target <暫存資料夾>/py python-pptx，再用 PYTHONPATH 執行。
內容格式見 slides-example.json；文字裡用 <em>…</em> 標重點色、<br> 換行。
做完一定用 Keynote 輸出圖片逐頁檢查（SKILL.md 有指令）。
"""
import json
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

FONT = "PingFang TC"  # Mac 內建；Windows 開會被換字
INK, ACCENT, MUTED, SUB = RGBColor(0x1d, 0x1a, 0x17), RGBColor(0x9a, 0x74, 0x49), RGBColor(0x8a, 0x80, 0x76), RGBColor(0x4a, 0x42, 0x3a)
CARD, LINE = RGBColor(0xff, 0xff, 0xff), RGBColor(0xe6, 0xdc, 0xcb)
px = lambda v: Emu(int(v * 6350))  # 以 1920px 寬設計，1px = 6350 EMU


def text(slide, x, y, w, h, html, size, color=INK, anchor=MSO_ANCHOR.TOP, spacing=None):
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(html.split("<br>")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if spacing:
            p.line_spacing = spacing
        for part in re.split(r"(<em>.*?</em>)", line):
            if not part:
                continue
            r = p.add_run()
            r.text = re.sub(r"</?em>", "", part)
            f = r.font
            f.name, f.size, f.bold = FONT, Pt(size), True
            f.color.rgb = ACCENT if part.startswith("<em>") else color
    return tb


def rect(slide, x, y, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(x), px(y), px(w), px(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def base(prs, bg, i, topic, foot):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = bg
    text(sl, 140, 112, 160, 110, "%02d" % (i + 1), 48, ACCENT)
    pill = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px(282), px(130), px(70 + 48 * len(topic)), px(76))
    pill.adjustments[0] = 0.5
    pill.fill.background()
    pill.line.color.rgb = ACCENT
    pill.line.width = Pt(1.5)
    pill.shadow.inherit = False
    tf = pill.text_frame
    tf.margin_left = tf.margin_right = 0
    r = tf.paragraphs[0].add_run()
    r.text = topic
    r.font.name, r.font.size, r.font.bold = FONT, Pt(20), True
    r.font.color.rgb = ACCENT
    rect(sl, 140, 940, 1640, 1.5, LINE)
    text(sl, 140, 964, 900, 50, foot[0], 15, MUTED)
    t = text(sl, 1000, 964, 780, 50, foot[1], 15, MUTED)
    t.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
    return sl


def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    bg = RGBColor(0xff, 0xff, 0xff) if "white" in sys.argv[3:] else RGBColor(0xfb, 0xf8, 0xf3)
    foot = data["footer"]
    prs = Presentation()
    prs.slide_width, prs.slide_height = px(1920), px(1080)
    for i, tp in enumerate(data["topics"]):
        # 標題頁：大標＋副標（左半邊，右邊留給人入鏡）
        sl = base(prs, bg, i, tp["name"], foot)
        rect(sl, 140, 290, 120, 8, ACCENT)
        text(sl, 140, 340, 1500, 360, tp["title"], 64, INK, spacing=0.95)
        text(sl, 140, 770 if "<br>" in tp["title"] else 600, 1500, 80, tp["sub"], 24, SUB)
        # 重點頁：兩欄三列，每點 ≤11 字
        if tp.get("points"):
            sl = base(prs, bg, i, tp["name"], foot)
            text(sl, 140, 255, 1600, 130, tp["list_title"], 46)
            for j, k in enumerate(tp["points"]):
                x, y = 140 + (j % 2) * 840, 430 + (j // 2) * 158
                rect(sl, x, y, 800, 132, CARD, line=LINE)
                rect(sl, x, y, 6, 132, ACCENT)
                text(sl, x + 40, y, 60, 132, str(j + 1), 23, ACCENT, MSO_ANCHOR.MIDDLE)
                text(sl, x + 122, y, 660, 132, k, 27, INK, MSO_ANCHOR.MIDDLE)
    prs.save(out)
    print("ok", len(prs.slides), "→", out)


main()
