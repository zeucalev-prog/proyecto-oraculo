# Cómo se escribe un guion para el Editor Oráculo

Tú solo lees el texto a cámara. Las marcas no se dicen: le indican al editor qué poner en pantalla y cuándo.

```
titulo: ¿Cuánto cuesta ser el más pay to win de Warzone?
moneda: $
musica: musica/tension.mp3        # opcional
subtitulos: si                    # si / no

# Las líneas con # son notas: no se leen ni se muestran.

[cara]
¿Cuánto dinero real necesitas para ser el jugador más pay to win de Warzone?

[mitad img=pase.png]
Círculo uno: el pase de batalla {precio "PASE DE BATALLA" 9.99 fase="EL PASE"} cuesta mil cien COD Points.
```

## 1 · Diseños de pantalla: `[corchetes]` en su propia línea
Cambian lo que se ve desde la **siguiente palabra que dices** hasta el siguiente corchete.

| Marca | Qué se ve |
|---|---|
| `[cara]` | Tú a pantalla completa. Alterna solo entre plano normal y plano cerrado para que se sienta editado. `[cara zoom]` = plano muy cerrado; `[cara fijo]` = sin alternar. |
| `[mitad img=x.png]` | Imagen arriba y tú abajo, en la mitad de la pantalla. Sin `img` sale un fondo de mapa táctico. |
| `[mitad-abajo img=x.png]` | Tú arriba y la imagen abajo. |
| `[cubrir img=x.png]` | La imagen te tapa por completo (con destello de entrada). |
| `[ventana img=x.png]` | Imagen a pantalla completa y tú en un círculo pequeño. |
| `clip=x.mp4` en lugar de `img=` | Un video de fondo, como gameplay o una animación hecha con la skill pizarra. `desde=12` empieza en el segundo 12. |

Extras: `sfx=nombre` cambia el sonido de la transición y `sfx=no` lo quita.

## 2 · Elementos: `{llaves}` dentro del texto
Aparecen **justo cuando dices la palabra que va después de la llave**.

| Marca | Qué hace | Sonido por defecto |
|---|---|---|
| `{precio "ETIQUETA" 19.99}` | Tarjeta con conteo hasta el monto. Se suma sola a tu cuenta. `fase="NOMBRE"` agrupa el precio en el total; `cuenta=no` hace que no sume. | caja registradora |
| `{cuenta}` | Muestra el informe de gastos acumulado hasta ese momento. | teclado |
| `{total}` | Tabla final por fases con el TOTAL. **Se calcula solo, sin errores de suma.** | subida + caja |
| `{titulo "TEXTO con *resaltado*"}` | Titular grande. Las palabras entre asteriscos van sobre una caja naranja. | impacto |
| `{texto "3 BUNDLES AL MES"}` | Rótulo amarillo a media pantalla. | whoosh |
| `{img archivo.png}` | Imagen tipo sticker con borde blanco, que entra con rebote. `tam=600`, `giro=5`. | pop |
| `{contador "HORAS JUGADAS" 730}` | Número grande que cuenta hacia arriba. `pre="$"` y `suf=" h"` añaden texto antes y después. | teclado + ding |
| `{barra "VIDA" 35}` | Barra de progreso al porcentaje indicado. | subida |
| `{kill "TÚ" "TU CARTERA"}` | Notificación de baja en la esquina superior. | disparo + hitmarker |
| `{hit}` | Hitmarker en pantalla. | hit |
| `{ping "ENEMIGO"}` | Marcador rojo flotante. Admite `x=540` e `y=700`. | bip |
| `{sello "CONFIRMADO"}` | Sello que cae de golpe. | impacto |
| `{tachar}` | X roja sobre la tarjeta de arriba. | error |
| `{zoom}` | Acercamiento rápido a tu cara (hasta que cambie el diseño). | whoosh suave |
| `{flash}` / `{sacudir}` | Destello blanco / sacudida de cámara. | glitch / explosión |
| `{sfx caja}` | Solo un sonido. | — |

Cualquier elemento acepta `sfx=otro`, `sfx=no`, `vol=0.5` y `dur=2.5`.

**Sonidos disponibles:** whoosh, whoosh-abajo, pop, caja, moneda, disparo, recarga, hit, uav, bip, impacto, explosion, subida, ding, teclado, error, glitch, tic.
Para usar tus propios sonidos, pon `sfx/caja.wav` junto al guion y reemplazará al sintetizado.

## 3 · Archivos
```
mi-video/
├── 01-pay-to-win.guion
├── imagenes/   pase.png, bundles.png …   (las que nombra el guion)
├── clips/      gameplay.mp4 …
├── sfx/        (opcional) tus propios sonidos
└── musica/     (opcional)
```
Si falta una imagen, el video se renderiza igual, con una tarjeta naranja que dice **FALTA IMAGEN: nombre**, para que la detectes en la hoja de revisión.

## 4 · Consejos para grabar
- Graba en vertical, a 1080×1920 o más, con buena luz. Deja tus ojos a ~40 % de la altura del cuadro (si quedan en otra altura, usa `--cara-y 0.35`).
- Lee el guion tal cual. Si improvisas un poco no pasa nada: la sincronía tolera cambios y los marca.
- Si te equivocas, repite la frase completa y corta el error antes de pasarlo al editor (o pásalo así; Whisper y la alineación absorben repeticiones cortas).
- Habla con energía en el primer segundo: el gancho es la primera frase, sin "hola, ¿qué tal?".
