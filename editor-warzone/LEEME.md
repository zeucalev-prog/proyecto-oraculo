# Editor Oráculo · video a cámara + guion → MP4 editado

Le das **tu video hablando** y el **guion con marcas**. Te devuelve el MP4 vertical (1080×1920) con imágenes, pantalla dividida, tarjetas de precio, cuentas, efectos de sonido y subtítulos dinámicos, todo sincronizado con tu voz.

Estrategia, formatos virales y banco de ideas: **[PLAN.md](PLAN.md)** · Cómo escribir un guion: **[guiones/FORMATO.md](guiones/FORMATO.md)**

## Instalar (una vez)
1. **Python 3.10+** → https://www.python.org (en Windows marca "Add to PATH").
2. **ffmpeg** → Windows: `winget install ffmpeg` · Mac: `brew install ffmpeg`.
3. En esta carpeta: `pip install -r requirements.txt`

## Usar
```bash
python editar.py mi_toma.mp4 guiones/01-pay-to-win.guion
```
Las imágenes que nombra el guion van en `guiones/imagenes/` (junto al guion). Salen tres archivos:
- `mi_toma-editado.mp4` → listo para subir
- `mi_toma-editado-hoja.jpg` → capturas cada 1.5 s para revisar de un vistazo
- `mi_toma-editado-plan.txt` → qué entra y en qué segundo

La primera vez Whisper descarga su modelo (~500 MB para `small`). Después funciona sin internet.

### Opciones
| Opción | Para qué |
|---|---|
| `--previa 15` | Renderiza solo los primeros 15 s (prueba rápida). |
| `--solo-plan` | Muestra la línea de tiempo sin renderizar. |
| `--srt subs.srt` | Usa los subtítulos de CapCut/TikTok en vez de Whisper. |
| `--sin-whisper` | Reparte el guion según tus pausas (sin instalar Whisper; menos preciso). |
| `--modelo medium` | Whisper más preciso (más lento). |
| `--musica pista.mp3` | Música de fondo, que baja sola cuando hablas. |
| `--cara-y 0.35` | Altura de tus ojos en el cuadro (para encuadrar la pantalla dividida). |
| `--sin-subtitulos` | Sin subtítulos dinámicos. |
| `--fps 30` | Cuadros por segundo de salida (por defecto, los de tu video). |

## Probar sin grabarte
```bash
python demo/hacer_demo.py guiones/01-pay-to-win.guion demo/salida      # requiere espeak-ng
python editar.py demo/salida/presentador-prueba.mp4 demo/salida/01-pay-to-win.guion --srt demo/salida/voz.srt
```

## Estructura
```
editar.py            ← el comando
transcribir.py       ← transcribe una toma improvisada (para escribir su guion)
oraculo/guion.py     ← lee las marcas [diseño] y {elemento}
oraculo/tiempos.py   ← Whisper / SRT / pausas + alineación guion↔voz
oraculo/graficos.py  ← tarjetas, informe, total, killfeed, subtítulos… (estilo HUD táctico)
oraculo/sonidos.py   ← 18 efectos sintetizados + mezcla con la voz y la música
oraculo/render.py    ← línea de tiempo y composición cuadro a cuadro
fuentes/             ← Anton, Bebas Neue, Montserrat (OFL) y DejaVu Mono
guiones/             ← formato + 3 guiones listos para grabar
```

## Usarlo con Claude en tu PC
Este repo trae la skill `.claude/skills/editor-warzone`. Abre Claude Code (Claude Desktop o `claude` en una terminal) **dentro de la carpeta del repo** y pídele: *"Edita mi video IMG_8139.MOV con el editor de Warzone"*. Claude buscará el video en tu PC, instalará lo que falte, escribirá o elegirá el guion y te entregará el MP4.
