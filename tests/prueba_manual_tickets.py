from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from config.database import initialize_database
from modules.catalogos.service import CatalogoService
from modules.tickets.service import TicketService
from modules.usuarios.service import UsuarioService


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

    solicitante_id = obtener_o_crear_usuario(
        usuarios,
        "Ana Solicitante",
        "ana.solicitante@empresa.com",
        "asolicitante",
        "solicitante",
    )
    categoria_id = obtener_o_crear_catalogo(
        catalogos,
        "categoria",
        "Hardware",
        "Fallas fisicas en equipos",
    )
    prioridad_id = obtener_o_crear_catalogo(
        catalogos,
        "prioridad",
        "Alta",
        "Incidencia que requiere atencion inmediata",
    )

    print("Flujo principal Semana 12")
    print("Entrada: usuario, categoria, prioridad y descripcion del ticket")

    ticket = tickets.crear(
        solicitante_id,
        categoria_id,
        prioridad_id,
        "La computadora del laboratorio no enciende correctamente.",
    )

    consulta = tickets.obtener_por_folio(ticket["folio"])

    print("Validacion: datos y referencias aceptadas")
    print("Procesamiento: folio generado y estado inicial asignado")
    print("Persistencia: ticket guardado en SQLite")
    print("Salida:")
    print(f"- Folio: {consulta['folio']}")
    print(f"- Solicitante: {consulta['solicitante']}")
    print(f"- Categoria: {consulta['categoria']}")
    print(f"- Prioridad: {consulta['prioridad']}")
    print(f"- Estado: {consulta['estado']}")


if __name__ == "__main__":
    main()
