"""HU-012: guardar y cargar la informacion del sistema en datos.json."""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO = os.path.join(RAIZ, "datos.json")


def datos_vacios():
    return {"productos": {}, "ventas": [], "bloques": {}}


def cargar():
    if not os.path.exists(ARCHIVO):
        return datos_vacios()
    try:
        with open(ARCHIVO, encoding="utf-8") as f:
            d = json.load(f)
        for k, v in datos_vacios().items():
            d.setdefault(k, v)
        return d
    except (json.JSONDecodeError, OSError):
        print(f"! No se pudo leer {ARCHIVO}. Se guarda una copia y se inicia vacio.")
        try:
            os.replace(ARCHIVO, ARCHIVO + ".danado")
        except OSError:
            pass
        return datos_vacios()


def guardar(d):
    tmp = ARCHIVO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ARCHIVO)  # escritura atomica
