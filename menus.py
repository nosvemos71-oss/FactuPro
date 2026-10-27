"""Submenus del sistema."""
from acciones.actualizar_producto import actualizar_producto
from acciones.abrir_bloque import abrir_bloque
from acciones.cerrar_bloque import cerrar_bloque
from acciones.consultar_productos import consultar_productos
from acciones.detalle_bloque import detalle_bloque
from acciones.registrar_producto import registrar_producto
from core.utilidades import pausa, titulo


def menu_productos(d):
    while True:
        titulo("PRODUCTOS")
        print("1) Registrar  2) Consultar/buscar  3) Actualizar  0) Volver")
        op = input("Opcion: ").strip()
        if op == "1":
            registrar_producto(d)
        elif op == "2":
            consultar_productos(d)
            pausa()
        elif op == "3":
            actualizar_producto(d)
        elif op == "0":
            return


def menu_caja(d):
    while True:
        titulo("CAJA Y BLOQUES")
        print("1) Abrir bloque  2) Cerrar bloque  3) Detalle de bloque  0) Volver")
        op = input("Opcion: ").strip()
        if op == "1":
            abrir_bloque(d)
            pausa()
        elif op == "2":
            cerrar_bloque(d)
            pausa()
        elif op == "3":
            detalle_bloque(d)
            pausa()
        elif op == "0":
            return
