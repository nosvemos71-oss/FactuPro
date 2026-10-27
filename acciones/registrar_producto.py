"""HU-001: registrar productos."""
from core.almacenamiento import guardar
from core.utilidades import confirmar, dinero, pedir_entero, pedir_texto, titulo


def registrar_producto(d):
    titulo("Registrar producto")
    codigo = pedir_texto("Codigo: ").upper()
    if codigo in d["productos"]:
        print("  ! Ya existe un producto con ese codigo.")
        return
    nombre = pedir_texto("Nombre: ")
    if any(p["nombre"].lower() == nombre.lower() for p in d["productos"].values()):
        if not confirmar("  Ya existe un producto con ese nombre. ¿Continuar?"):
            return
    precio = pedir_entero("Precio: ", minimo=1)
    stock = pedir_entero("Existencias iniciales: ", minimo=0)
    d["productos"][codigo] = {"nombre": nombre, "precio": precio, "stock": stock}
    guardar(d)
    print(f"  ✓ Producto registrado: {nombre} ({dinero(precio)}, stock {stock}).")
