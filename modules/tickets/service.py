from datetime import datetime
from uuid import uuid4

from modules.tickets.repository import TicketRepository
from modules.tickets.validators import validar_ticket


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

        if not self.repository.existe_usuario_activo(solicitante_limpio):
            raise ValueError("El solicitante indicado no existe o no esta activo.")

        if not self.repository.existe_catalogo_activo(categoria_limpia, "categoria"):
            raise ValueError("La categoria indicada no existe o no esta activa.")

        if not self.repository.existe_catalogo_activo(prioridad_limpia, "prioridad"):
            raise ValueError("La prioridad indicada no existe o no esta activa.")

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

    def _generar_folio(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        sufijo = uuid4().hex[:6].upper()
        return f"TCK-{timestamp}-{sufijo}"
