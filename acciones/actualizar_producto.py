"""HU-003: actualizar existencias y precios."""
from core.almacenamiento import guardar
from core.utilidades import dinero, pedir_entero, pedir_texto, titulo


def actualizar_producto(d):
    titulo("Actualizar existencias y precios")
    codigo = pedir_texto("Codigo del producto: ").upper()
    p = d["productos"].get(codigo)
    if not p:
        print("  ! Producto no encontrado.")
        return
    print(f"  {p['nombre']} | precio {dinero(p['precio'])} | stock {p['stock']}")
    precio = pedir_entero("Nuevo precio (Enter = sin cambio): ", 1, vacio_ok=True)
    print("Existencias: 1) Reemplazar total  2) Sumar entrada  Enter) sin cambio")
    op = input("Opcion: ").strip()
    if op == "1":
        p["stock"] = pedir_entero("Nuevo total: ", 0)
    elif op == "2":
        p["stock"] += pedir_entero("Unidades a sumar: ", 1)
    if precio is not None:
        p["precio"] = precio
    guardar(d)
    print(f"  ✓ Actualizado: precio {dinero(p['precio'])}, stock {p['stock']}")
