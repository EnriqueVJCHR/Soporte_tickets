from config.database import initialize_database
from modules.catalogos.service import CatalogoService
from modules.tickets.service import TicketService
from modules.usuarios.service import UsuarioService


def mostrar_catalogos(service):
    print("\nCatalogos registrados:")
    for item in service.listar():
        print(
            f"- {item['id']}: {item['tipo']} | {item['nombre']} | "
            f"{item['descripcion']} | activo={item['activo']}"
        )


def obtener_o_crear_catalogo(service, tipo, nombre, descripcion):
    for item in service.listar(tipo):
        if item["nombre"].lower() == nombre.lower():
            return item["id"]
    return service.crear(tipo, nombre, descripcion)


def obtener_o_crear_usuario(service, nombre, correo, usuario, rol):
    existente = service.obtener_por_usuario(usuario)
    if existente:
        return existente["id"]
    return service.crear(nombre, correo, usuario, rol)


def main():
    initialize_database()
    catalogos = CatalogoService()
    usuarios = UsuarioService()
    tickets = TicketService()

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
    ids_catalogos = {}
    for tipo, nombre, descripcion in registros_iniciales:
        try:
            nuevo_id = obtener_o_crear_catalogo(catalogos, tipo, nombre, descripcion)
            ids_catalogos[(tipo, nombre)] = nuevo_id
            print(f"OK: {tipo} - {nombre}")
        except ValueError as error:
            print(f"AVISO: {error}")

    mostrar_catalogos(catalogos)

    print("\nFlujo principal Semana 12: registro y consulta de ticket")
    solicitante_id = obtener_o_crear_usuario(
        usuarios,
        "Ana Solicitante",
        "ana.solicitante@empresa.com",
        "asolicitante",
        "solicitante",
    )
    ticket = tickets.crear(
        solicitante_id,
        ids_catalogos[("categoria", "Hardware")],
        ids_catalogos[("prioridad", "Alta")],
        "La computadora del laboratorio no enciende correctamente.",
    )
    consulta = tickets.obtener_por_folio(ticket["folio"])

    print("Entrada: datos validos del solicitante y del ticket")
    print("Validacion: usuario, categoria y prioridad existentes")
    print("Procesamiento: folio generado y estado Nuevo")
    print("Persistencia: registro guardado en SQLite")
    print(
        f"Salida: {consulta['folio']} | {consulta['solicitante']} | "
        f"{consulta['categoria']} | {consulta['prioridad']} | {consulta['estado']}"
    )

    print("\nPrueba de duplicado de catalogo:")
    try:
        catalogos.crear("categoria", "Hardware", "Registro duplicado de prueba")
    except ValueError as error:
        print(f"Resultado esperado: {error}")


if __name__ == "__main__":
    main()
