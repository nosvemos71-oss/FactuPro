"""HU-002: consultar y buscar productos."""
from core.utilidades import dinero, titulo


def listar_productos(productos):
    if not productos:
        print("  (sin resultados)")
        return
    print(f"{'CODIGO':<10}{'NOMBRE':<28}{'PRECIO':>12}{'STOCK':>8}")
    print("-" * 58)
    for c, p in sorted(productos.items()):
        aviso = "  ⚠ agotado" if p["stock"] == 0 else ""
        print(f"{c:<10}{p['nombre'][:27]:<28}{dinero(p['precio']):>12}{p['stock']:>8}{aviso}")


def consultar_productos(d):
    titulo("Consultar / buscar productos")
    q = input("Buscar por codigo o nombre (Enter = todos): ").strip().lower()
    res = {c: p for c, p in d["productos"].items()
           if not q or q in c.lower() or q in p["nombre"].lower()}
    listar_productos(res)
