"""HU-010: consultar el detalle de un bloque horario."""
from core.bloques import elegir_bloque, etiqueta_bloque, ventas_de
from core.utilidades import dinero, titulo


def detalle_bloque(d):
    titulo("Detalle de un bloque horario")
    clave = elegir_bloque(d)
    if not clave:
        return
    b = d["bloques"][clave]
    vs = ventas_de(d, clave)
    print(f"\n  Bloque: {etiqueta_bloque(clave, b)}  ({'cerrado' if b['cerrado'] else 'abierto'})")
    print(f"  Efectivo inicial: {dinero(b['efectivo_inicial'])}")
    if not vs:
        print("  (sin ventas en este bloque)")
    for v in vs:
        print(f"\n  Venta #{v['id']}  {v['fecha'][11:]}  recibido {dinero(v['recibido'])}"
              f"  vueltas {dinero(v['vueltas'])}")
        for i in v["items"]:
            print(f"     {i['cantidad']} x {i['nombre'][:24]:<24} {dinero(i['precio'] * i['cantidad']):>12}")
        print(f"     {'Total':<28}{dinero(v['total']):>12}")
    total = sum(v["total"] for v in vs)
    print(f"\n  Total vendido: {dinero(total)}  |  Esperado en caja: {dinero(b['efectivo_inicial'] + total)}")
    if b["cerrado"]:
        print(f"  Contado: {dinero(b['efectivo_contado'])}  |  Diferencia: {dinero(b['diferencia'])}")
