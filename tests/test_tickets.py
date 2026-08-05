import unittest

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from modules.tickets.service import TicketService
from modules.tickets.validators import validar_ticket


class TicketRepositoryMemoria:
    def __init__(self):
        self.tickets = []
        self.usuarios = {1}
        self.catalogos = {
            ("categoria", 1),
            ("prioridad", 2),
        }

    def crear(
        self,
        folio,
        solicitante_id,
        categoria_id,
        prioridad_id,
        descripcion,
        estado="Nuevo",
    ):
        if any(ticket["folio"] == folio for ticket in self.tickets):
            raise ValueError("Folio duplicado.")
        nuevo_id = len(self.tickets) + 1
        self.tickets.append(
            {
                "id": nuevo_id,
                "folio": folio,
                "solicitante_id": solicitante_id,
                "solicitante": "Ana Solicitante",
                "categoria_id": categoria_id,
                "categoria": "Hardware",
                "prioridad_id": prioridad_id,
                "prioridad": "Alta",
                "descripcion": descripcion,
                "estado": estado,
                "created_at": "2026-08-02 12:00:00",
            }
        )
        return nuevo_id

    def listar(self):
        return list(self.tickets)

    def obtener_por_folio(self, folio):
        for ticket in self.tickets:
            if ticket["folio"] == folio:
                return dict(ticket)
        return None

    def existe_usuario_activo(self, usuario_id):
        return usuario_id in self.usuarios

    def existe_catalogo_activo(self, catalogo_id, tipo):
        return (tipo, catalogo_id) in self.catalogos


class TicketServiceTest(unittest.TestCase):
    def setUp(self):
        self.repository = TicketRepositoryMemoria()
        self.service = TicketService(self.repository)

    def test_crear_ticket_genera_folio_y_estado_nuevo(self):
        ticket = self.service.crear(
            1,
            1,
            2,
            "La computadora del laboratorio no enciende.",
        )

        self.assertTrue(ticket["folio"].startswith("TCK-"))
        self.assertEqual(ticket["estado"], "Nuevo")
        self.assertEqual(ticket["descripcion"], "La computadora del laboratorio no enciende.")

    def test_consultar_ticket_por_folio(self):
        ticket = self.service.crear(
            1,
            1,
            2,
            "El sistema operativo no inicia correctamente.",
        )

        consulta = self.service.obtener_por_folio(ticket["folio"])

        self.assertIsNotNone(consulta)
        self.assertEqual(consulta["folio"], ticket["folio"])
        self.assertEqual(consulta["categoria"], "Hardware")

    def test_crear_dos_tickets_genera_folios_distintos(self):
        primero = self.service.crear(1, 1, 2, "El monitor no muestra imagen.")
        segundo = self.service.crear(1, 1, 2, "El teclado no responde al escribir.")

        self.assertNotEqual(primero["folio"], segundo["folio"])

    def test_rechaza_descripcion_vacia(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.crear(1, 1, 2, "")

        self.assertIn("obligatorios", str(contexto.exception))

    def test_rechaza_descripcion_demasiado_corta(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.crear(1, 1, 2, "Falla")

        self.assertIn("al menos", str(contexto.exception))

    def test_rechaza_solicitante_inexistente(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.crear(99, 1, 2, "La impresora no responde correctamente.")

        self.assertIn("solicitante", str(contexto.exception).lower())

    def test_rechaza_categoria_inexistente(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.crear(1, 99, 2, "La impresora no responde correctamente.")

        self.assertIn("categoria", str(contexto.exception).lower())

    def test_validador_rechaza_identificadores_invalidos(self):
        with self.assertRaises(ValueError) as contexto:
            validar_ticket("abc", 1, 2, "Descripcion valida de prueba.")

        self.assertIn("numeros enteros", str(contexto.exception))


if __name__ == "__main__":
    unittest.main()
