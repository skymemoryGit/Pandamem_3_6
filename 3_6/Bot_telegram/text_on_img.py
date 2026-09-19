# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 16:44:04 2023

@author: Ye Jian_cheng

Scrive testo sopra le immagini (meme PandaMem e waifu).
Il testo viene centrato, mandato a capo da solo e rimpicciolito
finche' non entra nello spazio disponibile, qualunque sia la dimensione
dell'immagine di partenza.
"""
import os

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Font incluso nel progetto, cosi' funziona uguale su Windows, Linux e Raspberry
FONT_PATH = os.path.join(BASE_DIR, "font", "BebasKai.ttf")


def _load_font(size):
    """Carica il font del progetto; se manca prova quelli di sistema, poi quello di default."""
    for candidate in (FONT_PATH, "DejaVuSans.ttf", "arial.ttf", "FreeMono"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)   # Pillow >= 10.1
    except TypeError:
        return ImageFont.load_default()


def _wrap_to_width(draw, testo, font, max_w):
    """Manda a capo il testo parola per parola in base alla larghezza reale."""
    righe = []
    for paragrafo in str(testo).split("\n"):
        parole = paragrafo.split()
        if not parole:
            righe.append("")
            continue
        riga = parole[0]
        for parola in parole[1:]:
            prova = riga + " " + parola
            if draw.textlength(prova, font=font) <= max_w:
                riga = prova
            else:
                righe.append(riga)
                riga = parola
        righe.append(riga)
    return "\n".join(righe)


def _fit_text(draw, testo, max_w, max_h, size_max, size_min=12):
    """Trova il font piu' grande con cui il testo entra in (max_w x max_h)."""
    font = _load_font(size_min)
    wrapped = _wrap_to_width(draw, testo, font, max_w)
    for size in range(int(size_max), int(size_min) - 1, -2):
        font = _load_font(size)
        wrapped = _wrap_to_width(draw, testo, font, max_w)
        spacing = max(2, size // 6)
        box = draw.multiline_textbbox((0, 0), wrapped, font=font, align="center", spacing=spacing)
        if (box[2] - box[0]) <= max_w and (box[3] - box[1]) <= max_h:
            return font, wrapped, spacing, box
    spacing = max(2, size_min // 6)
    box = draw.multiline_textbbox((0, 0), wrapped, font=font, align="center", spacing=spacing)
    return font, wrapped, spacing, box


def _draw_centered(draw, testo, font, spacing, box, centro_x, top_y, fill, stroke_w=0, stroke_fill=None):
    """Disegna il testo centrato orizzontalmente su centro_x, partendo da top_y."""
    larghezza = box[2] - box[0]
    x = centro_x - larghezza // 2 - box[0]
    y = top_y - box[1]
    draw.multiline_text(
        (x, y), testo, font=font, fill=fill, align="center", spacing=spacing,
        stroke_width=stroke_w, stroke_fill=stroke_fill,
    )


def creaCustomPandaMeme(img, testo):
    """Prende img e testo e crea img/pandamem/result.png con il testo centrato in alto."""
    im = Image.open(img).convert("RGB")
    draw = ImageDraw.Draw(im)
    W, H = im.size

    testo = str(testo).strip()
    if testo:
        margine = max(8, int(W * 0.05))
        max_w = W - 2 * margine
        max_h = int(H * 0.32)                     # la fascia bianca in alto
        size_max = max(16, int(H * 0.13))

        font, wrapped, spacing, box = _fit_text(draw, testo, max_w, max_h, size_max)
        # contorno bianco: tiene il testo leggibile anche se finisce sul panda
        stroke = max(1, font.size // 22)
        _draw_centered(draw, wrapped, font, spacing, box, W // 2, margine,
                       fill=(0, 0, 0), stroke_w=stroke, stroke_fill=(255, 255, 255))

    im.save(os.path.join(BASE_DIR, "img", "pandamem", "result.png"))


def crea_Image_with_Text(urlsave, img, testo):
    """Scrive il testo in una fascia scura semitrasparente in alto e salva in urlsave."""
    im = Image.open(img).convert("RGBA")
    W, H = im.size

    testo = str(testo).strip()
    if not testo:
        im.convert("RGB").save(urlsave)
        return

    misura = ImageDraw.Draw(im)
    margine = max(12, int(W * 0.05))
    max_w = W - 2 * margine
    max_h = int(H * 0.30)
    size_max = max(20, int(W * 0.09))

    font, wrapped, spacing, box = _fit_text(misura, testo, max_w, max_h, size_max)

    # fascia larga quanto l'immagine, alta quanto serve
    pad = max(10, font.size // 2)
    banda_h = (box[3] - box[1]) + 2 * pad
    banda = Image.new("RGBA", (W, banda_h), (0, 0, 0, 150))
    banda_draw = ImageDraw.Draw(banda)
    _draw_centered(banda_draw, wrapped, font, spacing, box, W // 2, pad,
                   fill=(255, 255, 255, 255))

    im.alpha_composite(banda, (0, max(0, int(H * 0.04))))
    im.convert("RGB").save(urlsave)


if __name__ == "__main__":
    # Test rapido
    base = os.path.join(BASE_DIR, "img", "pandamem", "hhh.png")
    creaCustomPandaMeme(base, "ciao")
    print("creato img/pandamem/result.png")
