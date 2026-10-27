"""Funciones comunes: lectura validada de datos (HU-013) y formato."""


def pedir_texto(msg, vacio_ok=False):
    while True:
        v = input(msg).strip()
        if v or vacio_ok:
            return v
        print("  ! Este dato es obligatorio.")


def pedir_entero(msg, minimo=0, maximo=None, vacio_ok=False):
    while True:
        v = input(msg).strip().replace(".", "").replace(",", "")
        if v == "" and vacio_ok:
            return None
        try:
            n = int(v)
        except ValueError:
            print("  ! Escribe un numero entero valido.")
            continue
        if n < minimo:
            print(f"  ! Debe ser mayor o igual a {minimo}.")
        elif maximo is not None and n > maximo:
            print(f"  ! Debe ser menor o igual a {maximo}.")
        else:
            return n


def confirmar(msg):
    return input(f"{msg} (s/n): ").strip().lower() in ("s", "si", "sí")


def dinero(n):
    signo = "-" if n < 0 else ""
    return signo + "$" + f"{abs(n):,}".replace(",", ".")


def pausa():
    input("\nEnter para continuar...")


def titulo(t):
    print("\n" + "=" * 56 + f"\n  {t}\n" + "=" * 56)
