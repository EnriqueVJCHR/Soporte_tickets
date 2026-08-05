from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from config.database import initialize_database
from modules.catalogos.service import CatalogoService


def ejecutar_prueba_manual():
    initialize_database()
    service = CatalogoService()

    print("Prueba 1: registrar catalogo valido")
    nuevo_id = service.crear("prioridad", "Baja", "Atencion normal")
    print(f"Resultado obtenido: registro creado con id {nuevo_id}")

    print("\nPrueba 2: listar catalogos")
    for item in service.listar("prioridad"):
        print(f"- {item['nombre']}")

    print("\nPrueba 3: validar duplicado")
    try:
        service.crear("prioridad", "Baja", "Duplicado")
    except ValueError as error:
        print(f"Resultado obtenido: {error}")


if __name__ == "__main__":
    ejecutar_prueba_manual()
