---
name: editor-warzone
description: Edita un video hablando a cámara (talking head) de la persona con el Editor Oráculo: lo sincroniza con un guion con marcas y le pone pantalla dividida, imágenes que la tapan, tarjetas de precio, cuentas, total, killfeed, sonidos y subtítulos, y entrega un MP4 vertical listo para subir. Úsalo cuando pida "edita mi video", "aplícalo a IMG_xxxx.MOV", "ponle los elementos a mi grabación", escribir un guion de Warzone con marcas, o transcribir una toma.
---

# Editor Warzone (Editor Oráculo)

La herramienta vive en `editor-warzone/` de este repo. Lee `editor-warzone/LEEME.md` (uso), `editor-warzone/guiones/FORMATO.md` (sintaxis de marcas) y `editor-warzone/PLAN.md` (estilo y reglas del canal) antes de escribir un guion. No reescribas el motor: si algo falla, arréglalo en `editor-warzone/oraculo/`.

## Flujo cuando la persona da un video

1. **Encontrar el video en el PC.** Si solo da el nombre (p. ej. `IMG_8139.MOV`), búscalo. En Windows (PowerShell):
   ```powershell
   Get-ChildItem -Path $env:USERPROFILE -Recurse -Filter "IMG_8139*" -ErrorAction SilentlyContinue | Select-Object FullName, Length, LastWriteTime
   ```
   Lugares típicos: Escritorio, Descargas, Videos, Imágenes, `Pictures\iCloud Photos\Photos`, OneDrive. En Mac/Linux: `find ~ -iname "IMG_8139*" 2>/dev/null`. Si hay varios, pregunta cuál. No muevas ni borres el original: trabaja con una copia en una carpeta de proyecto (`editor-warzone/proyectos/<nombre>/`).

2. **Dependencias (una vez).** `python --version` (3.10+), `ffmpeg -version` (si falta en Windows: `winget install ffmpeg`, y reabrir la terminal), luego `pip install -r editor-warzone/requirements.txt`.

3. **¿Qué dice en el video?**
   - Si leyó uno de `editor-warzone/guiones/*.guion`, cópialo a la carpeta del proyecto.
   - Si no (improvisó u otro texto): `python editor-warzone/transcribir.py <video>` → lee el `.txt` y escribe un guion nuevo **con sus palabras exactas** (no las corrijas: la sincronía depende de eso) y añade marcas siguiendo `FORMATO.md` y las reglas de `PLAN.md`: un cambio de pantalla `[ ]` cada 1–3 frases, un `{elemento}` cada 2–3 s, precios con `fase=` si hay costeo, `{total}` al final si hay precios, gancho en `[cara zoom]`, cierre en `[cara]`. Muestra el guion a la persona en 5–10 líneas de resumen antes de renderizar si hay dudas sobre cifras.

4. **Imágenes.** Las que nombra el guion van en `<proyecto>/imagenes/`. Si la persona aún no las tiene, renderiza igual (salen tarjetas "FALTA IMAGEN" visibles) y dale la lista de prompts del guion para generarlas. Puede reutilizar capturas o clips de gameplay propios (`clip=`).

5. **Plan y previa.**
   ```bash
   python editor-warzone/editar.py <video> <proyecto>/<guion>.guion --solo-plan
   python editor-warzone/editar.py <video> <proyecto>/<guion>.guion --previa 20 --preset veryfast
   ```
   Revisa la sincronía (debe decir ≥ 80 %), abre `*-hoja.jpg` y mira: texto encima de la cara, elementos cortados, subtítulos tapados. Si la cara no queda bien en `[mitad]`, ajusta `--cara-y` (altura de los ojos, 0–1; mide en un cuadro: `ffmpeg -ss 2 -i <video> -frames:v 1 cuadro.png`).

6. **Render final.**
   ```bash
   python editor-warzone/editar.py <video> <proyecto>/<guion>.guion -o <proyecto>/<nombre>-final.mp4
   ```
   Sale a 1080×1920, H.264 CRF 16 y −14 LUFS. Los videos HDR del iPhone se convierten solos a SDR. Dale a la persona la ruta del MP4 y la hoja de revisión, y ofrece un caption con gancho + pregunta para comentar + hashtags.

## Reglas
- Datos: solo cifras con fuente o dichas como estimado ("más o menos"). Nada de precios de armas reales ni de logos oficiales de Call of Duty en imágenes.
- No subas videos ni imágenes de la persona al repo (`proyectos/` está en `.gitignore`).
