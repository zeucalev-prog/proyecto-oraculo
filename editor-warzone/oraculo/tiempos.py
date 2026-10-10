"""Tiempos de cada palabra: Whisper (faster-whisper) → SRT → reparto proporcional. Y alineación guion ↔ voz."""
import difflib
import json
import os
import re
import subprocess

from .guion import normalizar


def transcribir(video, modelo='small', idioma='es', cache=None):
    """Palabras con tiempos [{'w','s','e'}] usando faster-whisper. Guarda caché en JSON."""
    if cache and os.path.exists(cache):
        return json.load(open(cache, encoding='utf-8'))
    from faster_whisper import WhisperModel
    m = WhisperModel(modelo, device='auto', compute_type='int8')
    segs, _ = m.transcribe(video, language=idioma, word_timestamps=True, vad_filter=True)
    palabras = [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)} for seg in segs for w in seg.words]
    if cache:
        json.dump(palabras, open(cache, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    return palabras


def leer_srt(ruta):
    """SRT (CapCut, TikTok, Premiere…) → palabras repartiendo cada subtítulo por longitud de palabra."""
    txt = open(ruta, encoding='utf-8-sig').read()
    out = []
    for bloque in re.split(r'\n\s*\n', txt.strip()):
        lineas = bloque.strip().splitlines()
        tl = next((l for l in lineas if '-->' in l), None)
        if not tl:
            continue
        a, b = [_t(x) for x in tl.split('-->')]
        texto = ' '.join(lineas[lineas.index(tl) + 1:])
        ws = [w for w in re.sub(r'<[^>]+>', '', texto).split() if normalizar(w)]
        if not ws:
            continue
        pesos = [len(w) + 2 for w in ws]
        tot, acc = sum(pesos), 0
        for w, p in zip(ws, pesos):
            s = a + (b - a) * acc / tot
            acc += p
            out.append({'w': w, 's': round(s, 3), 'e': round(a + (b - a) * acc / tot, 3)})
    return out


def _t(s):
    h, m, r = s.strip().replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(r)


def tramos_de_voz(video, ruido='-35dB', minimo=0.35):
    """Detecta tramos con voz (fuera de silencios) usando silencedetect de ffmpeg."""
    dur = duracion(video)
    log = subprocess.run(['ffmpeg', '-hide_banner', '-i', video, '-af', f'silencedetect=n={ruido}:d={minimo}',
                          '-f', 'null', '-'], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
    fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    tramos, t = [], 0.0
    for a, b in zip(ini, fin + [dur]):
        if a > t + 0.05:
            tramos.append((t, a))
        t = b
    if t < dur - 0.05:
        tramos.append((t, dur))
    return tramos or [(0, dur)]


def repartir(palabras_guion, video):
    """Sin transcripción: reparte las palabras del guion sobre los tramos con voz, por longitud."""
    tramos = tramos_de_voz(video)
    total = sum(b - a for a, b in tramos)
    pesos = [len(normalizar(w)) + 2 for w in palabras_guion]
    tp, out, acc = sum(pesos), [], 0.0

    def mapa(x):  # x en segundos de "voz" → segundos reales
        for a, b in tramos:
            if x <= b - a:
                return a + x
            x -= b - a
        return tramos[-1][1]
    for w, p in zip(palabras_guion, pesos):
        s = acc / tp * total
        acc += p
        out.append({'w': w, 's': round(mapa(s), 3), 'e': round(mapa(acc / tp * total), 3)})
    return out


def alinear(palabras_guion, voz):
    """Para cada palabra del guion, su tiempo de inicio en la voz real (aunque Whisper se equivoque o improvises).

    Alineación global con difflib sobre palabras normalizadas; las que no casan se interpolan."""
    a = [normalizar(w) for w in palabras_guion]
    b = [normalizar(w['w']) for w in voz]
    t = [None] * len(a)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            t[i + k] = (voz[j + k]['s'], voz[j + k]['e'])
    # palabras unidas/separadas distinto ("pay to win" vs "paytowin"): coincidencia aproximada en huecos
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'replace':
            for k in range(i1, i2):
                jj = j1 + round((k - i1) * (j2 - j1) / max(1, i2 - i1))
                jj = min(jj, j2 - 1)
                t[k] = (voz[jj]['s'], voz[jj]['e'])
    conocidos = [(i, x) for i, x in enumerate(t) if x]
    if not conocidos:
        raise RuntimeError('No pude alinear el guion con la voz: ¿es el guion correcto para este video?')
    for i in range(len(t)):
        if t[i]:
            continue
        prev = max((c for c in conocidos if c[0] < i), default=None, key=lambda c: c[0])
        nxt = min((c for c in conocidos if c[0] > i), default=None, key=lambda c: c[0])
        if prev and nxt:
            f = (i - prev[0]) / (nxt[0] - prev[0])
            s = prev[1][1] + f * (nxt[1][0] - prev[1][1])
        elif prev:
            s = prev[1][1] + 0.3 * (i - prev[0])
        else:
            s = max(0, nxt[1][0] - 0.3 * (nxt[0] - i))
        t[i] = (s, s + 0.25)
    coincidencia = sum(n for *_, n in sm.get_matching_blocks()) / max(1, len(a))
    return [x[0] for x in t], [x[1] for x in t], coincidencia


def duracion(video):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video],
                                capture_output=True, text=True).stdout.strip())


def info_video(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height,r_frame_rate:stream_side_data=rotation', '-of', 'json', video],
                       capture_output=True, text=True)
    st = json.loads(r.stdout)['streams'][0]
    num, den = st['r_frame_rate'].split('/')
    return st['width'], st['height'], float(num) / float(den)
