from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from config.database import initialize_database
from modules.usuarios.service import UsuarioService


def ejecutar_prueba_manual():
    initialize_database()
    service = UsuarioService()

    print("Prueba 1: registrar usuarios validos")
    usuarios = [
        ("Ana Lopez", "ana.lopez@empresa.com", "alopez", "solicitante"),
        ("Luis Perez", "luis.perez@empresa.com", "lperez", "tecnico"),
        ("Mario Admin", "mario.admin@empresa.com", "madmin", "administrador"),
    ]

    for nombre, correo, usuario, rol in usuarios:
        try:
            nuevo_id = service.crear(nombre, correo, usuario, rol)
            print(f"OK: usuario creado con id {nuevo_id} - {usuario} ({rol})")
        except ValueError as error:
            print(f"AVISO: {error}")

    print("\nPrueba 2: listar usuarios registrados")
    for item in service.listar():
        print(f"- {item['nombre']} | {item['usuario']} | {item['rol']}")

    print("\nPrueba 3: validar duplicado")
    try:
        service.crear("Ana Lopez", "ana.lopez@empresa.com", "alopez2", "solicitante")
    except ValueError as error:
        print(f"Resultado esperado: {error}")

    print("\nPrueba 4: validar rol no permitido")
    try:
        service.crear("Invitado Prueba", "invitado@empresa.com", "invitado", "invitado")
    except ValueError as error:
        print(f"Resultado esperado: {error}")


if __name__ == "__main__":
    ejecutar_prueba_manual()
