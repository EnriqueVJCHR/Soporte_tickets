from config.database import initialize_database
from modules.catalogos.service import CatalogoService


def mostrar_catalogos(service):
    print("\nCatalogos registrados:")
    for item in service.listar():
        print(
            f"- {item['id']}: {item['tipo']} | {item['nombre']} | "
            f"{item['descripcion']} | activo={item['activo']}"
        )


def main():
    initialize_database()
    service = CatalogoService()

    registros_iniciales = [
        ("categoria", "Hardware", "Fallas fisicas en equipos"),
        ("categoria", "Software", "Problemas con programas o sistema operativo"),
        ("prioridad", "Alta", "Incidencia que requiere atencion inmediata"),
        ("prioridad", "Media", "Incidencia importante sin bloqueo total"),
        ("estado", "Nuevo", "Ticket registrado sin asignacion"),
        ("area", "Laboratorio", "Equipos ubicados en laboratorio"),
        ("equipo", "Computadora", "Equipo de computo de escritorio o portatil"),
    ]

    print("Insertando catalogos iniciales...")
    for tipo, nombre, descripcion in registros_iniciales:
        try:
            service.crear(tipo, nombre, descripcion)
            print(f"OK: {tipo} - {nombre}")
        except ValueError as error:
            print(f"AVISO: {error}")

    mostrar_catalogos(service)

    print("\nPrueba de duplicado:")
    try:
        service.crear("categoria", "Hardware", "Registro duplicado de prueba")
    except ValueError as error:
        print(f"Resultado esperado: {error}")


if __name__ == "__main__":
    main()

