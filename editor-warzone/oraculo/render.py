"""Línea de tiempo + render cuadro por cuadro: tu video es la base y encima van diseños, gráficos y sonidos."""
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

from . import graficos as G
from .tiempos import duracion

W, H = 1080, 1920
ADELANTO = 0.10          # los elementos entran un pelín antes de la palabra: se siente "a tiempo"
T_ENTRA, T_SALE = 0.22, 0.15
T_TRANS = 0.24

SFX_DEFECTO = {
    'precio': [('caja', 0, 1.0)], 'titulo': [('impacto', 0, 0.7)], 'texto': [('whoosh', -0.05, 0.8)],
    'img': [('pop', 0, 1.0)], 'clip': [('whoosh', -0.05, 0.8)], 'kill': [('disparo', 0, 0.8), ('hit', 0.06, 1.0)],
    'hit': [('hit', 0, 1.0)], 'ping': [('bip', 0, 1.0)], 'cuenta': [('teclado', 0.1, 1.0)],
    'total': [('subida', -0.3, 0.9), ('caja', 1.1, 1.0)], 'contador': [('teclado', 0, 0.8), ('ding', 0.7, 0.7)],
    'barra': [('subida', 0, 0.7)], 'sello': [('impacto', 0.08, 1.0)], 'tachar': [('error', 0, 1.0)],
    'zoom': [('whoosh', -0.05, 0.4)], 'flash': [('glitch', 0, 0.6)], 'sacudir': [('explosion', 0, 0.9)],
}
DURACION = {'precio': 3.0, 'titulo': 6.0, 'texto': 2.4, 'img': 5.0, 'clip': 6.0, 'kill': 2.6, 'hit': 0.38,
            'ping': 2.6, 'cuenta': 3.4, 'total': 99, 'contador': 3.0, 'barra': 3.0, 'sello': 2.0, 'tachar': 1.8,
            'flash': 0.28, 'sacudir': 0.4}
SLOT = {'precio': 'arriba', 'titulo': 'arriba', 'contador': 'arriba', 'barra': 'arriba', 'cuenta': 'arriba',
        'total': 'arriba', 'texto': 'centro', 'sello': 'centro', 'img': 'img', 'clip': 'img', 'tachar': 'tachar'}

ZONAS = {  # (cx, cy, max_w, max_h) por diseño y slot; 'subs' = altura de subtítulos
    'cara':        {'arriba': (540, 400, 1000, 470), 'centro': (540, 1080, 1000, 330), 'img': (540, 470, 820, 560), 'subs': 1360},
    'mitad':       {'arriba': (540, 470, 1000, 820), 'centro': (540, 760, 1000, 260), 'img': (540, 470, 860, 800), 'subs': 962},
    'mitad-abajo': {'arriba': (540, 1300, 1000, 560), 'centro': (540, 1160, 1000, 260), 'img': (540, 1300, 860, 520), 'subs': 962},
    'cubrir':      {'arriba': (540, 470, 1000, 600), 'centro': (540, 1060, 1000, 330), 'img': (540, 600, 880, 760), 'subs': 1360},
    'ventana':     {'arriba': (540, 440, 1000, 520), 'centro': (540, 820, 1000, 300), 'img': (540, 520, 880, 600), 'subs': 1010},
}


class Proyecto:
    def __init__(self, guion, tiempos_guion, voz, video, carpeta, fps, cara_y=0.40, subtitulos=True, musica=None,
                 tiempos_fin=None):
        self.tg_fin = tiempos_fin or [t + 0.25 for t in tiempos_guion]
        self.g, self.tg, self.voz, self.video, self.dir = guion, tiempos_guion, voz, video, carpeta
        self.fps, self.cara_y, self.subtitulos = fps, cara_y, subtitulos
        self.dur = duracion(video)
        self.moneda = guion.meta.get('moneda', '$')
        self.musica = musica
        self.bloques, self.capas, self.sfx, self.avisos = [], [], [], []
        self._linea_de_tiempo()

    # ---------- tiempos ----------
    def t_palabra(self, idx):
        if idx >= len(self.tg):
            return min(self.dur - 0.3, self.tg[-1] + 0.5)
        return max(0.0, self.tg[idx] - ADELANTO)

    def _ruta(self, nombre):
        for base in (self.dir, os.path.join(self.dir, 'imagenes'), os.path.join(self.dir, 'clips')):
            p = os.path.join(base, nombre)
            if os.path.exists(p):
                return p
        self.avisos.append(f'falta el archivo "{nombre}" (lo busqué en {self.dir}, imagenes/ y clips/)')
        return None

    def _sfx(self, tipo, t, kv):
        s = kv.get('sfx')
        vol = float(kv.get('vol', 1))
        if s == 'no':
            return
        if s:
            for nombre in s.split(','):
                self.sfx.append((t, nombre, vol))
            return
        for nombre, dt, v in SFX_DEFECTO.get(tipo, []):
            self.sfx.append((t + dt, nombre, v * vol))

    def _linea_de_tiempo(self):
        bl = self.g.bloques
        cara_n = 0
        for i, b in enumerate(bl):
            t0 = 0.0 if i == 0 else self.t_palabra(b['idx'])
            t1 = self.dur if i == len(bl) - 1 else self.t_palabra(bl[i + 1]['idx'])
            kv = b['kv']
            zoom = 1.0
            if b['layout'] == 'cara':
                zoom = float(kv.get('zoom', 1.0 if 'zoom' not in b['args'] else 1.18))
                if 'zoom' not in kv and 'zoom' not in b['args'] and 'fijo' not in b['args']:
                    zoom = (1.0, 1.1)[cara_n % 2]  # alterna planos: se siente editado ("jump cut")
                cara_n += 1
            fondo = None
            if kv.get('img'):
                p = self._ruta(kv['img'])
                fondo = ('img', p, kv['img'])
            elif kv.get('clip'):
                p = self._ruta(kv['clip'])
                fondo = ('clip', p, kv['clip']) if p else ('img', None, kv['clip'])
            self.bloques.append({'layout': b['layout'], 't0': t0, 't1': t1, 'zoom': zoom, 'fondo': fondo, 'kv': kv,
                                 'idx': i, 'args': b['args']})
            if i > 0:
                if kv.get('sfx') != 'no':
                    nombre = kv.get('sfx') or ('whoosh' if b['layout'] != 'cara' else 'whoosh-abajo')
                    for n_ in nombre.split(','):
                        self.sfx.append((t0 - 0.12, n_, 0.75))
        self._eventos()

    def bloque_en(self, t):
        for b in reversed(self.bloques):
            if t >= b['t0']:
                return b
        return self.bloques[0]

    def _eventos(self):
        libro = []      # compras acumuladas (etiqueta, valor, fase)
        for e in self.g.eventos:
            tipo, a, kv = e['tipo'], e['args'], e['kv']
            t = self.tg_fin[e['idx']] + 0.05 if e.get('al_final') else self.t_palabra(e['idx'])
            b = self.bloque_en(t + 0.01)
            if tipo == 'sfx':
                for nombre in a or [kv.get('nombre', 'pop')]:
                    self.sfx.append((t, nombre, float(kv.get('vol', 1))))
                continue
            capa = {'tipo': tipo, 't0': t, 'kv': kv, 'args': a, 'bloque': b, 'al_final': e.get('al_final')}
            dur = float(kv.get('dur', DURACION.get(tipo, 3.0)))
            capa['t1'] = t + dur
            if tipo in ('precio',):
                etiqueta = a[0] if a else 'PRECIO'
                v = G.valor(a[1] if len(a) > 1 else kv.get('monto', 0))
                capa.update(etiqueta=etiqueta, valor=v)
                if kv.get('cuenta', 'si') != 'no':
                    libro.append((kv.get('item', etiqueta), v, kv.get('fase')))
            elif tipo == 'cuenta':
                capa['items'] = [(x[0], x[1]) for x in libro]
                if not libro:
                    self.avisos.append(f'línea {e["linea"]}: {{cuenta}} sin precios antes')
            elif tipo == 'total':
                fases = {}
                for et, v, fase in libro:
                    fases.setdefault(fase or et, 0)
                    fases[fase or et] += v
                capa['items'] = list(fases.items())
                capa['total'] = sum(v for _, v, _ in libro)
            elif tipo in ('img', 'clip'):
                capa['ruta'] = self._ruta(a[0]) if a else None
                capa['nombre'] = a[0] if a else '?'
            elif tipo == 'zoom':
                capa['t1'] = b['t1']
                capa['factor'] = float(a[0]) if a else 1.18
            self._sfx(tipo, t, kv)
            self.capas.append(capa)
        # cada slot: una capa termina cuando entra la siguiente del mismo slot o cambia el diseño
        for c in self.capas:
            if c['tipo'] in ('kill', 'hit', 'ping', 'flash', 'sacudir'):
                continue
            if not c['al_final']:  # lo que va al final de una frase puede quedarse un momento en el siguiente plano
                c['t1'] = min(c['t1'], c['bloque']['t1'])
            sig = [d['t0'] for d in self.capas if d is not c and SLOT.get(d['tipo']) == SLOT.get(c['tipo'])
                   and SLOT.get(c['tipo']) and d['t0'] > c['t0']]
            if sig:
                c['t1'] = min(c['t1'], min(sig) - 0.02)
            c['t1'] = min(c['t1'], self.dur)

    def resumen(self):
        out = []
        f = lambda t: f'{int(t // 60):02d}:{t % 60:05.2f}'
        for b in self.bloques:
            fondo = f' fondo={b["fondo"][2]}' if b['fondo'] else ''
            out.append(f'{f(b["t0"])}  ── [{b["layout"]}]{fondo}  zoom={b["zoom"]}')
            for c in self.capas:
                if c['bloque'] is b:
                    extra = c.get('etiqueta') or ' '.join(c['args'])
                    out.append(f'{f(c["t0"])}     {{{c["tipo"]}}} {extra}  → hasta {f(c["t1"])}')
        out.append('\nSonidos: ' + ', '.join(f'{f(t)} {n}' for t, n, _ in sorted(self.sfx)))
        return '\n'.join(out)

    # ---------- subtítulos ----------
    def grupos_subtitulos(self):
        ws = self.voz
        grupos, actual = [], []
        for i, w in enumerate(ws):
            if actual and (len(actual) >= 3 or w['s'] - actual[-1]['e'] > 0.35
                           or actual[-1]['w'][-1:] in '.,?!;:' or len(''.join(x['w'] for x in actual)) > 16):
                grupos.append(actual)
                actual = []
            actual.append(w)
        if actual:
            grupos.append(actual)
        out = []
        for k, gr in enumerate(grupos):
            fin = gr[-1]['e'] + 0.25
            if k + 1 < len(grupos):
                fin = min(fin, grupos[k + 1][0]['s'])
            out.append((gr[0]['s'] - 0.04, fin, gr))
        return out


class LectorVideo:
    """Lee cuadros RGB ya encuadrados a w×h desde ffmpeg (con bucle opcional)."""

    def __init__(self, ruta, w, h, fps, desde=0.0, bucle=False):
        from .tiempos import es_hdr, filtro_sdr
        self.ruta, self.w, self.h, self.fps, self.desde, self.bucle = ruta, w, h, fps, desde, bucle
        self.pre = filtro_sdr() if es_hdr(ruta) else ''  # video HDR del iPhone → colores normales
        self.ultimo = np.zeros((h, w, 3), np.uint8)
        self._abrir()

    def _abrir(self):
        vf = self.pre + f'scale={self.w}:{self.h}:force_original_aspect_ratio=increase,crop={self.w}:{self.h},setsar=1,fps={self.fps}'
        self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(self.desde), '-i', self.ruta, '-vf', vf, '-an',
                                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)

    def leer(self):
        n = self.w * self.h * 3
        buf = self.p.stdout.read(n)
        if len(buf) < n:
            if self.bucle:
                self.p.kill()
                self._abrir()
                buf = self.p.stdout.read(n)
            if len(buf) < n:
                return self.ultimo
        self.ultimo = np.frombuffer(buf, np.uint8).reshape(self.h, self.w, 3)
        return self.ultimo

    def cerrar(self):
        self.p.kill()


class Render:
    def __init__(self, proy, salida, crf=16, preset='slow', hasta=None, hoja=None):
        self.p, self.salida, self.crf, self.preset, self.hasta, self.hoja = proy, salida, crf, preset, hasta, hoja
        self.cache_img, self.cache_fondo, self.clips = {}, {}, {}
        self.subs = proy.grupos_subtitulos() if proy.subtitulos else []
        self.prev = None
        self.cuadro_trans = {}

    # ---------- fondos ----------
    def _region(self, layout):
        return {'mitad': (0, 0, W, H // 2), 'mitad-abajo': (0, H // 2, W, H // 2)}.get(layout, (0, 0, W, H))

    def fondo(self, b, t):
        x, y, w, h = self._region(b['layout'])
        f = b['fondo']
        if f and f[0] == 'clip' and f[1]:
            k = (b['idx'], w, h)
            if k not in self.clips:
                self.clips[k] = LectorVideo(f[1], w, h, self.p.fps, float(b['kv'].get('desde', 0)), bucle=True)
            return Image.fromarray(self.clips[k].leer())
        k = (b['idx'], w, h)
        if k not in self.cache_fondo:
            if f and f[1]:
                base = G.cubrir(Image.open(f[1]), int(w * 1.12), int(h * 1.12))
            elif f:
                base = G.marcador_imagen(f[2], w, h).convert('RGB').resize((int(w * 1.12), int(h * 1.12)))
            else:
                base = G.fondo_tactico(int(w * 1.12), int(h * 1.12))
            self.cache_fondo[k] = base
        base = self.cache_fondo[k]
        # Ken Burns: acercamiento lento, dirección alterna por bloque
        u = (t - b['t0']) / max(0.5, b['t1'] - b['t0'])
        z = 1.0 + 0.1 * G.ease_in_out(u) if b['idx'] % 2 == 0 else 1.1 - 0.1 * G.ease_in_out(u)
        cw, ch = base.width / (1.12 / 1.0) / z * 1.0, base.height / 1.12 / z
        cx = base.width / 2 + (u - 0.5) * (base.width - cw) * 0.4 * (1 if b['idx'] % 3 else -1)
        cy = base.height / 2
        caja = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        return base.resize((w, h), Image.BILINEAR, box=caja)

    def cara(self, src, zoom, region_h, cy_rel):
        """Recorte de tu cara: llena W×region_h con zoom alrededor de la altura de tus ojos."""
        ch = region_h / zoom
        cw = W / zoom
        cy = min(max(cy_rel * H, ch / 2), H - ch / 2)
        cx = W / 2
        return src.resize((W, region_h), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))

    def zoom_actual(self, b, t):
        z = b['zoom']
        for c in self.p.capas:
            if c['tipo'] == 'zoom' and c['bloque'] is b and c['t0'] <= t:
                z = max(z, 1.0) * 1.0 + (c['factor'] - 1.0) * G.ease_out((t - c['t0']) / 0.18)
        return z

    def base(self, src, b, t):
        lay = b['layout']
        if lay == 'cara':
            return self.cara(src, self.zoom_actual(b, t), H, self.p.cara_y)
        if lay == 'cubrir':
            return self.fondo(b, t)
        out = Image.new('RGB', (W, H))
        if lay == 'mitad':
            out.paste(self.fondo(b, t), (0, 0))
            out.paste(self.cara(src, 1.0 * self.zoom_actual(b, t), H // 2, self.p.cara_y + 0.06), (0, H // 2))
            self._costura(out, H // 2)
        elif lay == 'mitad-abajo':
            out.paste(self.cara(src, self.zoom_actual(b, t), H // 2, self.p.cara_y + 0.06), (0, 0))
            out.paste(self.fondo(b, t), (0, H // 2))
            self._costura(out, H // 2)
        elif lay == 'ventana':
            out.paste(self.fondo(b, t), (0, 0))
            d = 400
            c = self.cara(src, 1.0, H, self.p.cara_y)
            lado = int(W * 0.62)
            cy = int(self.p.cara_y * H)
            c = c.crop(((W - lado) // 2, cy - lado // 2, (W + lado) // 2, cy + lado // 2)).resize((d, d), Image.LANCZOS)
            m = Image.new('L', (d, d), 0)
            ImageDraw.Draw(m).ellipse([0, 0, d - 1, d - 1], fill=255)
            u = G.ease_out_back((t - b['t0']) / 0.35)
            dd = max(2, int(d * u))
            px, py = 60 + (d - dd) // 2, 1110 + (d - dd) // 2
            ImageDraw.Draw(out).ellipse([px - 9, py - 9, px + dd + 9, py + dd + 9], fill=G.NARANJA)
            out.paste(c.resize((dd, dd)), (px, py), m.resize((dd, dd)))
        return out

    @staticmethod
    def _costura(img, y):
        d = ImageDraw.Draw(img)
        d.rectangle([0, y - 5, W, y + 5], fill=G.NARANJA)
        for x in range(0, W, 60):
            d.polygon([(x, y - 5), (x + 30, y - 5), (x + 18, y + 5), (x - 12, y + 5)], fill=G.NEGRO)

    # ---------- capas ----------
    def _img(self, clave, fn):
        if clave not in self.cache_img:
            self.cache_img[clave] = fn()
        return self.cache_img[clave]

    def capa_img(self, c, t):
        tipo, kv, a = c['tipo'], c['kv'], c['args']
        mon = self.p.moneda
        u_cnt = G.ease_out((t - c['t0'] - 0.1) / 0.6)
        if tipo == 'precio':
            v = c['valor'] * u_cnt
            txt = G.dinero(v if u_cnt < 1 else c['valor'], mon)
            return self._img(('precio', c['etiqueta'], txt), lambda: G.tarjeta_precio(c['etiqueta'], txt))
        if tipo == 'titulo':
            return self._img(('titulo', a[0]), lambda: G.titulo(a[0]))
        if tipo == 'texto':
            return self._img(('texto', a[0]), lambda: G.barra_texto(a[0]))
        if tipo == 'cuenta':
            n = len(c['items'])
            return self._img(('cuenta', id(c)), lambda: G.informe(c['items'], n, mon))
        if tipo == 'total':
            u = G.ease_out((t - c['t0'] - 0.5) / 1.2)
            tt = G.dinero(round(c['total'] * u, 2) if u < 1 else c['total'], mon)
            return self._img(('total', id(c), tt), lambda: G.tabla_total(c['items'], tt, mon))
        if tipo == 'contador':
            meta = G.valor(a[1] if len(a) > 1 else 0)
            v = meta * u_cnt if u_cnt < 1 else meta
            txt = (kv.get('pre', '') + (f'{v:,.0f}' if meta >= 10 or u_cnt < 1 else f'{meta:g}') + kv.get('suf', ''))
            return self._img(('cont', a[0], txt), lambda: G.contador(a[0], txt))
        if tipo == 'barra':
            pct = G.valor(a[1] if len(a) > 1 else 100) * u_cnt
            return self._img(('barra', a[0], round(pct)), lambda: G.barra(a[0], pct))
        if tipo == 'sello':
            return self._img(('sello', a[0]), lambda: G.sello(a[0]))
        if tipo == 'tachar':
            return self._img(('tachar',), G.tachar)
        if tipo == 'img':
            if not c['ruta']:
                return self._img(('falta', c['nombre']),
                                 lambda: G.sombra(G.marcador_imagen(c['nombre'], 700, 520)))
            tam = int(kv.get('tam', 760))
            return self._img(('img', c['ruta'], tam), lambda: G.sticker(c['ruta'], tam, tam))
        if tipo == 'kill':
            return self._img(('kill', tuple(a)), lambda: G.killfeed(a[0] if a else 'TÚ', a[1] if len(a) > 1 else 'ENEMIGO'))
        if tipo == 'hit':
            return self._img(('hit',), G.hitmarker)
        if tipo == 'ping':
            return self._img(('ping', tuple(a)), lambda: G.ping(a[0] if a else 'ENEMIGO'))
        return None

    def componer_capas(self, frame, t, b):
        lay = b['layout']
        oscurecer = 0
        kills = 0
        for c in self.p.capas:
            if not (c['t0'] <= t < c['t1']):
                continue
            tipo = c['tipo']
            if tipo in ('zoom', 'flash', 'sacudir', 'clip'):
                continue
            if tipo in ('total', 'cuenta'):
                oscurecer = max(oscurecer, 0.55 * G.ease_out((t - c['t0']) / 0.3))
        if oscurecer:
            negro = Image.new('RGBA', frame.size, (0, 0, 0, int(255 * oscurecer)))
            frame.alpha_composite(negro)
        for c in self.p.capas:
            if not (c['t0'] <= t < c['t1']):
                continue
            tipo = c['tipo']
            if tipo in ('zoom', 'flash', 'sacudir', 'clip'):
                continue
            img = self.capa_img(c, t)
            if img is None:
                continue
            zona = ZONAS[c['bloque']['layout'] if tipo not in ('total', 'cuenta') else 'cara']
            dentro = (t - c['t0']) / T_ENTRA
            fuera = (c['t1'] - t) / T_SALE
            esc = G.ease_out_back(dentro) if tipo not in ('sello', 'hit') else 1.0
            alfa = min(1.0, dentro * 1.6, fuera)
            if fuera < 1:
                esc *= 0.85 + 0.15 * fuera
            if tipo == 'sello':
                esc = 2.4 - 1.4 * G.ease_out(dentro / 0.6)
            if tipo == 'hit':
                esc = 1.25 - 0.25 * G.ease_out(dentro * 2)
            if tipo == 'kill':
                x = int(-img.width + (img.width + 30) * G.ease_out(dentro))
                y = 240 + kills * 130
                kills += 1
                self._pegar(frame, img, x, y, alfa)
                continue
            if tipo in ('total', 'cuenta'):
                cx, cy, mw, mh = 540, 860, 1000, 1350
            elif tipo == 'hit':
                cx, cy, mw, mh = int(c['kv'].get('x', 540)), int(c['kv'].get('y', zona['arriba'][1] + 150)), 400, 400
            elif tipo == 'ping':
                cx = int(c['kv'].get('x', 540))
                cy = int(c['kv'].get('y', zona['arriba'][1])) + int(10 * math.sin((t - c['t0']) * 6))
                mw = mh = 600
            elif tipo == 'tachar':
                cx, cy, mw, mh = zona['arriba']
            else:
                cx, cy, mw, mh = zona[SLOT.get(tipo, 'arriba')]
            if 'y' in c['kv'] and tipo not in ('hit', 'ping'):
                cy = int(c['kv']['y'])
            f = min(1.0, mw / img.width, mh / img.height) * esc
            if tipo == 'img':
                f *= 1.0
                ang = float(c['kv'].get('giro', -4 if c['t0'] * 10 % 2 < 1 else 4))
                img2 = img.resize((max(1, int(img.width * f)), max(1, int(img.height * f))), Image.BILINEAR)
                img2 = img2.rotate(ang, expand=True, resample=Image.BICUBIC)
            elif abs(f - 1) > 0.01:
                img2 = img.resize((max(1, int(img.width * f)), max(1, int(img.height * f))), Image.BILINEAR)
            else:
                img2 = img
            self._pegar(frame, img2, int(cx - img2.width / 2), int(cy - img2.height / 2), alfa)

    @staticmethod
    def _pegar(frame, img, x, y, alfa):
        if alfa <= 0:
            return
        if alfa < 0.999:
            img = img.copy()
            img.putalpha(img.split()[3].point(lambda v: int(v * alfa)))
        # recorte manual para no salirnos del cuadro
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(W, x + img.width), min(H, y + img.height)
        if x1 <= x0 or y1 <= y0:
            return
        frame.alpha_composite(img.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))

    def componer_subs(self, frame, t, b):
        if any(c['tipo'] in ('total', 'cuenta') and c['t0'] <= t < c['t1'] for c in self.p.capas):
            return
        for s0, s1, gr in self.subs:
            if s0 <= t < s1:
                activa = max([i for i, w in enumerate(gr) if w['s'] - 0.05 <= t] or [0])
                img = self._img(('sub', s0, activa), lambda: G.subtitulo([w['w'].strip(' ,.?!¿¡') for w in gr], activa))
                u = G.ease_out_back((t - s0) / 0.14)
                if u < 0.999:
                    img = img.resize((max(1, int(img.width * u)), max(1, int(img.height * u))), Image.BILINEAR)
                y = ZONAS[b['layout']]['subs']
                self._pegar(frame, img, int(540 - img.width / 2), int(y - img.height / 2), 1.0)
                return

    # ---------- cuadro ----------
    def cuadro(self, src_arr, t):
        b = self.p.bloque_en(t)
        src = Image.fromarray(src_arr)
        frame = self.base(src, b, t).convert('RGBA')
        self.componer_capas(frame, t, b)
        self.componer_subs(frame, t, b)
        out = frame.convert('RGB')
        # transición al entrar a un bloque: barrido con línea naranja (o destello si cubre)
        dt = t - b['t0']
        if b['idx'] > 0 and dt < T_TRANS and self.prev is not None:
            u = G.ease_out(dt / T_TRANS)
            prev = self.prev
            if b['layout'] == 'cubrir':
                blanco = Image.new('RGB', (W, H), (255, 255, 255))
                out = Image.blend(out, blanco, 0.65 * (1 - u))
            else:
                y = int(H * u) if b['layout'] != 'cara' else int(H * (1 - u))
                mezcla = prev.copy()
                if b['layout'] != 'cara':
                    mezcla.paste(out.crop((0, 0, W, y)), (0, 0))
                else:
                    mezcla.paste(out.crop((0, y, W, H)), (0, y))
                ImageDraw.Draw(mezcla).rectangle([0, y - 7, W, y + 7], fill=G.NARANJA)
                out = mezcla
        else:
            self.prev = out
        # efectos de cámara
        for c in self.p.capas:
            if not (c['t0'] <= t < c['t1']):
                continue
            if c['tipo'] == 'flash':
                out = Image.blend(out, Image.new('RGB', (W, H), (255, 255, 255)), 0.8 * (1 - (t - c['t0']) / 0.28))
            elif c['tipo'] == 'sacudir':
                a = 26 * (1 - (t - c['t0']) / 0.4)
                dx, dy = random.uniform(-a, a), random.uniform(-a, a)
                out = out.transform(out.size, Image.AFFINE, (1, 0, dx, 0, 1, dy), resample=Image.BILINEAR)
        return out

    def correr(self, audio_wav):
        fps = self.p.fps
        dur = self.hasta or self.p.dur
        n = int(math.ceil(dur * fps))
        src = LectorVideo(self.p.video, W, H, fps)
        cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps),
               '-i', '-', '-i', audio_wav, '-map', '0:v', '-map', '1:a', '-t', f'{dur:.3f}',
               '-c:v', 'libx264', '-preset', self.preset, '-crf', str(self.crf), '-profile:v', 'high',
               '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
               '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000',
               '-movflags', '+faststart', self.salida]
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        muestras = []
        cada = int(fps * (self.hoja or 0)) or None
        for i in range(n):
            t = i / fps
            out = self.cuadro(src.leer(), t)
            enc.stdin.write(out.tobytes())
            if cada and i % cada == 0:
                muestras.append((t, out.resize((270, 480))))
            if i % (fps * 2) == 0:
                sys.stderr.write(f'\r  render {t:6.1f}s / {dur:.1f}s ({100 * i / n:4.0f}%)')
                sys.stderr.flush()
        enc.stdin.close()
        enc.wait()
        src.cerrar()
        for c in self.clips.values():
            c.cerrar()
        sys.stderr.write('\r  render listo.' + ' ' * 40 + '\n')
        if enc.returncode:
            raise RuntimeError('ffmpeg falló al codificar')
        if muestras:
            self._hoja(muestras)

    def _hoja(self, muestras):
        cols = 6
        filas = math.ceil(len(muestras) / cols)
        hoja = Image.new('RGB', (cols * 280, filas * 520), (20, 20, 20))
        d = ImageDraw.Draw(hoja)
        for k, (t, im) in enumerate(muestras):
            x, y = (k % cols) * 280 + 5, (k // cols) * 520 + 5
            hoja.paste(im, (x, y))
            d.text((x + 6, y + 486), f'{t:5.1f}s', font=G.fuente('bold', 24), fill=G.AMARILLO)
        ruta = os.path.splitext(self.salida)[0] + '-hoja.jpg'
        hoja.save(ruta, quality=88)
        print(f'  hoja de revisión: {ruta}')
