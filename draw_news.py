"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

A broadsheet-style composition: masthead with the date, a lead story on
North Korea (Kim's tactical-nuclear call and the Swiss office expulsion),
four story cards (US markets slide, China's Chen Jining graft probe, the
Gaza strike, Bangladesh's garment pay rise) and a ticker of the day's
other stories. All stories were reported on Thursday 26 November 2026.
Run: python3 draw_news.py — writes entry.png next to this file.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (246, 241, 230)
INK = (26, 26, 26)
RED = (176, 42, 32)
NAVY = (31, 58, 95)
GREY = (110, 108, 100)
CARD = (255, 253, 247)
RULE = (26, 26, 26)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, spacing=5):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_missile(draw, x, y, w, h):
    """Stylised missile climbing over a dark panel with a CLOSED stamp."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # stars
    for sx, sy, r in [(x + 30, y + 26, 2), (x + 90, y + 18, 2),
                      (x + 200, y + 30, 2), (x + 260, y + 20, 2),
                      (x + 150, y + 44, 2), (x + 300, y + 48, 2)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # smoke trail
    for i, r in enumerate([16, 22, 28, 34]):
        cx = x + 70 + i * 26
        cy = y + h - 40 - i * 34
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 200, 205))
    # missile body, angled up-right
    bx, by = x + 120, y + h - 120
    draw.polygon([(bx, by - 52), (bx + 16, by - 18), (bx + 10, by + 26),
                  (bx - 10, by + 26), (bx - 16, by - 18)], fill=(235, 235, 235))
    draw.polygon([(bx, by - 52), (bx + 8, by - 28), (bx - 8, by - 28)],
                 fill=RED)
    draw.polygon([(bx - 10, by + 26), (bx - 30, by + 44), (bx - 10, by + 38)],
                 fill=(235, 235, 235))
    draw.polygon([(bx + 10, by + 26), (bx + 30, by + 44), (bx + 10, by + 38)],
                 fill=(235, 235, 235))
    # flame
    draw.polygon([(bx - 8, by + 28), (bx + 8, by + 28), (bx, by + 62)],
                 fill=(240, 160, 40))
    # CLOSED stamp
    sx0, sy0 = x + w - 140, y + h - 58
    draw.rectangle([sx0, sy0, sx0 + 124, sy0 + 40], outline=RED, width=4)
    draw.text((sx0 + 12, sy0 + 8), "CLOSED", font=font(SANS_B, 24),
              fill=RED)


def icon_chart(draw, x, y, s, color):
    pts = [(x, y + s * 0.3), (x + s * 0.3, y + s * 0.45),
           (x + s * 0.55, y + s * 0.2), (x + s, y + s * 0.75)]
    draw.line(pts, fill=color, width=5, joint="curve")
    draw.polygon([(x + s, y + s * 0.75), (x + s - 12, y + s * 0.75),
                  (x + s, y + s * 0.75 - 12)], fill=color)


def icon_search(draw, x, y, s, color):
    draw.ellipse([x, y, x + s * 0.62, y + s * 0.62], outline=color, width=5)
    draw.line([(x + s * 0.5, y + s * 0.5), (x + s, y + s)], fill=color,
              width=6)


def icon_blast(draw, x, y, s, color):
    pts = []
    for i in range(16):
        r = s * 0.5 if i % 2 == 0 else s * 0.22
        a = math.pi * i / 8 - math.pi / 2
        pts.append((x + s / 2 + r * math.cos(a),
                    y + s / 2 + r * math.sin(a)))
    draw.polygon(pts, fill=color)


def icon_rise(draw, x, y, s, color):
    draw.ellipse([x, y + s * 0.45, x + s * 0.55, y + s], outline=color,
                 width=5)
    draw.text((x + s * 0.08, y + s * 0.58), "%", font=font(SANS_B, 26),
              fill=color)
    draw.line([(x + s * 0.55, y + s * 0.55), (x + s * 0.85, y + s * 0.15)],
              fill=color, width=5)
    draw.line([(x + s * 0.85, y + s * 0.15), (x + s * 0.62, y + s * 0.15)],
              fill=color, width=5)
    draw.line([(x + s * 0.85, y + s * 0.15), (x + s * 0.85, y + s * 0.38)],
              fill=color, width=5)


def card(draw, x, y, w, h, kicker, headline, summary, icon):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=2)
    draw.text((x + 16, y + 12), kicker, font=font(SANS_B, 17), fill=RED)
    icon(draw, x + w - 58, y + 10, 44, NAVY)
    hl = wrap(draw, headline, font(SERIF_B, 25), w - 32)
    yy = text_block(draw, x + 16, y + 40, hl, font(SERIF_B, 25), INK, 2)
    sm = wrap(draw, summary, font(SANS, 19), w - 32)
    text_block(draw, x + 16, yy + 6, sm, font(SANS, 19), (70, 70, 70), 3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # double border
    d.rectangle([14, 14, W - 14, H - 14], outline=RULE, width=3)
    d.rectangle([22, 22, W - 22, H - 22], outline=RULE, width=1)

    # ---- masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 44), title, font=tf, fill=INK)
    sub = "Thursday, 26 November 2026  ·  The day's news in one picture"
    sf = font(SANS, 24)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 122), sub, font=sf, fill=GREY)
    hrule(d, 40, W - 40, 162, 3)
    hrule(d, 40, W - 40, 168, 1)

    # ---- lead story ----
    lx, ly, lw = 40, 186, 944
    d.text((lx, ly), "LEAD STORY  ·  KOREA", font=font(SANS_B, 20), fill=RED)
    head = "KIM PRESSES NUCLEAR BUILD-UP AS PYONGYANG SHUTS SWISS OFFICE"
    hl = wrap(d, head, font(SERIF_B, 36), 560)
    yy = text_block(d, lx, ly + 32, hl, font(SERIF_B, 36), INK, 4)
    body = ("North Korea's leader called for tactical nuclear weapons to be "
            "deployed more widely, state media said Thursday, as Pyongyang "
            "ordered Switzerland to shut its new office and expel its "
            "diplomat within 48 hours.")
    bl = wrap(d, body, font(SANS, 21), 560)
    text_block(d, lx, yy + 10, bl, font(SANS, 21), (60, 60, 60), 5)
    draw_missile(d, lx + 600, ly + 30, 344, 252)
    hrule(d, 40, W - 40, 505, 2)

    # ---- four story cards ----
    cw, ch, gap = 464, 168, 16
    x0, y0 = 40, 522
    card(d, x0, y0, cw, ch, "U.S. MARKETS",
         "MARKETS SLIDE AS TARIFF FEARS SPREAD",
         "Nasdaq falls nearly 4% as Washington's new tariff plan rattles traders.",
         icon_chart)
    card(d, x0 + cw + gap, y0, cw, ch, "CHINA",
         "SHANGHAI PARTY CHIEF UNDER GRAFT PROBE",
         "Xi's anti-corruption drive reaches Politburo member Chen Jining.",
         icon_search)
    card(d, x0, y0 + ch + gap, cw, ch, "GAZA",
         "ISRAELI STRIKE KILLS SENIOR HAMAS OFFICIAL",
         "Airstrike in Gaza kills the official and his family, reports say.",
         icon_blast)
    card(d, x0 + cw + gap, y0 + ch + gap, cw, ch, "BANGLADESH",
         "GARMENT WORKERS WIN 36% PAY RISE",
         "Bangladesh raises the minimum wage for entry-level garment workers.",
         icon_rise)
    hrule(d, 40, W - 40, 890, 2)

    # ---- ticker ----
    d.text((40, 902), "ALSO TODAY", font=font(SANS_B, 20), fill=RED)
    tick1 = ("Sudan drone strikes kill 19  ·  Chinese bomber near Philippines"
             "  ·  Australia–Solomon Islands pact")
    tick2 = ("2,000 migrants reach Canary Islands  ·  Cairo tanker fire "
             "kills 31  ·  US Thanksgiving travel snarls")
    t1 = wrap(d, tick1, font(SANS, 18), 944)
    yy = text_block(d, 40, 930, t1, font(SANS, 18), INK, 4)
    t2 = wrap(d, tick2, font(SANS, 18), 944)
    text_block(d, 40, yy + 2, t2, font(SANS, 18), INK, 4)
    hrule(d, 40, W - 40, 972, 1)
    foot = "Drawn from reports of 26 November 2026  ·  make.fun news-image-20261126"
    ff = font(SANS, 16)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 980), foot, font=ff, fill=GREY)

    img.save(OUT, optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
