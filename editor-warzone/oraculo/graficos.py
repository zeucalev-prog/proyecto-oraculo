"""Gráficos estilo HUD táctico (Pillow). Todo devuelve imágenes RGBA listas para componer."""
import math
import os
import re
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(AQUI, '..', 'fuentes')

NEGRO = (10, 12, 11)
PANEL = (14, 17, 15, 225)
NARANJA = (255, 107, 26)
AMARILLO = (255, 210, 63)
BLANCO = (255, 255, 255)
ROJO = (255, 59, 48)
VERDE = (150, 255, 90)
AZUL = (90, 175, 255)
GRIS = (150, 158, 152)


@lru_cache(maxsize=64)
def fuente(nombre, tam):
    archivo = {'titulo': 'Anton.ttf', 'bebas': 'BebasNeue.ttf', 'negra': 'Montserrat-Black.ttf',
               'bold': 'Montserrat-ExtraBold.ttf', 'mono': 'Mono-Bold.ttf'}[nombre]
    return ImageFont.truetype(os.path.join(FUENTES, archivo), tam)


def medir(txt, f, espaciado=0):
    b = f.getbbox(txt)
    return b[2] - b[0] + espaciado * max(0, len(txt) - 1), b[3] - b[1]


def texto_espaciado(d, xy, txt, f, fill, espaciado=0, **kw):
    if not espaciado:
        d.text(xy, txt, font=f, fill=fill, **kw)
        return
    x, y = xy
    for c in txt:
        d.text((x, y), c, font=f, fill=fill, **kw)
        x += f.getlength(c) + espaciado


def sombra(img, radio=18, offset=(0, 10), opacidad=150):
    """Añade sombra suave bajo un RGBA (devuelve imagen más grande, centrada igual)."""
    pad = radio * 2 + max(abs(offset[0]), abs(offset[1]))
    w, h = img.size
    base = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    a = img.split()[3].point(lambda v: v * opacidad // 255)
    sh = Image.new('RGBA', img.size, (0, 0, 0, 255))
    sh.putalpha(a)
    base.alpha_composite(sh, (pad + offset[0], pad + offset[1]))
    base = base.filter(ImageFilter.GaussianBlur(radio))
    base.alpha_composite(img, (pad, pad))
    return base


def esquinas_hud(d, x0, y0, x1, y1, color, largo=34, grosor=6):
    for (cx, cy, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(cx, cy), (cx + dx * largo, cy)], fill=color, width=grosor)
        d.line([(cx, cy), (cx, cy + dy * largo)], fill=color, width=grosor)


def envolver(txt, f, ancho):
    lineas, actual = [], ''
    for w in txt.split():
        prueba = (actual + ' ' + w).strip()
        if medir(prueba.replace('*', ''), f)[0] <= ancho or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = w
    if actual:
        lineas.append(actual)
    return lineas


# ---------- dinero ----------
def valor(txt):
    return float(re.sub(r'[^\d.\-]', '', str(txt).replace(',', '')) or 0)


def dinero(v, moneda='$', sufijo=''):
    s = f'{v:,.2f}' if abs(v - round(v)) > 1e-6 and abs(v) < 1000 else f'{round(v):,}'
    return f'{"-" if v < 0 else ""}{moneda}{s.lstrip("-")}{(" " + sufijo) if sufijo else ""}'


# ---------- elementos ----------
def tarjeta_precio(etiqueta, monto_txt, ancho=840):
    """Tarjeta de precio: etiqueta en versalitas + monto grande (el monto se redibuja en el conteo)."""
    f_et, f_m = fuente('bold', 34), fuente('titulo', 150)
    alto = 290
    img = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, ancho - 1, alto - 1], 26, fill=PANEL, outline=NARANJA, width=5)
    esquinas_hud(d, 14, 14, ancho - 15, alto - 15, AMARILLO, 30, 5)
    et = etiqueta.upper()
    w, _ = medir(et, f_et, 6)
    texto_espaciado(d, ((ancho - w) // 2, 34), et, f_et, BLANCO, 6)
    d.line([(ancho // 2 - 60, 88), (ancho // 2 + 60, 88)], fill=NARANJA, width=4)
    w, _ = medir(monto_txt, f_m)
    bb = f_m.getbbox(monto_txt)
    x, y = (ancho - w) // 2 - bb[0], 108 - bb[1]
    d.text((x + 4, y + 6), monto_txt, font=f_m, fill=(0, 0, 0, 160))
    d.text((x, y), monto_txt, font=f_m, fill=AMARILLO)
    return sombra(img)


def titulo(txt, ancho=1000, tam=150):
    """Titular grande. Las *palabras* entre asteriscos van sobre caja naranja."""
    f = fuente('titulo', tam)
    lineas = envolver(txt.upper(), f, ancho - 80)
    alto_l = int(tam * 1.22)
    img = Image.new('RGBA', (ancho, alto_l * len(lineas) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, linea in enumerate(lineas):
        partes = re.split(r'(\*[^*]+\*)', linea)
        limpio = linea.replace('*', '')
        x = (ancho - medir(limpio, f)[0]) // 2
        y = 20 + i * alto_l
        for p in partes:
            if not p:
                continue
            resaltar = p.startswith('*')
            p = p.strip('*')
            w = f.getlength(p)
            if resaltar:
                d.polygon([(x - 16, y + 8), (x + w + 22, y + 2), (x + w + 14, y + alto_l - 6), (x - 22, y + alto_l)],
                          fill=NARANJA)
            for dx, dy in ((-5, 0), (5, 0), (0, -5), (0, 5), (4, 4), (-4, 4), (4, -4), (-4, -4)):
                d.text((x + dx, y + dy), p, font=f, fill=NEGRO)
            d.text((x, y), p, font=f, fill=BLANCO)
            x += w
    return sombra(img, 14, (0, 8))


def barra_texto(txt, ancho=960):
    """Rótulo de impacto a media pantalla (amarillo sobre panel con franja naranja)."""
    f = fuente('titulo', 96)
    lineas = envolver(txt.upper(), f, ancho - 120)
    alto = 40 + len(lineas) * 112
    w_max = max(medir(l, f)[0] for l in lineas) + 110
    img = Image.new('RGBA', (w_max, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w_max, alto], fill=(12, 14, 13, 215))
    d.rectangle([0, 0, 16, alto], fill=NARANJA)
    d.polygon([(w_max - 40, alto), (w_max, alto), (w_max, alto - 40)], fill=NARANJA)
    for i, l in enumerate(lineas):
        bb = f.getbbox(l)
        x = (w_max + 16 - (bb[2] - bb[0])) // 2 - bb[0]
        d.text((x, 22 + i * 112 - bb[1] + 6), l, font=f, fill=AMARILLO)
    return sombra(img, 12, (0, 6))


def informe(items, visibles, moneda='$', titulo_txt='INFORME DE GASTOS', resaltar_ultimo=True):
    """Tablet táctica con las compras acumuladas (sustituye el 'ticket' de la referencia)."""
    f_h, f_r, f_t = fuente('bold', 40), fuente('mono', 44), fuente('titulo', 84)
    ancho, fila = 1000, 72
    filas = items[:visibles]
    alto = 150 + max(1, len(filas)) * fila + 120
    img = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, ancho - 1, alto - 1], 22, fill=(16, 20, 17, 235), outline=(70, 78, 72), width=3)
    d.rectangle([0, 0, ancho, 92], fill=NARANJA)
    texto_espaciado(d, (32, 22), titulo_txt, f_h, NEGRO, 5)
    d.ellipse([ancho - 66, 30, ancho - 34, 62], fill=ROJO)
    y = 120
    for i, (et, v) in enumerate(filas):
        color = AMARILLO if (resaltar_ultimo and i == len(filas) - 1) else BLANCO
        txt = et.upper()
        while f_r.getlength(txt) > ancho - 360 and len(txt) > 4:
            txt = txt[:-2] + '…'
        d.text((34, y), f'{i + 1:02d} {txt}', font=f_r, fill=color)
        m = dinero(v, moneda)
        d.text((ancho - 34 - f_r.getlength(m), y), m, font=f_r, fill=color)
        y += fila
    d.line([(30, y + 10), (ancho - 30, y + 10)], fill=GRIS, width=2)
    total = dinero(sum(v for _, v in filas), moneda)
    d.text((34, y + 32), 'TOTAL', font=f_t, fill=GRIS)
    d.text((ancho - 34 - f_t.getlength(total), y + 32), total, font=f_t, fill=NARANJA)
    return sombra(img)


def tabla_total(items, total_txt, moneda='$'):
    """Resumen final: fases + TOTAL grande (el total se calcula solo, nunca a mano)."""
    f_r, f_v, f_tt, f_t = fuente('bebas', 66), fuente('bebas', 66), fuente('bold', 40), fuente('titulo', 150)
    ancho, fila = 980, 92
    alto = len(items) * fila + 330
    img = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, (et, v) in enumerate(items):
        y = i * fila
        d.rounded_rectangle([0, y, ancho - 1, y + fila - 14], 14, fill=(16, 20, 17, 235), outline=NARANJA, width=3)
        d.rectangle([0, y + 8, 10, y + fila - 22], fill=NARANJA)
        d.text((30, y + 8), f'{i + 1} · {et.upper()}', font=f_r, fill=BLANCO)
        m = dinero(v, moneda)
        d.text((ancho - 30 - f_v.getlength(m), y + 8), m, font=f_v, fill=AMARILLO)
    y = len(items) * fila + 24
    d.rounded_rectangle([90, y, ancho - 90, y + 290], 26, fill=(8, 9, 9, 245), outline=AMARILLO, width=5)
    w, _ = medir('TOTAL', f_tt, 10)
    texto_espaciado(d, ((ancho - w) // 2, y + 20), 'TOTAL', f_tt, NARANJA, 10)
    bb = f_t.getbbox(total_txt)
    d.text(((ancho - (bb[2] - bb[0])) // 2 - bb[0], y + 82 - bb[1] + 10), total_txt, font=f_t, fill=AMARILLO)
    return sombra(img)


def killfeed(a, b):
    f = fuente('bold', 60)
    wa, wb = f.getlength(a.upper()), f.getlength(b.upper())
    ancho = int(wa + wb + 230)
    img = Image.new('RGBA', (ancho, 112), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, ancho - 1, 111], 14, fill=(0, 0, 0, 180))
    d.text((28, 18), a.upper(), font=f, fill=AZUL)
    cx = int(28 + wa + 76)
    d.ellipse([cx - 30, 26, cx + 30, 86], outline=BLANCO, width=6)
    d.line([(cx - 44, 56), (cx + 44, 56)], fill=BLANCO, width=5)
    d.line([(cx, 10), (cx, 102)], fill=BLANCO, width=5)
    d.text((cx + 64, 18), b.upper(), font=f, fill=ROJO)
    return img


def hitmarker(tam=220, color=BLANCO):
    img = Image.new('RGBA', (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c, a, b = tam // 2, tam * 0.16, tam * 0.44
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        d.line([(c + sx * a, c + sy * a), (c + sx * b, c + sy * b)], fill=color, width=max(6, tam // 18))
    return sombra(img, 8, (0, 3), 200)


def ping(txt, color=ROJO):
    f = fuente('bold', 40)
    w = int(f.getlength(txt.upper())) + 60
    ancho = max(w, 180)
    img = Image.new('RGBA', (ancho, 230), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = ancho // 2
    d.rounded_rectangle([cx - w // 2, 0, cx + w // 2, 64], 10, fill=(0, 0, 0, 190))
    d.text((cx - f.getlength(txt.upper()) / 2, 8), txt.upper(), font=f, fill=color)
    d.polygon([(cx, 90), (cx + 50, 140), (cx, 190), (cx - 50, 140)], fill=color, outline=BLANCO, width=5)
    d.polygon([(cx, 200), (cx + 12, 215), (cx, 230), (cx - 12, 215)], fill=color)
    return sombra(img, 10, (0, 4))


def contador(etiqueta, valor_txt):
    f_e, f_v = fuente('bold', 38), fuente('titulo', 180)
    w = max(f_v.getlength(valor_txt), f_e.getlength(etiqueta.upper()) + 40) + 100
    img = Image.new('RGBA', (int(w), 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, 319], 24, fill=PANEL)
    esquinas_hud(d, 12, 12, w - 13, 307, NARANJA, 40, 6)
    texto_espaciado(d, ((w - medir(etiqueta.upper(), f_e, 6)[0]) / 2, 30), etiqueta.upper(), f_e, GRIS, 6)
    bb = f_v.getbbox(valor_txt)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], 92 - bb[1]), valor_txt, font=f_v, fill=BLANCO)
    return sombra(img)


def barra(etiqueta, pct, texto_pct=None):
    f_e, f_p = fuente('bold', 38), fuente('titulo', 72)
    ancho = 900
    img = Image.new('RGBA', (ancho, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, ancho - 1, 199], 20, fill=PANEL)
    texto_espaciado(d, (32, 26), etiqueta.upper(), f_e, BLANCO, 4)
    t = texto_pct or f'{round(pct)}%'
    d.text((ancho - 32 - f_p.getlength(t), 6), t, font=f_p, fill=AMARILLO)
    d.rounded_rectangle([32, 118, ancho - 32, 164], 10, fill=(40, 46, 42))
    fin = 32 + (ancho - 64) * max(0, min(1, pct / 100))
    if fin > 44:
        d.rounded_rectangle([32, 118, fin, 164], 10, fill=NARANJA)
        for x in range(52, int(fin), 34):
            d.line([(x, 164), (x + 18, 118)], fill=(255, 150, 80), width=8)
    return sombra(img)


def sello(txt, color=ROJO):
    f = fuente('titulo', 120)
    w = int(f.getlength(txt.upper())) + 90
    img = Image.new('RGBA', (w, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([6, 6, w - 7, 193], 18, outline=color, width=12)
    bb = f.getbbox(txt.upper())
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (200 - (bb[3] - bb[1])) / 2 - bb[1]), txt.upper(), font=f, fill=color)
    return img.rotate(-12, expand=True, resample=Image.BICUBIC)


def tachar(ancho=900, alto=360):
    img = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.line([(20, 20), (ancho - 20, alto - 20)], fill=ROJO, width=26)
    d.line([(20, alto - 20), (ancho - 20, 20)], fill=ROJO, width=26)
    return sombra(img, 10, (0, 4))


def sticker(ruta, max_w=760, max_h=760, borde=14):
    im = Image.open(ruta).convert('RGBA')
    im.thumbnail((max_w, max_h), Image.LANCZOS)
    tiene_alfa = im.getextrema()[3][0] < 250
    if tiene_alfa:  # recorte transparente → contorno blanco que sigue la forma
        a = im.split()[3].filter(ImageFilter.MaxFilter(borde * 2 + 1))
        base = Image.new('RGBA', im.size, BLANCO + (0,))
        base.putalpha(a)
        lienzo = Image.new('RGBA', (im.width + borde * 2, im.height + borde * 2), (0, 0, 0, 0))
        lienzo.alpha_composite(base.resize(lienzo.size), (0, 0))
        lienzo.alpha_composite(im, (borde, borde))
        return sombra(lienzo, 16, (0, 10))
    marco = Image.new('RGBA', (im.width + borde * 2, im.height + borde * 2), BLANCO + (255,))
    marco.alpha_composite(im, (borde, borde))
    m = Image.new('L', marco.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, marco.width - 1, marco.height - 1], 24, fill=255)
    marco.putalpha(m)
    return sombra(marco, 18, (0, 12))


def marcador_imagen(txt, w, h):
    """Si falta una imagen: tarjeta con el nombre para que el render no se rompa (y se note qué falta)."""
    img = fondo_tactico(w, h).convert('RGBA')
    d = ImageDraw.Draw(img)
    f = fuente('bold', 44)
    lineas = envolver(f'FALTA IMAGEN: {txt}', f, w - 120)
    y = h // 2 - len(lineas) * 30
    for l in lineas:
        d.text(((w - f.getlength(l)) / 2, y), l, font=f, fill=NARANJA)
        y += 60
    esquinas_hud(d, 30, 30, w - 31, h - 31, NARANJA, 60, 8)
    return img


@lru_cache(maxsize=8)
def fondo_tactico(w, h):
    """Fondo de 'mapa táctico': degradado oscuro, cuadrícula y curvas de nivel."""
    import numpy as np
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.hypot(xx - w * 0.5, yy - h * 0.45) / max(w, h)
    base = (np.clip(1 - r * 1.3, 0, 1)[..., None] * np.array([22, 30, 24]) + np.array([6, 8, 7])).astype(np.float32)
    z = (np.sin(xx / 97.0) * np.cos(yy / 131.0) + 0.6 * np.sin((xx + yy) / 173.0) + 0.4 * np.cos((xx - 2 * yy) / 61.0))
    curvas = (np.abs((z * 4) % 1 - 0.5) < 0.03)
    base[curvas] += np.array([18, 26, 18])
    rejilla = ((xx % 90) < 2) | ((yy % 90) < 2)
    base[rejilla] += np.array([10, 14, 10])
    return Image.fromarray(np.clip(base, 0, 255).astype('uint8'), 'RGB')


def subtitulo(palabras, activa, ancho=980):
    """Subtítulos dinámicos: 1–3 palabras, la que estás diciendo en amarillo y algo más grande."""
    f = fuente('negra', 84)
    txt = [w.upper() for w in palabras]
    esp = 22
    total = sum(f.getlength(w) for w in txt) + esp * (len(txt) - 1)
    escala = min(1.0, (ancho - 40) / max(1, total))
    if escala < 1:
        f = fuente('negra', int(84 * escala))
        total = sum(f.getlength(w) for w in txt) + esp * (len(txt) - 1)
    img = Image.new('RGBA', (ancho, 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = (ancho - total) / 2
    for i, w in enumerate(txt):
        color = AMARILLO if i == activa else BLANCO
        d.text((x, 20), w, font=f, fill=color, stroke_width=9, stroke_fill=NEGRO)
        x += f.getlength(w) + esp
    return img


def cubrir(im, w, h):
    """Ajusta una imagen PIL para llenar w×h (recorte centrado)."""
    return ImageOps.fit(im.convert('RGB'), (w, h), Image.LANCZOS)


def ease_out_back(t, s=1.7):
    t = max(0.0, min(1.0, t)) - 1
    return t * t * ((s + 1) * t + s) + 1


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - math.cos(math.pi * t) / 2
