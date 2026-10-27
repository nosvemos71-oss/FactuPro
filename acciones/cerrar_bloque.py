"""Cerrar bloque: registra la hora de cierre, detecta descuadres y muestra un informe."""
from datetime import datetime

from core.almacenamiento import guardar
from core.bloques import FORMATO, elegir_bloque, etiqueta_bloque, ventas_de
from core.utilidades import dinero, pedir_entero, titulo


def _duracion(inicio, fin):
    seg = int((datetime.strptime(fin, FORMATO) - datetime.strptime(inicio, FORMATO)).total_seconds())
    h, resto = divmod(seg, 3600)
    return f"{h}h {resto // 60:02d}min"


def cerrar_bloque(d):
    titulo("Cerrar bloque")
    abiertos = sorted(k for k, b in d["bloques"].items() if not b["cerrado"])
    if not abiertos:
        print("  ! No hay ningun bloque abierto. Abre uno con 'Abrir bloque'.")
        return
    clave = abiertos[0] if len(abiertos) == 1 else elegir_bloque(d, solo_abiertos=True)
    if not clave:
        return
    b = d["bloques"][clave]
    vs = ventas_de(d, clave)
    total = sum(v["total"] for v in vs)
    esperado = b["efectivo_inicial"] + total

    print(f"\n  Bloque           : {etiqueta_bloque(clave, b)}")
    print(f"  Efectivo inicial : {dinero(b['efectivo_inicial'])}")
    print(f"  Ventas ({len(vs)})     : {dinero(total)}")
    print(f"  Efectivo esperado: {dinero(esperado)}")
    contado = pedir_entero("  Efectivo contado en caja: ", 0)
    dif = contado - esperado

    ahora = datetime.now()
    if b.get("apertura"):  # el cierre nunca puede quedar antes de la apertura
        ahora = max(ahora, datetime.strptime(b["apertura"], FORMATO))
    cierre = ahora.strftime(FORMATO)
    b.update(cerrado=True, cierre=cierre, efectivo_contado=contado,
             esperado=esperado, diferencia=dif)
    guardar(d)

    unidades = sum(i["cantidad"] for v in vs for i in v["items"])
    ini = b.get("apertura")
    titulo("INFORME DE CIERRE")
    print(f"  Apertura         : {ini[11:19] if ini else '-'}")
    print(f"  Cierre           : {cierre[11:19]}")
    if ini:
        print(f"  Duracion         : {_duracion(ini, cierre)}")
    print(f"  Efectivo inicial : {dinero(b['efectivo_inicial'])}")
    print(f"  Ventas           : {len(vs)} ({unidades} unidades)")
    print(f"  Total vendido    : {dinero(total)}")
    print(f"  Efectivo esperado: {dinero(esperado)}")
    print(f"  Efectivo contado : {dinero(contado)}")
    if dif == 0:
        print("  Resultado        : ✓ CAJA CUADRADA")
    elif dif > 0:
        print(f"  Resultado        : ⚠ DESCUADRE, sobrante de {dinero(dif)}")
    else:
        print(f"  Resultado        : ⚠ DESCUADRE, faltante de {dinero(-dif)}")
