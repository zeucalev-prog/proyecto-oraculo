"""Lee un guion con marcas y lo convierte en palabras + eventos.

Formato (ver guiones/FORMATO.md):

    titulo: ¿Cuánto cuesta ser pay to win en Warzone?
    musica: musica/tension.mp3

    [cara]
    ¿Cuánto dinero real te costaría ser el jugador más pay to win de Warzone?

    [mitad img=pase.png]
    Primero el pase de batalla {precio "PASE DE BATALLA" 10} que cuesta diez dólares.

- Una línea entre [corchetes] cambia el DISEÑO de pantalla desde la siguiente palabra dicha.
- Un {evento} dentro del texto aparece justo cuando dices la palabra que le sigue.
- Las líneas que empiezan con # son comentarios (notas, prompts de imágenes, etc.).
"""
import re
import shlex
import unicodedata

LAYOUTS = {'cara', 'mitad', 'mitad-abajo', 'cubrir', 'ventana'}
EVENTOS = {'precio', 'titulo', 'texto', 'img', 'clip', 'kill', 'hit', 'ping', 'sfx', 'zoom', 'flash',
           'sacudir', 'cuenta', 'total', 'contador', 'barra', 'tachar', 'sello'}


def normalizar(palabra):
    s = unicodedata.normalize('NFKD', palabra.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s)


def _parse_args(texto):
    """'precio "PASE DE BATALLA" 10 sfx=caja' → ('precio', ['PASE DE BATALLA', '10'], {'sfx': 'caja'})"""
    partes = shlex.split(texto, posix=True)
    if not partes:
        raise ValueError('marca vacía')
    tipo, pos, kv = partes[0].lower(), [], {}
    for p in partes[1:]:
        if '=' in p and not p.startswith('='):
            k, v = p.split('=', 1)
            kv[k.lower()] = v
        else:
            pos.append(p)
    return tipo, pos, kv


class Guion:
    def __init__(self, ruta):
        self.ruta = ruta
        self.meta = {}
        self.palabras = []      # palabras dichas (texto original)
        self.bloques = []       # {'layout', 'args', 'kv', 'idx'}  idx = índice de la primera palabra
        self.eventos = []       # {'tipo', 'args', 'kv', 'idx', 'linea'}
        self._leer()

    def _leer(self):
        cuerpo = False
        with open(self.ruta, encoding='utf-8') as f:
            for n, linea in enumerate(f, 1):
                s = linea.strip()
                if not s or s.startswith('#'):
                    continue
                m = re.match(r'^([a-záéíóú_]+)\s*:\s*(.+)$', s, re.I)
                if not cuerpo and m and not s.startswith('['):
                    self.meta[m.group(1).lower()] = m.group(2).strip()
                    continue
                cuerpo = True
                if s.startswith('[') and s.endswith(']'):
                    tipo, pos, kv = _parse_args(s[1:-1])
                    if tipo not in LAYOUTS:
                        raise ValueError(f'línea {n}: diseño "{tipo}" no existe (usa: {", ".join(sorted(LAYOUTS))})')
                    self.bloques.append({'layout': tipo, 'args': pos, 'kv': kv, 'idx': len(self.palabras), 'linea': n})
                    continue
                self._texto(s, n)
        if not self.palabras:
            raise ValueError('el guion no tiene texto hablado')
        if not self.bloques or self.bloques[0]['idx'] > 0:
            self.bloques.insert(0, {'layout': 'cara', 'args': [], 'kv': {}, 'idx': 0, 'linea': 0})

    def _texto(self, s, n):
        pos = 0
        primero = len(self.eventos)
        for m in re.finditer(r'\{([^}]*)\}', s):
            self._palabras(s[pos:m.start()])
            tipo, args, kv = _parse_args(m.group(1))
            if tipo not in EVENTOS:
                raise ValueError(f'línea {n}: evento "{tipo}" no existe (usa: {", ".join(sorted(EVENTOS))})')
            self.eventos.append({'tipo': tipo, 'args': args, 'kv': kv, 'idx': len(self.palabras), 'linea': n})
            pos = m.end()
        self._palabras(s[pos:])
        # eventos al final de la línea: entran al terminar la última palabra (no en la línea siguiente)
        for e in self.eventos[primero:]:
            if e['idx'] == len(self.palabras) and self.palabras:
                e['idx'] -= 1
                e['al_final'] = True

    def _palabras(self, txt):
        for w in txt.split():
            if normalizar(w):
                self.palabras.append(w)
