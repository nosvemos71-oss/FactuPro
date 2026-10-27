"""HU-011: generar resumen diario."""
from datetime import datetime

from core.bloques import etiqueta_bloque, ventas_de
from core.utilidades import dinero, titulo


def resumen_diario(d):
    titulo("Resumen diario")
    hoy = datetime.now().strftime("%Y-%m-%d")
    dia = input(f"Fecha AAAA-MM-DD (Enter = {hoy}): ").strip() or hoy
    try:
        datetime.strptime(dia, "%Y-%m-%d")
    except ValueError:
        print("  ! Fecha invalida.")
        return
    vs = [v for v in d["ventas"] if v["fecha"].startswith(dia)]
    bloques = sorted(k for k in d["bloques"] if k.startswith(dia))
    if not vs and not bloques:
        print("  No hay informacion para esa fecha.")
        return
    print(f"\n  {'BLOQUE':<20}{'VENTAS':>7}{'TOTAL':>14}{'DIFERENCIA':>14}")
    print("  " + "-" * 55)
    for k in bloques:
        b = d["bloques"][k]
        vb = ventas_de(d, k)
        dif = dinero(b["diferencia"]) if b["cerrado"] else "abierto"
        etq = etiqueta_bloque(k, b)[11:]
        print(f"  {etq:<20}{len(vb):>7}{dinero(sum(v['total'] for v in vb)):>14}{dif:>14}")
    print(f"\n  Numero de ventas : {len(vs)}")
    print(f"  Total vendido    : {dinero(sum(v['total'] for v in vs))}")
    descuadre = sum(d["bloques"][k]["diferencia"] for k in bloques if d["bloques"][k]["cerrado"])
    print(f"  Descuadre neto   : {dinero(descuadre)}")
    abiertos = [k for k in bloques if not d["bloques"][k]["cerrado"]]
    if abiertos:
        print(f"  ⚠ Bloques sin cerrar: {len(abiertos)}")
    vendidos = {}
    for v in vs:
        for i in v["items"]:
            x = vendidos.setdefault(i["nombre"], [0, 0])
            x[0] += i["cantidad"]
            x[1] += i["cantidad"] * i["precio"]
    if vendidos:
        print("\n  Productos vendidos:")
        for n, (q, t) in sorted(vendidos.items(), key=lambda kv: -kv[1][1]):
            print(f"   {q:>4} x {n[:28]:<28}{dinero(t):>12}")
