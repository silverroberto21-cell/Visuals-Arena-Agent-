#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reprise de la vignette d'origine sur un autre fond — défaut : FOND 17.

Rien ne bouge sauf la matière : mêmes textes, même police (Playfair Black Italic
+ Montserrat), même disposition que la vignette fournie par ICC Pahou.
Badge de durée non reproduit (interface de plateforme).
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont

W, H = 1280, 720
TITRE_TTF = "polices/playfair-display-italic-var.ttf"
SANS_TTF = "polices/montserrat-var.ttf"

SAGE = (150, 200, 165)          # barres de la vignette d'origine
VIOLET = (58, 59, 143)          # bleu violacé de la vignette


def var_font(path, size, variation):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name(variation)
    except Exception as e:
        print("variation indisponible:", variation, e)
    return f


def cover(im, w, h):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    return im.crop(((im.width - w) // 2, (im.height - h) // 2,
                    (im.width - w) // 2 + w, (im.height - h) // 2 + h))


def vgrad(w, h, stops):
    g = Image.new("RGBA", (1, h))
    px = g.load()
    for y in range(h):
        t = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                k = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                px[0, y] = tuple(round(c0[j] + (c1[j] - c0[j]) * k) for j in range(4))
                break
    return g.resize((w, h))


def text_mask(text, fnt, tracking=0):
    widths = [fnt.getlength(ch) for ch in text]
    asc, desc = fnt.getmetrics()
    total = sum(widths) + tracking * max(0, len(text) - 1)
    m = Image.new("L", (max(1, int(round(total)) + 12), int(asc + desc + 14)), 0)
    d = ImageDraw.Draw(m)
    x = 6
    for ch, cw in zip(text, widths):
        d.text((x, 6), ch, font=fnt, fill=255)
        x += cw + tracking
    return m


def fill(mask, top, bottom):
    w, h = mask.size
    g = Image.new("RGB", (1, h))
    px = g.load()
    for y in range(h):
        k = y / max(1, h - 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * k) for i in range(3))
    layer = g.resize((w, h)).convert("RGBA")
    layer.putalpha(mask)
    return layer


def drop(layer, blur, alpha, offset):
    sh = Image.new("RGBA", (layer.width + 100, layer.height + 100), (0, 0, 0, 0))
    tint = Image.new("RGBA", layer.size, (0, 0, 0, alpha))
    sh.paste(tint, (50 + offset[0], 50 + offset[1]), layer)
    return sh.filter(ImageFilter.GaussianBlur(blur))


def paste_cx_top(base, layer, cx, top):
    bb = layer.getbbox() or (0, 0, layer.width, layer.height)
    x = round(cx - (bb[0] + bb[2]) / 2)
    y = round(top - bb[1])
    base.alpha_composite(layer, (x, y))


def paste_left_top(base, layer, left, top):
    bb = layer.getbbox() or (0, 0, layer.width, layer.height)
    base.alpha_composite(layer, (round(left - bb[0]), round(top - bb[1])))


def main(fond, out, violet=0.32, dark=0.95):
    bg = cover(Image.open(fond).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.UnsharpMask(radius=2.2, percent=95, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * dark)))

    wash = Image.eval(Image.new("RGB", (W, H), VIOLET), lambda v: int(v * 0.55))
    base = Image.blend(bg.convert("RGBA"),
                       ImageChops.screen(bg, wash).convert("RGBA"), violet)

    base.alpha_composite(vgrad(W, H, [
        (0.00, (6, 8, 34, 210)),
        (0.35, (8, 12, 52, 120)),
        (0.62, (8, 12, 52, 40)),
        (1.00, (4, 6, 26, 90)),
    ]))

    # barres sauge de la vignette d'origine, derrière le titre
    bar = Image.new("L", (W, H), 0)
    dbar = ImageDraw.Draw(bar)
    dbar.polygon([(300, 232), (1010, 232), (984, 284), (272, 284)], fill=120)
    dbar.polygon([(330, 336), (1000, 336), (974, 380), (304, 380)], fill=70)
    bar = bar.filter(ImageFilter.GaussianBlur(1.6))
    sage = Image.new("RGBA", (W, H), SAGE + (0,))
    sage.putalpha(bar)
    base.alpha_composite(sage)

    d = ImageDraw.Draw(base, "RGBA")

    # accroche
    fk = var_font(SANS_TTF, 21, "Medium")
    for i, line in enumerate(["ATMOSPHÈRE", "PROPHÉTIQUE"]):
        m = text_mask(line, fk, 4)
        col = Image.new("RGBA", m.size, (236, 240, 252, 235))
        col.putalpha(m)
        paste_left_top(base, col, 336, 148 + i * 30)

    # titre
    ft = var_font(TITRE_TTF, 118, "Black Italic")
    l1 = fill(text_mask("ATMOSPHÈRE", ft, 1), (255, 255, 255), (232, 236, 252))
    l2 = fill(text_mask("DE PRIÈRE", ft, 1), (255, 255, 255), (232, 236, 252))
    paste_cx_top(base, drop(l1, 14, 110, (4, 6)), 640, 232)
    paste_cx_top(base, drop(l2, 14, 110, (4, 6)), 640, 336)
    paste_cx_top(base, l1, 640, 226)
    paste_cx_top(base, l2, 640, 330)

    # sous-titre
    fs = var_font(SANS_TTF, 17, "Light")
    m = text_mask("TEMPS DE PRIÈRE ET D'ADORATION", fs, 6)
    col = Image.new("RGBA", m.size, (236, 241, 252, 210))
    col.putalpha(m)
    paste_cx_top(base, col, 640, 482)

    base.convert("RGB").save(out, quality=93, subsampling=1, optimize=True)
    print("écrit", out)


if __name__ == "__main__":
    fond = sys.argv[1] if len(sys.argv) > 1 else "fonds/f17-bleu-scene-louange.jpg"
    out = sys.argv[2] if len(sys.argv) > 2 else "essais/2026-11-07/reprise-vignette-origine-fond17.jpg"
    main(fond, out)
