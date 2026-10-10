#!/usr/bin/env python3
"""Crea un video de PRUEBA (presentador falso + voz sintética espeak-ng) a partir de un guion,
para probar el editor sin grabarte. También crea un SRT con los tiempos y unas imágenes de ejemplo.

Uso: python demo/hacer_demo.py guiones/01-pay-to-win.guion demo/salida
Necesita: espeak-ng (apt install espeak-ng)."""
import math
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from oraculo import graficos as G  # noqa: E402
from oraculo.guion import Guion  # noqa: E402

SR = 48000
W, H, FPS = 1080, 1920, 30


def frases_del_guion(ruta):
    """Texto hablado por línea (sin marcas)."""
    out = []
    for linea in open(ruta, encoding='utf-8'):
        s = linea.strip()
        if not s or s.startswith('#') or s.startswith('[') or re.match(r'^[a-z_]+\s*:', s):
            continue
        s = re.sub(r'\{[^}]*\}', ' ', s)
        s = re.sub(r'\s+', ' ', s).strip()
        if s:
            out.append(s)
    return out


def voz(frases, carpeta):
    trozos, srt, t = [], [], 0.3
    for i, fr in enumerate(frases):
        wav = os.path.join(carpeta, f'_f{i}.wav')
        subprocess.run(['espeak-ng', '-v', 'es-419', '-s', '172', '-p', '45', '-w', wav, fr], check=True)
        x = subprocess.run(['ffmpeg', '-v', 'error', '-i', wav, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                           capture_output=True, check=True).stdout
        a = np.frombuffer(x, np.float32)
        # quitar silencios de los bordes
        idx = np.where(np.abs(a) > 0.02)[0]
        a = a[idx[0]:idx[-1]] if len(idx) else a
        os.remove(wav)
        # un subtítulo por oración
        oraciones = [o for o in re.split(r'(?<=[.?!,])\s+', fr) if o]
        pesos = [len(o) for o in oraciones]
        acc = 0
        for o, p in zip(oraciones, pesos):
            a0 = t + len(a) / SR * acc / sum(pesos)
            acc += p
            srt.append((a0, t + len(a) / SR * acc / sum(pesos), o))
        trozos.append(np.zeros(int(0.3 * SR)) if i == 0 else np.zeros(int(0.28 * SR)))
        trozos.append(a)
        t += len(a) / SR + 0.28
    trozos.append(np.zeros(int(0.8 * SR)))
    audio = np.concatenate(trozos).astype(np.float32)
    return audio, srt


def escribir_srt(srt, ruta):
    f = lambda s: f'{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(s * 1000 % 1000):03d}'
    with open(ruta, 'w', encoding='utf-8') as fh:
        for i, (a, b, txt) in enumerate(srt, 1):
            fh.write(f'{i}\n{f(a)} --> {f(b)}\n{txt}\n\n')


def presentador(audio, ruta):
    """Presentador falso: personaje con casco que mueve la boca con el volumen de la voz."""
    dur = len(audio) / SR
    n = int(dur * FPS)
    env = np.array([np.sqrt(np.mean(audio[int(i / FPS * SR):int((i + 1) / FPS * SR)] ** 2) + 1e-9) for i in range(n)])
    env = np.clip(env / (np.percentile(env, 95) or 1), 0, 1)
    fondo = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(fondo)
    for y in range(H):  # pared con degradado + "luz" de cuarto gamer
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(28 + 20 * k), int(24 + 10 * k), int(44 - 10 * k)))
    luz = Image.new('L', (W, H), 0)
    ImageDraw.Draw(luz).ellipse([-300, -200, 700, 900], fill=120)
    luz = luz.filter(ImageFilter.GaussianBlur(160))
    fondo = Image.composite(Image.new('RGB', (W, H), (255, 107, 26)), fondo, luz.point(lambda v: v // 3))
    d = ImageDraw.Draw(fondo)
    d.rectangle([700, 300, 1080, 1100], fill=(18, 16, 30))
    for k in range(6):
        d.rectangle([730, 340 + k * 120, 1050, 420 + k * 120], fill=(30 + k * 8, 26, 60))
    d.text((40, 60), 'VIDEO DE PRUEBA · AQUÍ VA TU GRABACIÓN', font=G.fuente('bold', 34), fill=(255, 255, 255))
    cy = int(0.40 * H)
    tmpwav = ruta + '.f32'
    audio.tofile(tmpwav)
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', tmpwav,
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-shortest', ruta], stdin=subprocess.PIPE)
    for i in range(n):
        im = fondo.copy()
        d = ImageDraw.Draw(im)
        bob = int(6 * math.sin(i / FPS * 2.1))
        hx, hy = 540, cy + bob
        d.rounded_rectangle([230, hy + 330, 850, H + 50], 160, fill=(48, 58, 44))            # torso
        d.rectangle([500, hy + 250, 580, hy + 360], fill=(232, 190, 160))                    # cuello
        d.ellipse([hx - 230, hy - 260, hx + 230, hy + 300], fill=(240, 200, 170))            # cara
        d.chord([hx - 260, hy - 330, hx + 260, hy + 120], 180, 360, fill=(62, 74, 52))      # casco
        d.rectangle([hx - 262, hy - 110, hx + 262, hy - 80], fill=(62, 74, 52))
        parpadeo = (i % 110) < 4
        for ox in (-95, 95):
            if parpadeo:
                d.line([(hx + ox - 30, hy + 10), (hx + ox + 30, hy + 10)], fill=(20, 20, 20), width=8)
            else:
                d.ellipse([hx + ox - 26, hy - 20, hx + ox + 26, hy + 36], fill=(20, 20, 20))
        boca = int(10 + 70 * env[i])
        d.rounded_rectangle([hx - 70, hy + 140 - boca // 3, hx + 70, hy + 150 + boca], 30, fill=(90, 20, 30))
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()
    os.remove(tmpwav)


def imagen_ejemplo(nombre, ruta):
    """Ilustraciones simples de relleno para la demo (en tu canal: imágenes de IA con el prompt del guion)."""
    w, h = 1080, 1350
    im = G.fondo_tactico(w, h).convert('RGB').copy()
    d = ImageDraw.Draw(im)
    luz = Image.new('L', (w, h), 0)
    ImageDraw.Draw(luz).ellipse([140, 200, 940, 1100], fill=200)
    luz = luz.filter(ImageFilter.GaussianBlur(140))
    im = Image.composite(Image.new('RGB', (w, h), (120, 60, 20)), im, luz.point(lambda v: v // 2))
    d = ImageDraw.Draw(im)
    N, A, B = G.NARANJA, G.AMARILLO, (240, 240, 230)
    if 'pase' in nombre:
        for k in range(7):
            d.rounded_rectangle([200 + k * 14, 300 + k * 110, 880 - k * 14, 390 + k * 110], 20, fill=(40 + k * 20, 40, 20), outline=A, width=6)
            d.text((240 + k * 14, 312 + k * 110), f'NIVEL {k * 15 + 1}', font=G.fuente('titulo', 60), fill=A)
    elif 'bundle' in nombre:
        for k in range(14):
            x, y = 160 + (k % 4) * 190 + (k // 4) * 40, 1050 - (k // 4) * 200 - (k % 2) * 30
            d.rectangle([x, y, x + 170, y + 170], fill=(70 + k * 9, 50, 30), outline=N, width=8)
            d.rectangle([x + 70, y, x + 100, y + 170], fill=A)
    elif 'setup' in nombre:
        for k, x in enumerate((90, 380, 670)):
            d.rounded_rectangle([x, 380, x + 320, 600], 14, fill=(20, 22, 40), outline=(90, 200, 255), width=8)
        d.rectangle([150, 700, 930, 760], fill=(50, 50, 60))
        d.rounded_rectangle([340, 820, 740, 1180], 60, fill=(25, 25, 30), outline=N, width=10)
    elif 'energ' in nombre:
        for k in range(18):
            x, y = 130 + (k % 6) * 140, 1080 - (k // 6) * 250
            d.rounded_rectangle([x, y, x + 110, y + 220], 18, fill=(30, 200, 90) if k % 2 else (40, 120, 255))
            d.rectangle([x, y + 80, x + 110, y + 120], fill=(10, 10, 10))
    elif 'coach' in nombre:
        d.rectangle([140, 300, 940, 860], fill=(30, 60, 40), outline=(140, 100, 60), width=20)
        d.text((200, 380), 'NO TE ASOMES', font=G.fuente('titulo', 110), fill=B)
        d.text((200, 560), 'SIN PLACAS', font=G.fuente('titulo', 110), fill=B)
        d.line([(200, 760), (880, 700)], fill=N, width=14)
    elif 'gulag' in nombre:
        cono = Image.new('L', (w, h), 0)
        ImageDraw.Draw(cono).polygon([(470, 0), (610, 0), (900, 1200), (180, 1200)], fill=170)
        cono = cono.filter(ImageFilter.GaussianBlur(40))
        im = Image.composite(Image.new('RGB', (w, h), (230, 230, 210)), im.point(lambda v: v // 2), cono)
        d = ImageDraw.Draw(im)
        d.ellipse([440, 760, 640, 960], fill=(62, 74, 52))
        d.rectangle([450, 940, 630, 1200], fill=(48, 58, 44))
    im.save(ruta, quality=92)


def main():
    guion, carpeta = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(carpeta, 'imagenes'), exist_ok=True)
    frases = frases_del_guion(guion)
    audio, srt = voz(frases, carpeta)
    escribir_srt(srt, os.path.join(carpeta, 'voz.srt'))
    presentador(audio, os.path.join(carpeta, 'presentador-prueba.mp4'))
    g = Guion(guion)
    nombres = {b['kv'].get('img') for b in g.bloques} | {e['args'][0] for e in g.eventos if e['tipo'] == 'img'}
    for nm in filter(None, nombres):
        imagen_ejemplo(nm, os.path.join(carpeta, 'imagenes', nm))
    print('listo:', carpeta, f'({len(audio) / SR:.1f}s)')


if __name__ == '__main__':
    main()
