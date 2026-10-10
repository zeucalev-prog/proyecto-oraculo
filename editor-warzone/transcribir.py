#!/usr/bin/env python3
"""Transcribe tu video (Whisper) para escribir el guion con marcas a partir de lo que dijiste.

Uso: python transcribir.py mi_toma.MOV [--modelo small]
Genera mi_toma.txt (texto por frases, con segundos) y mi_toma.palabras.json (lo reutiliza editar.py)."""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oraculo import tiempos  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('video')
ap.add_argument('--modelo', default='small')
ap.add_argument('--idioma', default='es')
a = ap.parse_args()
base = os.path.splitext(a.video)[0]
voz = tiempos.transcribir(a.video, a.modelo, a.idioma, cache=base + '.palabras.json')
lineas, actual = [], []
for w in voz:
    actual.append(w)
    if w['w'][-1:] in '.?!' or len(actual) > 22:
        lineas.append(f"[{actual[0]['s']:6.1f}s] " + ' '.join(x['w'] for x in actual))
        actual = []
if actual:
    lineas.append(f"[{actual[0]['s']:6.1f}s] " + ' '.join(x['w'] for x in actual))
open(base + '.txt', 'w', encoding='utf-8').write('\n'.join(lineas) + '\n')
print('\n'.join(lineas))
print(f'\n✔ {base}.txt y {base}.palabras.json  ({len(voz)} palabras, {tiempos.duracion(a.video):.1f}s)')
