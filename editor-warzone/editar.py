#!/usr/bin/env python3
"""Editor Oráculo · tu video hablando a cámara + guion con marcas → MP4 vertical listo para subir.

Uso básico:
    python editar.py mi_video.mp4 guiones/01-pay-to-win.guion

Opciones útiles:
    -o final.mp4          nombre de salida (por defecto: <video>-editado.mp4)
    --srt subs.srt        usa los tiempos de un SRT (CapCut/TikTok) en vez de Whisper
    --sin-whisper         reparte el guion sobre tus pausas (rápido, menos preciso)
    --modelo medium       modelo de Whisper (tiny/base/small/medium/large-v3). Default: small
    --musica pista.mp3    música de fondo (baja sola cuando hablas)
    --cara-y 0.40         altura de tus ojos en el cuadro (0 arriba, 1 abajo) para encuadrar la mitad de pantalla
    --sin-subtitulos      sin subtítulos dinámicos
    --previa 15           renderiza solo los primeros 15 s (para revisar rápido)
    --fps 30              cuadros por segundo de salida (default: los de tu video, máx. 60)
    --solo-plan           no renderiza: muestra la línea de tiempo (qué entra y cuándo)

Las imágenes y clips que nombra el guion se buscan junto al guion, en imagenes/ y en clips/.
"""
import argparse
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from oraculo.guion import Guion  # noqa: E402
from oraculo import tiempos, sonidos  # noqa: E402
from oraculo.render import Proyecto, Render  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description='Editor Oráculo: video a cámara + guion → MP4 editado')
    ap.add_argument('video')
    ap.add_argument('guion')
    ap.add_argument('-o', '--salida')
    ap.add_argument('--srt')
    ap.add_argument('--palabras', help='JSON de palabras con tiempos [{"w","s","e"}] (avanzado)')
    ap.add_argument('--sin-whisper', action='store_true')
    ap.add_argument('--modelo', default='small')
    ap.add_argument('--idioma', default='es')
    ap.add_argument('--musica')
    ap.add_argument('--vol-musica', type=float, default=0.16)
    ap.add_argument('--vol-sfx', type=float, default=0.7)
    ap.add_argument('--cara-y', type=float, default=0.40)
    ap.add_argument('--sin-subtitulos', action='store_true')
    ap.add_argument('--previa', type=float)
    ap.add_argument('--fps', type=int)
    ap.add_argument('--crf', type=int, default=16)
    ap.add_argument('--preset', default='slow')
    ap.add_argument('--hoja', type=float, default=1.5, help='segundos entre capturas de la hoja de revisión (0 = no)')
    ap.add_argument('--solo-plan', action='store_true')
    a = ap.parse_args()

    t_ini = time.time()
    g = Guion(a.guion)
    carpeta = os.path.dirname(os.path.abspath(a.guion))
    base = os.path.splitext(a.video)[0]
    salida = a.salida or base + '-editado.mp4'
    print(f'▶ Guion: {g.meta.get("titulo", os.path.basename(a.guion))}  ({len(g.palabras)} palabras, '
          f'{len(g.bloques)} cambios de pantalla, {len(g.eventos)} elementos)')

    # 1) tiempos de tu voz
    if a.palabras:
        import json
        voz = json.load(open(a.palabras, encoding='utf-8'))
        fuente = 'archivo de palabras'
    elif a.srt:
        voz, fuente = tiempos.leer_srt(a.srt), 'SRT'
    elif a.sin_whisper:
        voz, fuente = tiempos.repartir(g.palabras, a.video), 'reparto por pausas'
    else:
        try:
            print(f'▶ Transcribiendo con Whisper ({a.modelo})… la primera vez descarga el modelo.')
            voz = tiempos.transcribir(a.video, a.modelo, a.idioma, cache=base + '.palabras.json')
            fuente = 'Whisper'
        except ImportError:
            print('  (faster-whisper no está instalado: pip install faster-whisper) → uso reparto por pausas')
            voz, fuente = tiempos.repartir(g.palabras, a.video), 'reparto por pausas'
    tg, tg_fin, parecido = tiempos.alinear(g.palabras, voz)
    if fuente == 'reparto por pausas':
        print('▶ Sincronía aproximada (reparto por pausas): instala faster-whisper para precisión por palabra')
    else:
        print(f'▶ Sincronía ({fuente}): {parecido * 100:.0f}% de las palabras del guion encontradas en tu voz')
    if parecido < 0.5 and fuente != 'reparto por pausas':
        print('  ⚠ Coincide poco: ¿improvisaste mucho o es otro guion? Los elementos pueden caer desfasados.')

    # 2) línea de tiempo
    w, h, fps_src = tiempos.info_video(a.video)
    fps = a.fps or min(60, max(24, round(fps_src)))
    musica = a.musica or (os.path.join(carpeta, g.meta['musica']) if g.meta.get('musica') else None)
    if musica and not os.path.exists(musica):
        print(f'  ⚠ no encontré la música {musica}; sigo sin música')
        musica = None
    subs = not a.sin_subtitulos and g.meta.get('subtitulos', 'si').lower() not in ('no', 'false', '0')
    voz_subs = voz if fuente != 'reparto por pausas' else [{'w': p, 's': s, 'e': e} for p, s, e in zip(g.palabras, tg, tg_fin)]
    proy = Proyecto(g, tg, voz_subs, a.video, carpeta, fps, a.cara_y, subs, musica, tg_fin)
    plan = proy.resumen()
    with open(os.path.splitext(salida)[0] + '-plan.txt', 'w', encoding='utf-8') as f:
        f.write(plan)
    for av in proy.avisos:
        print('  ⚠', av)
    if a.solo_plan:
        print(plan)
        return

    # 3) audio: voz + efectos + música
    hdr = ' (HDR → convertido a SDR)' if tiempos.es_hdr(a.video) else ''
    print(f'▶ Video {w}×{h} @ {fps_src:.2f} fps{hdr} → salida 1080×1920 @ {fps} fps · {proy.dur:.1f}s')
    tmp = tempfile.mkdtemp(prefix='oraculo-')
    wav = os.path.join(tmp, 'mezcla.wav')
    sonidos.mezclar(a.video, proy.sfx, wav, proy.dur, musica, a.vol_musica, a.vol_sfx, os.path.join(carpeta, 'sfx'))

    # 4) render
    Render(proy, salida, a.crf, a.preset, a.previa, a.hoja or None).correr(wav)
    mb = os.path.getsize(salida) / 1e6
    print(f'✔ Listo: {salida}  ({mb:.1f} MB, {time.time() - t_ini:.0f}s)')


if __name__ == '__main__':
    main()
