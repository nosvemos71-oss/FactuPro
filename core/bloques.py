"""Utilidades para trabajar con bloques de caja.

Un bloque se abre y se cierra de forma explicita (ya no depende de la hora
del reloj). La clave del bloque es su fecha y hora de apertura.
"""
from core.utilidades import pedir_entero

FORMATO = "%Y-%m-%d %H:%M:%S"


def clave_bloque(dt):
    return dt.strftime(FORMATO)


def etiqueta_bloque(clave, b=None):
    """Texto tipo '2026-10-27 08:00:00-09:15:30' (o 'en curso' si sigue abierto)."""
    b = b or {}
    if len(clave) == 13:  # formato antiguo: un bloque por hora del reloj
        h = int(clave[-2:])
        return f"{clave[:10]} {h:02d}:00-{h:02d}:59"
    if b.get("cierre"):
        fin = b["cierre"][11:19]
    else:
        fin = "en curso" if not b.get("cerrado") else "?"
    return f"{clave[:10]} {clave[11:19]}-{fin}"


def ventas_de(d, clave):
    return [v for v in d["ventas"] if v["bloque"] == clave]


def bloque_abierto(d):
    """Devuelve (clave, bloque) del bloque abierto, o (None, None)."""
    abiertos = sorted(k for k, b in d["bloques"].items() if not b["cerrado"])
    if not abiertos:
        return None, None
    return abiertos[-1], d["bloques"][abiertos[-1]]


def elegir_bloque(d, solo_abiertos=False):
    claves = sorted(k for k, b in d["bloques"].items()
                    if not (solo_abiertos and b["cerrado"]))
    if not claves:
        print("  No hay bloques disponibles.")
        return None
    for i, k in enumerate(claves, 1):
        b = d["bloques"][k]
        est = "cerrado" if b["cerrado"] else "abierto"
        print(f"  {i}) {etiqueta_bloque(k, b)} [{est}]")
    n = pedir_entero("Numero de bloque: ", 1, len(claves))
    return claves[n - 1]
