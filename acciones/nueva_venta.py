"""HU-004, 005, 006, 007: registrar venta, vueltas, descontar inventario, bloque."""
from datetime import datetime

from acciones.abrir_bloque import abrir_bloque
from acciones.consultar_productos import consultar_productos
from core.almacenamiento import guardar
from core.bloques import bloque_abierto
from core.utilidades import confirmar, dinero, pedir_entero, titulo


def _total(d, carrito):
    return sum(d["productos"][c]["precio"] * q for c, q in carrito.items())


def nueva_venta(d, usuario):
    titulo("Nueva venta")
    if not d["productos"]:
        print("  ! No hay productos registrados.")
        return
    ahora = datetime.now()
    clave, _ = bloque_abierto(d)
    if clave is None:
        print("  ! No hay un bloque abierto, no se puede vender.")
        if not confirmar("  ¿Abrir un bloque ahora?"):
            return
        abrir_bloque(d)
        clave, _ = bloque_abierto(d)
        if clave is None:
            return

    carrito = {}  # codigo -> cantidad
    while True:
        if carrito:
            print("\n  Carrito:")
            for c, q in carrito.items():
                p = d["productos"][c]
                print(f"   {q} x {p['nombre'][:24]:<24} {dinero(p['precio'] * q):>12}")
            print(f"   {'TOTAL':<30}{dinero(_total(d, carrito)):>12}")
        c = input("\nCodigo (Enter = terminar, ? = buscar, x = cancelar): ").strip().upper()
        if c == "X":
            print("  Venta cancelada.")
            return
        if c == "?":
            consultar_productos(d)
            continue
        if c == "":
            if carrito:
                break
            print("  ! Agrega al menos un producto o escribe x para cancelar.")
            continue
        p = d["productos"].get(c)
        if not p:
            print("  ! Producto no encontrado.")
            continue
        disp = p["stock"] - carrito.get(c, 0)
        if disp <= 0:
            print("  ! Sin existencias disponibles.")
            continue
        q = pedir_entero(f"  {p['nombre']} ({dinero(p['precio'])}, disp. {disp}) cantidad: ", 1, disp)
        carrito[c] = carrito.get(c, 0) + q

    total = _total(d, carrito)
    print(f"\n  TOTAL A COBRAR: {dinero(total)}")
    recibido = pedir_entero("  Dinero recibido: ", total)  # HU-005
    vueltas = recibido - total
    print(f"  VUELTAS: {dinero(vueltas)}")
    if not confirmar("  ¿Confirmar venta?"):
        print("  Venta cancelada.")
        return

    items = []
    for c, q in carrito.items():
        p = d["productos"][c]
        p["stock"] -= q  # HU-006
        items.append({"codigo": c, "nombre": p["nombre"], "cantidad": q, "precio": p["precio"]})
    d["ventas"].append({
        "id": len(d["ventas"]) + 1, "fecha": ahora.strftime("%Y-%m-%d %H:%M:%S"),
        "bloque": clave, "items": items, "total": total,
        "recibido": recibido, "vueltas": vueltas, "usuario": usuario})
    guardar(d)
    print(f"  ✓ Venta #{d['ventas'][-1]['id']} registrada.")
