#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rendu d'une miniature 1280x720 — essai « Atmosphère de Prière ».

Fond : f25-rayures-indigo.jpg (couleur de référence).
Structure empruntée à la vignette fournie : accroche haute, titre serré en deux
lignes avec surlignage en biseau, ligne de rattachement, arc script en accent.
Aucune couleur du modèle n'est reprise : palette reconstruite 60/30/10.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 1280, 720
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# --- Palette reconstruite -------------------------------------------------
# 60 % nuances du fond f25
NUIT = (7, 41, 91)
BLEU = (14, 68, 132)
BLEU_CLAIR = (23, 105, 165)
# 30 % secondaire dérivée du fond (pas de photo d'orateur cette fois)
ACIER = (127, 182, 232)
# 10 % accent
MENTHE = (104, 216, 192)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def cover(im, w, h):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def vgrad(w, h, stops):
    """stops : liste de (position 0-1, (r,g,b,a))"""
    g = Image.new("RGBA", (1, h))
    px = g.load()
    for y in range(h):
        t = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                k = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = tuple(round(c0[j] + (c1[j] - c0[j]) * k) for j in range(4))
                px[0, y] = col
                break
    return g.resize((w, h))


def radial(w, h, center, radius, color, peak):
    """Lueur radiale douce."""
    small = 160
    m = Image.new("L", (small, int(small * h / w)), 0)
    d = ImageDraw.Draw(m)
    cx = center[0] * small / w
    cy = center[1] * small * h / w / h * (small * h / w) / (small * h / w)
    cy = center[1] * (small * h / w) / h
    r = radius * small / w
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=peak)
    m = m.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(60))
    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(m)
    return layer


def text_mask(text, fnt, tracking=0):
    """Masque du texte avec interlettrage manuel."""
    widths = []
    for ch in text:
        widths.append(fnt.getlength(ch))
    asc, desc = fnt.getmetrics()
    total = sum(widths) + tracking * max(0, len(text) - 1)
    m = Image.new("L", (max(1, int(round(total)) + 10), int(asc + desc + 8)), 0)
    d = ImageDraw.Draw(m)
    x = 4
    for ch, cw in zip(text, widths):
        d.text((x, 4), ch, font=fnt, fill=255)
        x += cw + tracking
    return m


def fill_gradient(mask, top, bottom):
    w, h = mask.size
    g = Image.new("RGB", (1, h))
    px = g.load()
    for y in range(h):
        k = y / max(1, h - 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * k) for i in range(3))
    g = g.resize((w, h))
    layer = g.convert("RGBA")
    layer.putalpha(mask)
    return layer


def shear(layer, angle_deg, pad=90):
    """Italique synthétique (cisaillement vers la droite)."""
    w, h = layer.size
    b = -math.tan(math.radians(angle_deg))
    canvas = Image.new("RGBA", (w + pad, h + 20), (0, 0, 0, 0))
    canvas.paste(layer, (pad // 2, 10))
    out = canvas.transform(
        canvas.size,
        Image.AFFINE,
        (1, b, -b * (h + 10) * 0.5, 0, 1, 0),
        resample=Image.BICUBIC,
    )
    return out


def drop(layer, blur, alpha, offset, color=(0, 0, 0)):
    sh = Image.new("RGBA", (layer.width + 120, layer.height + 120), (0, 0, 0, 0))
    tint = Image.new("RGBA", layer.size, color + (alpha,))
    sh.paste(tint, (60 + offset[0], 60 + offset[1]), layer)
    return sh.filter(ImageFilter.GaussianBlur(blur))


def paste_center(base, layer, cx, cy):
    base.alpha_composite(layer, (round(cx - layer.width / 2), round(cy - layer.height / 2)))


def main(out_path):
    bg = cover(Image.open("fonds/f25-rayures-indigo.jpg").convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.UnsharpMask(radius=2.2, percent=95, threshold=2))

    base = bg.convert("RGBA")

    # --- assombrissement directionnel + vignettage ------------------------
    base.alpha_composite(vgrad(W, H, [
        (0.00, (3, 12, 32, 205)),
        (0.30, (4, 18, 48, 120)),
        (0.55, (4, 18, 48, 60)),
        (0.78, (3, 12, 30, 130)),
        (1.00, (2, 8, 22, 215)),
    ]))
    base.alpha_composite(radial(W, H, (W * 0.5, H * 0.46), W * 0.62, BLEU_CLAIR, 70))

    d = ImageDraw.Draw(base, "RGBA")

    # --- surlignage en biseau (accent 10 %) -------------------------------
    def beamer(y, h, x0, x1, alpha, cut=26):
        d.polygon([
            (x0 + cut, y), (x1, y), (x1 - cut, y + h), (x0, y + h),
        ], fill=MENTHE + (alpha,))

    beam = Image.new("L", (W, H), 0)
    db = ImageDraw.Draw(beam)
    def band(y, h, x0, x1, a, cut=30):
        db.polygon([(x0 + cut, y), (x1, y), (x1 - cut, y + h), (x0, y + h)], fill=a)
    band(252, 62, 40, 1240, 165)
    beam = beam.filter(ImageFilter.GaussianBlur(3.4))
    tint_rgb = Image.new("RGB", (W, H), MENTHE)
    scaled = tint_rgb.convert("RGB")
    scaled = Image.eval(scaled, lambda v: int(v * 0.52))
    scaled.putalpha(beam)
    lit = ImageChops.screen(base.convert("RGB"), scaled.convert("RGB"))
    base = Image.composite(lit.convert("RGBA"), base, beam)
    d = ImageDraw.Draw(base, "RGBA")

    # petit repère haut
    d.polygon([(96, 74), (128, 74), (112, 104)], fill=MENTHE + (215,))
    d.line([(150, 88), (1184, 88)], fill=MENTHE + (70,), width=2)

    # --- titre ------------------------------------------------------------
    f1 = font("DejaVuSerif-Bold.ttf", 116)
    f2 = font("DejaVuSerif-Bold.ttf", 116)

    l1 = shear(fill_gradient(text_mask("ATMOSPHÈRE", f1, 2), (255, 255, 255), (176, 200, 228)), 11)
    l2 = shear(fill_gradient(text_mask("DE PRIÈRE", f2, 2), (255, 255, 255), (176, 200, 228)), 11)

    shadow1 = drop(l1, 22, 95, (6, 9))
    shadow2 = drop(l2, 22, 95, (6, 9))
    paste_center(base, shadow1, W / 2 - 4, 286)
    paste_center(base, shadow2, W / 2 - 4, 438)
    paste_center(base, l1, W / 2, 280)
    paste_center(base, l2, W / 2, 432)

    # --- ligne de rattachement -------------------------------------------
    fs = font("DejaVuSans-Bold.ttf", 31)
    m = text_mask("À ICC PAHOU", fs, 7)
    col = Image.new("RGBA", m.size, MENTHE + (255,))
    col.putalpha(m)
    y = 604
    paste_center(base, col, W / 2, y)
    wl = m.width / 2 + 40
    d.line([(W / 2 - wl - 90, y), (W / 2 - wl, y)], fill=ACIER + (200,), width=2)
    d.line([(W / 2 + wl, y), (W / 2 + wl + 90, y)], fill=ACIER + (200,), width=2)

    out = base.convert("RGB")
    out.save(out_path, quality=93, subsampling=1, optimize=True)
    print("écrit", out_path, out.size)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "livrables/2026-11-07-miniature-atmosphere-de-priere-1280x720.jpg")
