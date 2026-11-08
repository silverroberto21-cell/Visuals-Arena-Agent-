#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flyer 1080×1350 — « Les Bonnes nouvelles du royaume » sur **FOND 13 uniquement**.

Le fond f13 (bleu électrique, vagues) n'est pas recouvert d'une image, pas d'un motif, pas
d'un portrait : seuls les voiles de lisibilité et la lumière le travaillent. Le titre fait
tout le visuel.

**Duo de polices du thème (nouveau)** : Cormorant Garamond *Bold* — un Garamond de labeur,
lisible posé sur un fond saturé — + Jost *Medium* (signalétique géométrique, née du Futura).
C'est le premier thème « annonce / évangile » : on quitte Anton (exhortation) et Playfair
(vignette de référence).

Date « négligeable » : elle n'est pas composée. Aucune date, aucune heure inventées.

    python3 scripts/render_bonnes_nouvelles_f13.py livrables/<AAAA-MM-JJ>-flyer-....jpg
"""
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
SIZES = {
    "digital": (1080, 1350),      # 4:5 portrait (feed)
    "a5": (1748, 2480),           # A5 portrait 300 dpi
    "paysage": (1920, 1080),      # 16:9 paysage (screen, projection, bannière)
    "a5-paysage": (2480, 1748),   # A5 paysage 300 dpi (print)
}
# géométrie de la maquette, dans les deux orientations : le titre occupe la même
# proportion de la surface utile, seule la disposition des blocs change.
LAYOUT = {"portrait": dict(ml=96, mt=96, big=172, small_ratio=0.70,
                           block_y=0.54, title_center=True),
          "paysage": dict(ml=132, mt=104, big=196, small_ratio=0.60,
                          block_y=0.50, title_center=True)}
SERIF = "polices/cormorant-garamond-var.ttf"
SANS = "polices/jost-var.ttf"
FOND = "fonds/f13-bleu-nuit-vagues.jpg"

# 60 % — nuances mesurées sur f13
BLEU = (1, 85, 251)
AZUR = (1, 130, 254)
NUIT = (1, 27, 208)
# 30 % — secondaire
BLANC = (247, 250, 255)
# 10 % — accent
OR = (240, 205, 130)

TITRE = "Les Bonnes nouvelles du royaume"

M = 96          # marge de sécurité (specs : 72 px mini en 1080×1350)


def font(path, size, variation=None):
    f = ImageFont.truetype(path, size)
    if variation:
        f.set_variation_by_name(variation)
    return f


def cover(im, w, h):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


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


def radial(w, h, cx, cy, r, color, peak, blur=110):
    small = 220
    sh = int(small * h / w)
    m = Image.new("L", (small, sh), 0)
    ImageDraw.Draw(m).ellipse([cx * small / w - r * small / w, cy * sh / h - r * sh / h,
                               cx * small / w + r * small / w, cy * sh / h + r * sh / h],
                              fill=peak)
    m = m.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(blur))
    lay = Image.new("RGBA", (w, h), color + (0,))
    lay.putalpha(m)
    return lay


def text_mask(text, fnt, tracking=0):
    widths = [fnt.getlength(c) for c in text]
    asc, desc = fnt.getmetrics()
    total = sum(widths) + tracking * max(0, len(text) - 1)
    m = Image.new("L", (max(1, int(round(total)) + 24), int(asc + desc + 30)), 0)
    d = ImageDraw.Draw(m)
    x = 12
    for c, cw in zip(text, widths):
        d.text((x, 14), c, font=fnt, fill=255)
        x += cw + tracking
    return m


def fill_gradient(mask, top, bottom):
    w, h = mask.size
    g = Image.new("RGB", (1, h))
    px = g.load()
    for y in range(h):
        k = y / max(1, h - 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * k) for i in range(3))
    lay = g.resize((w, h)).convert("RGBA")
    lay.putalpha(mask)
    return lay


def drop(layer, blur, alpha, offset, color=(0, 0, 0)):
    sh = Image.new("RGBA", (layer.width + 200, layer.height + 200), (0, 0, 0, 0))
    tint = Image.new("RGBA", layer.size, color + (alpha,))
    sh.paste(tint, (100 + offset[0], 100 + offset[1]), layer)
    return sh.filter(ImageFilter.GaussianBlur(blur))


def paste(base, layer, x, y, anchor="left"):
    bb = layer.getbbox()
    if bb is None:
        return
    if anchor == "center":
        x -= (bb[0] + bb[2]) / 2
    base.alpha_composite(layer, (round(x - bb[0]), round(y - bb[1])))


def wrap(fnt, text, target_w, tracking=0):
    """Découpe en lignes qui tiennent dans target_w (respecte les mots)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        width = fnt.getlength(cand) + tracking * (len(cand) - 1)
        if width <= target_w or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main(out, fond=FOND, size="digital"):
    w, h = SIZES[size]
    portrait = h > w
    L = LAYOUT["portrait" if portrait else "paysage"]
    k = h / 1350.0 if portrait else h / 1080.0   # échelle : la hauteur porte le corps
    W, H = w, h
    M = round(L["ml"] * (w / (1080.0 if portrait else 1920.0)))
    MT = round(L["mt"] * k)
    bg = cover(Image.open(fond).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.6))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=60, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.86)))

    base = bg.convert("RGBA")
    # lisibilité : haut et bas assombris, le centre garde son bleu vif
    base.alpha_composite(vgrad(W, H, [
        (0.00, (2, 10, 60, 150)),
        (0.22, (2, 12, 62, 70)),
        (0.50, (2, 12, 62, 26)),
        (0.78, (2, 10, 55, 96)),
        (1.00, (1, 6, 40, 205)),
    ]))
    base.alpha_composite(radial(W, H, W * 0.5, H * 0.46, W * 0.72, (150, 200, 255), 26, 160))
    base.alpha_composite(radial(W, H, M + 40, 250, 230, OR, 26, 120))

    d = ImageDraw.Draw(base, "RGBA")

    # ---------- filet de cadre intérieur (structure, pas un ornement)
    c = round(70 * k)
    d.line([(M, MT), (M + c, MT)], fill=OR + (225,), width=max(2, round(3 * k)))
    d.line([(M, MT), (M, MT + c)], fill=OR + (225,), width=max(2, round(3 * k)))
    d.line([(W - M - c, MT), (W - M, MT)], fill=OR + (225,), width=max(2, round(3 * k)))
    d.line([(W - M, MT), (W - M, MT + c)], fill=OR + (225,), width=max(2, round(3 * k)))

    # ---------- accroche
    fk = font(SANS, round(23 * k), "Medium")
    mk = text_mask("ICC PAHOU", fk, 9)
    col = Image.new("RGBA", mk.size, (238, 244, 255, 240))
    col.putalpha(mk)
    paste(base, col, M + round(30 * k), MT + round(36 * k))

    # ---------- titre
    if portrait:
        # portrait : trois lignes centrées, « royaume » d'un corps plus petit
        big_w = W - 2 * M - round(40 * k)
        f_big = font(SERIF, round(L["big"] * k), "Bold")
        while f_big.getlength("nouvelles") > big_w and f_big.size > 60:
            f_big = font(SERIF, f_big.size - 4, "Bold")
        f_sml = font(SERIF, round(f_big.size * L["small_ratio"]), "Medium")
        print("corps titre :", f_big.size, "/", f_sml.size)

        a_big, a_sml = f_big.getmetrics(), f_sml.getmetrics()
        block = (a_big[0] + a_big[1]) * 2 + (a_sml[0] + a_sml[1]) * 1.16 + round(26 * k)
        y = int((H - block) / 2) + round(74 * k)
        cx = W / 2
        for txt, fnt in (("Les Bonnes", f_big), ("nouvelles", f_big), ("du royaume", f_sml)):
            m = text_mask(txt, fnt, 0)
            lay = fill_gradient(m, (255, 255, 255), (223, 234, 253))
            paste(base, drop(lay, 30, 88, (0, 10)), cx, y + 8, "center")
            paste(base, lay, cx, y, "center")
            y += int(m.getbbox()[3] - m.getbbox()[1]) + round(14 * k)
        line_w, line_y = 150 * k, y + round(6 * k)
    else:
        # paysage : deux lignes centrées, la seconde d'un corps plus petit
        big_w = W - 2 * M - round(60 * k)
        f_big = font(SERIF, round(L["big"] * k), "Bold")
        while f_big.getlength("Les Bonnes nouvelles") > big_w and f_big.size > 60:
            f_big = font(SERIF, f_big.size - 4, "Bold")
        f_sml = font(SERIF, round(f_big.size * L["small_ratio"]), "Medium")
        print("corps titre :", f_big.size, "/", f_sml.size)

        a_big, a_sml = f_big.getmetrics(), f_sml.getmetrics()
        block = (a_big[0] + a_big[1]) + (a_sml[0] + a_sml[1]) * 1.2 + round(26 * k)
        y = int((H - block) / 2) + round(58 * k)
        cx = W / 2
        for txt, fnt in (("Les Bonnes nouvelles", f_big), ("du royaume", f_sml)):
            m = text_mask(txt, fnt, 0)
            lay = fill_gradient(m, (255, 255, 255), (223, 234, 253))
            paste(base, drop(lay, 34 * k / 1.25, 88, (0, 10)), cx, y + 8, "center")
            paste(base, lay, cx, y, "center")
            y += int(m.getbbox()[3] - m.getbbox()[1]) + round(12 * k)
        line_w, line_y = 190 * k, y + round(10 * k)

    # filet or sous le titre
    d.line([(cx - line_w, line_y), (cx + line_w, line_y)], fill=OR + (235,), width=max(2, round(3 * k)))
    r = round(5 * k)
    d.ellipse([cx - r, line_y - r, cx + r, line_y + r], fill=OR + (235,))

    # ---------- pied : filet seul, aucune date, aucun texte inventé
    d.line([(cx - 70 * k, H - MT - round(24 * k)), (cx + 70 * k, H - MT - round(24 * k))],
           fill=OR + (200,), width=max(2, round(2 * k)))

    base.convert("RGB").save(out, quality=95, subsampling=1, optimize=True)
    print("écrit", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else FOND,
         sys.argv[3] if len(sys.argv) > 3 else "digital")
