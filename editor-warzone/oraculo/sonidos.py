"""Efectos de sonido sintetizados (sin archivos con derechos) + mezcla con la voz y la música.

Si pones un .wav/.mp3 en sfx/<nombre>.wav, se usa ese en lugar del sintetizado (p. ej. sfx/caja.wav)."""
import os
import subprocess

import numpy as np

SR = 48000
_rng = np.random.default_rng(11)


def _t(s): return np.arange(int(s * SR)) / SR
def _ruido(s): return _rng.standard_normal(int(s * SR))
def _env(s, tau): return np.exp(-_t(s) / tau)


def _norm(x, pico=1.0):
    p = np.max(np.abs(x)) or 1.0
    return x / p * pico


def _banda(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def _barrido(f0, f1, s):
    t = _t(s)
    f = f0 * (f1 / f0) ** (t / s)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def _tonos(fs, s, tau):
    t = _t(s)
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t / tau) for f in fs)


def _poner(dst, src, en):
    i = int(en * SR)
    n = min(len(src), len(dst) - i)
    if n > 0:
        dst[i:i + n] += src[:n]


def whoosh(s=0.45, subir=True):
    x = _ruido(s)
    seg, out, n = int(0.02 * SR), np.zeros(int(s * SR)), int(s * SR)
    for k in range(0, n - 2 * seg, seg):
        c = (300 * (12 ** (k / n))) if subir else (3600 / (12 ** (k / n)))
        out[k:k + 2 * seg] += _banda(x[k:k + 2 * seg], c * 0.6, c * 1.8) * np.hanning(2 * seg)
    return _norm(out * np.sin(np.linspace(0, np.pi, n)) ** 1.5, 0.55)


def pop():
    x = _barrido(300, 900, 0.12) * _env(0.12, 0.04)
    return _norm(x, 0.6)


def caja():
    """Caja registradora: golpe mecánico + campana."""
    out = np.zeros(int(1.0 * SR))
    _poner(out, _banda(_ruido(0.08), 600, 5000) * _env(0.08, 0.015) * 0.7, 0)
    _poner(out, _banda(_ruido(0.06), 800, 6000) * _env(0.06, 0.012) * 0.5, 0.07)
    _poner(out, _tonos([2637, 3520, 5274], 0.9, 0.28), 0.12)
    return _norm(out, 0.55)


def moneda():
    out = np.zeros(int(0.7 * SR))
    a = _tonos([1976, 2637], 0.5, 0.12)
    _poner(out, a, 0)
    _poner(out, a * 0.8, 0.08)
    return _norm(out, 0.4)


def disparo():
    t = _t(0.6)
    cuerpo = np.sin(2 * np.pi * np.cumsum(140 * np.exp(-t / 0.03) + 45) / SR) * np.exp(-t / 0.12)
    crack = _banda(_ruido(0.6), 800, 9000) * np.exp(-t / 0.02)
    cola = _banda(_ruido(0.6), 150, 1500) * np.exp(-t / 0.18) * 0.35
    return _norm(cuerpo + crack * 1.2 + cola, 0.9)


def recarga():
    out = np.zeros(int(0.6 * SR))
    clic = lambda: _banda(_ruido(0.03), 1500, 8000) * _env(0.03, 0.004) + _tonos([3200], 0.03, 0.005) * 0.3
    _poner(out, clic(), 0)
    _poner(out, _banda(_ruido(0.12), 400, 3000) * np.hanning(int(0.12 * SR)) * 0.3, 0.06)
    _poner(out, clic() * 1.3, 0.28)
    return _norm(out, 0.6)


def hitmarker():
    t = _t(0.09)
    x = _banda(_ruido(0.09), 2500, 9000) * np.exp(-t / 0.012) + np.sin(2 * np.pi * 2900 * t) * np.exp(-t / 0.015) * 0.6
    return _norm(x, 0.55)


def uav():
    """Barrido de radar (ping de UAV)."""
    t = _t(1.1)
    x = np.sin(2 * np.pi * 1480 * t) * np.exp(-t / 0.35) + np.sin(2 * np.pi * 2960 * t) * np.exp(-t / 0.2) * 0.3
    return _norm(x * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)), 0.4)


def bip():
    out = np.zeros(int(0.32 * SR))
    b = np.sin(2 * np.pi * 1760 * _t(0.07)) * np.hanning(int(0.07 * SR))
    _poner(out, b, 0)
    _poner(out, b, 0.13)
    return _norm(out, 0.35)


def impacto():
    t = _t(0.8)
    x = np.sin(2 * np.pi * 52 * t) * np.exp(-t / 0.2) + _banda(_ruido(0.8), 60, 2500) * np.exp(-t / 0.05) * 0.8
    return _norm(x, 0.85)


def explosion():
    t = _t(1.6)
    x = _banda(_ruido(1.6), 30, 900) * np.exp(-t / 0.45) + np.sin(2 * np.pi * 38 * t) * np.exp(-t / 0.3)
    return _norm(x, 0.95)


def subida(s=0.9):
    x = _barrido(180, 1400, s) * 0.4 + _banda(_ruido(s), 1000, 6000) * 0.25
    return _norm(x * np.linspace(0, 1, int(s * SR)) ** 2, 0.5)


def ding():
    return _norm(_tonos([1318.5, 1975.5, 2637], 1.4, 0.4), 0.45)


def teclado(s=0.6, golpes=10):
    out = np.zeros(int((s + 0.05) * SR))
    for k in range(golpes):
        c = _banda(_ruido(0.015), 1800, 7000) * _env(0.015, 0.003)
        _poner(out, c * _rng.uniform(0.6, 1), k * s / golpes)
    return _norm(out, 0.35)


def error():
    t = _t(0.45)
    x = np.sign(np.sin(2 * np.pi * 180 * t)) * 0.4 + np.sign(np.sin(2 * np.pi * 188 * t)) * 0.4
    return _norm(_banda(x, 100, 3000) * np.exp(-t / 0.25), 0.35)


def glitch():
    out = np.zeros(int(0.35 * SR))
    for k in range(6):
        _poner(out, _banda(_ruido(0.03), _rng.uniform(300, 2000), 8000) * _rng.uniform(0.4, 1), k * 0.05)
    return _norm(out, 0.4)


def tic():
    return _norm(_banda(_ruido(0.02), 2000, 8000) * _env(0.02, 0.004), 0.25)


BANCO = {
    'whoosh': lambda: whoosh(), 'whoosh-abajo': lambda: whoosh(subir=False), 'pop': pop, 'caja': caja,
    'moneda': moneda, 'disparo': disparo, 'recarga': recarga, 'hit': hitmarker, 'uav': uav, 'bip': bip,
    'impacto': impacto, 'explosion': explosion, 'subida': lambda: subida(), 'ding': ding,
    'teclado': lambda: teclado(), 'error': error, 'glitch': glitch, 'tic': tic,
}


def cargar(nombre, carpeta_sfx=None):
    """Devuelve el sonido como array mono a 48 kHz. Prefiere un archivo propio sfx/<nombre>.(wav|mp3)."""
    if carpeta_sfx:
        for ext in ('.wav', '.mp3', '.ogg', '.m4a'):
            p = os.path.join(carpeta_sfx, nombre + ext)
            if os.path.exists(p):
                return leer_audio(p)
    if nombre not in BANCO:
        raise ValueError(f'sonido "{nombre}" no existe. Disponibles: {", ".join(sorted(BANCO))}')
    return BANCO[nombre]()


def leer_audio(ruta, canales=1):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', ruta, '-ac', str(canales), '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return x.reshape(-1, canales) if canales > 1 else x


def mezclar(video, eventos_sfx, salida_wav, duracion, musica=None, vol_musica=0.16, vol_sfx=0.7, carpeta_sfx=None):
    """Voz del video + SFX en sus tiempos + música (baja sola cuando hablas). Escribe WAV estéreo 48 kHz."""
    n = int(duracion * SR) + SR
    voz = leer_audio(video, 2) if _tiene_audio(video) else np.zeros((n, 2))
    voz = np.pad(voz, ((0, max(0, n - len(voz))), (0, 0)))[:n]
    fx = np.zeros(n)
    cache = {}
    for t, nombre, vol in eventos_sfx:
        if nombre not in cache:
            cache[nombre] = cargar(nombre, carpeta_sfx)
        _poner(fx, cache[nombre] * vol, max(0, t))
    mezcla = voz + (fx * vol_sfx)[:, None]
    if musica:
        m = leer_audio(musica, 2)
        reps = int(np.ceil(n / len(m)))
        m = np.tile(m, (reps, 1))[:n]
        # ducking: envolvente de la voz suavizada → la música baja ~60% mientras hablas
        e = np.abs(voz).mean(axis=1)
        k = int(0.25 * SR)
        e = np.convolve(e, np.ones(k) / k, 'same')
        e = np.clip(e / (np.percentile(e, 95) or 1), 0, 1)
        duck = 1 - 0.6 * e
        fade = np.ones(n)
        fade[-2 * SR:] = np.linspace(1, 0, 2 * SR)
        mezcla += m * (vol_musica * duck * fade)[:, None]
    pico = np.max(np.abs(mezcla)) or 1
    if pico > 0.98:
        mezcla *= 0.98 / pico
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', salida_wav],
                   input=mezcla.astype(np.float32).tobytes(), check=True)


def _tiene_audio(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0',
                        video], capture_output=True, text=True)
    return bool(r.stdout.strip())
