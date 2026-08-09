from datetime import datetime
from uuid import uuid4

from modules.catalogos.validators import normalizar_texto
from modules.tickets.repository import TicketRepository
from modules.tickets.validators import validar_ticket


ESTADOS_PERMITIDOS = {"Nuevo", "Asignado", "En proceso", "Resuelto", "Cerrado"}


class TicketService:
    def __init__(self, repository=None):
        self.repository = repository or TicketRepository()

    def crear(self, solicitante_id, categoria_id, prioridad_id, descripcion):
        (
            solicitante_limpio,
            categoria_limpia,
            prioridad_limpia,
            descripcion_limpia,
        ) = validar_ticket(solicitante_id, categoria_id, prioridad_id, descripcion)

        self._validar_referencias(solicitante_limpio, categoria_limpia, prioridad_limpia)

        folio = self._generar_folio()
        nuevo_id = self.repository.crear(
            folio,
            solicitante_limpio,
            categoria_limpia,
            prioridad_limpia,
            descripcion_limpia,
            "Nuevo",
        )

        return self.obtener_por_folio(folio) or {"id": nuevo_id, "folio": folio}

    def listar(self):
        return self.repository.listar()

    def obtener_por_folio(self, folio):
        return self.repository.obtener_por_folio(folio)

    def actualizar(self, folio, categoria_id, prioridad_id, descripcion, estado):
        ticket = self.obtener_por_folio(folio)
        if not ticket:
            raise ValueError("El ticket indicado no existe.")

        (
            _,
            categoria_limpia,
            prioridad_limpia,
            descripcion_limpia,
        ) = validar_ticket(
            ticket["solicitante_id"],
            categoria_id,
            prioridad_id,
            descripcion,
        )
        estado_limpio = normalizar_texto(estado)
        if estado_limpio not in ESTADOS_PERMITIDOS:
            permitidos = ", ".join(sorted(ESTADOS_PERMITIDOS))
            raise ValueError(f"Estado no permitido. Use: {permitidos}.")

        self._validar_referencias(ticket["solicitante_id"], categoria_limpia, prioridad_limpia)
        actualizados = self.repository.actualizar(
            folio,
            categoria_limpia,
            prioridad_limpia,
            descripcion_limpia,
            estado_limpio,
        )
        if actualizados == 0:
            raise ValueError("No se actualizo el ticket.")
        return self.obtener_por_folio(folio)

    def eliminar(self, folio):
        if not self.obtener_por_folio(folio):
            raise ValueError("El ticket indicado no existe.")
        eliminados = self.repository.eliminar(folio)
        if eliminados == 0:
            raise ValueError("No se elimino el ticket.")
        return True

    def _validar_referencias(self, solicitante_id, categoria_id, prioridad_id):
        if not self.repository.existe_usuario_activo(solicitante_id):
            raise ValueError("El solicitante indicado no existe o no esta activo.")

        if not self.repository.existe_catalogo_activo(categoria_id, "categoria"):
            raise ValueError("La categoria indicada no existe o no esta activa.")

        if not self.repository.existe_catalogo_activo(prioridad_id, "prioridad"):
            raise ValueError("La prioridad indicada no existe o no esta activa.")

    def _generar_folio(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        sufijo = uuid4().hex[:6].upper()
        return f"TCK-{timestamp}-{sufijo}"
