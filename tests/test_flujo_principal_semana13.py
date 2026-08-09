import tempfile
import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import config.database as database
from config.database import initialize_database
from modules.catalogos.service import CatalogoService
from modules.tickets.service import TicketService
from modules.usuarios.service import UsuarioService


class FlujoPrincipalSemana13Test(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="mesa_ayuda_semana13_"))
        self.original_data_dir = database.DATA_DIR
        self.original_database_path = database.DATABASE_PATH
        database.DATA_DIR = self.temp_dir
        database.DATABASE_PATH = database.DATA_DIR / "mesa_ayuda_test.db"
        initialize_database()
        self.catalogos = CatalogoService()
        self.usuarios = UsuarioService()
        self.tickets = TicketService()

    def tearDown(self):
        database.DATA_DIR = self.original_data_dir
        database.DATABASE_PATH = self.original_database_path
        # En Windows SQLite puede liberar el archivo unos ms despues; no se borra aqui.

    def test_flujo_principal_persiste_y_consulta_ticket(self):
        solicitante_id = self.usuarios.crear(
            "Ana Solicitante",
            "ana.final@empresa.com",
            "afinal",
            "solicitante",
        )
        categoria_id = self.catalogos.crear(
            "categoria",
            "Hardware",
            "Fallas fisicas en equipos",
        )
        prioridad_id = self.catalogos.crear(
            "prioridad",
            "Alta",
            "Atencion inmediata",
        )

        ticket = self.tickets.crear(
            solicitante_id,
            categoria_id,
            prioridad_id,
            "La computadora del laboratorio no enciende correctamente.",
        )
        consulta = TicketService().obtener_por_folio(ticket["folio"])

        self.assertIsNotNone(consulta)
        self.assertEqual(consulta["estado"], "Nuevo")
        self.assertEqual(consulta["solicitante"], "Ana Solicitante")
        self.assertEqual(consulta["categoria"], "Hardware")
        self.assertEqual(consulta["prioridad"], "Alta")

    def test_flujo_principal_rechaza_prioridad_inexistente(self):
        solicitante_id = self.usuarios.crear(
            "Ana Solicitante",
            "ana.error@empresa.com",
            "aerror",
            "solicitante",
        )
        categoria_id = self.catalogos.crear(
            "categoria",
            "Hardware",
            "Fallas fisicas en equipos",
        )

        with self.assertRaises(ValueError) as contexto:
            self.tickets.crear(
                solicitante_id,
                categoria_id,
                99,
                "La computadora del laboratorio no enciende correctamente.",
            )

        self.assertIn("prioridad", str(contexto.exception).lower())


if __name__ == "__main__":
    unittest.main()


