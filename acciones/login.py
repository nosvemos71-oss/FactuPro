"""HU-014: acceso obligatorio al sistema (usuario: admin / clave: admin123)."""
import getpass
import secrets

from core.utilidades import titulo

USUARIO = "admin"
CLAVE = "admin123"
INTENTOS = 3


def _igual(a, b):
    return secrets.compare_digest(a.encode(), b.encode())


def iniciar_sesion():
    """Devuelve el nombre de usuario si el acceso es correcto, o None."""
    titulo("FACTUPRO - INICIAR SESION")
    for restantes in range(INTENTOS - 1, -1, -1):
        usuario = input("Usuario: ").strip().lower()
        clave = getpass.getpass("Contraseña: ")
        if _igual(usuario, USUARIO) and _igual(clave, CLAVE):
            print(f"\n  ✓ Bienvenido, {usuario}.")
            return usuario
        if restantes:
            print(f"  ! Usuario o contraseña incorrectos. Intentos restantes: {restantes}")
    print("  ! Demasiados intentos fallidos.")
    return None
