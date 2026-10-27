"""Abrir bloque: guarda la hora de apertura y el dinero con el que arranca la caja.

Las ventas que se registren mientras el bloque este abierto quedan asociadas
a el (campo "bloque" de cada venta).
"""
from datetime import datetime, timedelta

from core.almacenamiento import guardar
from core.bloques import bloque_abierto, clave_bloque, etiqueta_bloque, ventas_de
from core.utilidades import confirmar, dinero, pedir_entero, titulo


def _efectivo_ultimo_cierre(d):
    cerrados = [k for k, b in d["bloques"].items()
                if b["cerrado"] and b.get("efectivo_contado") is not None]
    return d["bloques"][max(cerrados)]["efectivo_contado"] if cerrados else None


def abrir_bloque(d):
    titulo("Abrir bloque")
    clave, b = bloque_abierto(d)
    if clave:
        n = len(ventas_de(d, clave))
        print(f"  Ya hay un bloque abierto: {etiqueta_bloque(clave, b)}")
        print(f"  Efectivo inicial: {dinero(b['efectivo_inicial'])}  |  Ventas registradas: {n}")
        if n == 0 and confirmar("  ¿Corregir el efectivo inicial?"):
            b["efectivo_inicial"] = pedir_entero("Nuevo efectivo inicial: ", 0)
            guardar(d)
            print("  ✓ Corregido.")
        else:
            print("  Para abrir uno nuevo, primero cierra este (Cerrar bloque).")
        return

    sugerido = _efectivo_ultimo_cierre(d)
    if sugerido is None:
        inicial = pedir_entero("Dinero actual en caja: ", 0)
    else:
        print(f"  Efectivo contado al cerrar el bloque anterior: {dinero(sugerido)}")
        inicial = pedir_entero(f"Dinero actual en caja (Enter = {dinero(sugerido)}): ",
                               0, vacio_ok=True)
        if inicial is None:
            inicial = sugerido

    ahora = datetime.now()
    while clave_bloque(ahora) in d["bloques"]:
        ahora += timedelta(seconds=1)
    clave = clave_bloque(ahora)
    d["bloques"][clave] = {
        "apertura": clave, "cierre": None, "efectivo_inicial": inicial,
        "cerrado": False, "efectivo_contado": None, "esperado": None, "diferencia": None}
    guardar(d)
    print(f"  ✓ Bloque abierto a las {clave[11:19]} con {dinero(inicial)} en caja.")
