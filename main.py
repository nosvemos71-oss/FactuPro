#!/usr/bin/env python3
"""FactuPro - sistema de ventas y caja por bloques de una hora.

Uso:  py main.py        (usuario: admin  |  contraseña: admin123)
"""
import sys

from acciones.login import iniciar_sesion
from acciones.nueva_venta import nueva_venta
from acciones.resumen_diario import resumen_diario
from core.almacenamiento import cargar
from core.bloques import bloque_abierto, etiqueta_bloque
from core.utilidades import pausa, titulo
from menus import menu_caja, menu_productos


def main():
    usuario = iniciar_sesion()
    if usuario is None:
        sys.exit(1)
    d = cargar()
    while True:
        titulo("FACTUPRO - MENU PRINCIPAL")
        clave, b = bloque_abierto(d)
        estado = etiqueta_bloque(clave, b) if clave else "ninguno (abrelo en Caja y bloques)"
        print(f"Bloque abierto: {estado}  | usuario: {usuario}")
        print("1) Productos\n2) Nueva venta\n3) Caja y bloques\n4) Resumen diario\n0) Salir")
        op = input("Opcion: ").strip()
        if op == "1":
            menu_productos(d)
        elif op == "2":
            nueva_venta(d, usuario)
            pausa()
        elif op == "3":
            menu_caja(d)
        elif op == "4":
            resumen_diario(d)
            pausa()
        elif op == "0":
            print("Hasta luego.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSaliendo. Los datos ya estan guardados.")
