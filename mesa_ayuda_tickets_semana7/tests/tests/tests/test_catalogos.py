import sqlite3
import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from modules.catalogos.repository import CatalogoRepository
from modules.catalogos.service import CatalogoService
from modules.catalogos.validators import validar_catalogo


class CatalogoRepositoryMemoria(CatalogoRepository):
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            """
            CREATE TABLE catalogos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                activo INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(tipo, nombre)
            )
            """
        )
        self.connection.commit()

    def crear(self, tipo, nombre, descripcion=""):
        try:
            cursor = self.connection.execute(
                """
                INSERT INTO catalogos (tipo, nombre, descripcion)
                VALUES (?, ?, ?)
                """,
                (tipo, nombre, descripcion),
            )
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"Ya existe un catalogo de tipo '{tipo}' con el nombre '{nombre}'."
            ) from exc

    def listar(self, tipo=None):
        if tipo:
            rows = self.connection.execute(
                """
                SELECT id, tipo, nombre, descripcion, activo, created_at
                FROM catalogos
                WHERE tipo = ?
                ORDER BY tipo, nombre
                """,
                (tipo,),
            ).fetchall()
        else:
            rows = self.connection.execute(
                """
                SELECT id, tipo, nombre, descripcion, activo, created_at
                FROM catalogos
                ORDER BY tipo, nombre
                """
            ).fetchall()
        return [dict(row) for row in rows]


class CatalogoServiceTest(unittest.TestCase):
    def setUp(self):
        self.repository = CatalogoRepositoryMemoria()
        self.service = CatalogoService(self.repository)

    def test_crear_y_listar_catalogo_valido(self):
        nuevo_id = self.service.crear("categoria", "Hardware", "Fallas fisicas")
        catalogos = self.service.listar("categoria")

        self.assertEqual(nuevo_id, 1)
        self.assertEqual(len(catalogos), 1)
        self.assertEqual(catalogos[0]["tipo"], "categoria")
        self.assertEqual(catalogos[0]["nombre"], "Hardware")

    def test_normaliza_espacios_en_nombre(self):
        self.service.crear(" prioridad ", "  Alta   Urgente  ", " Atencion inmediata ")
        catalogos = self.service.listar("prioridad")

        self.assertEqual(catalogos[0]["nombre"], "Alta Urgente")
        self.assertEqual(catalogos[0]["descripcion"], "Atencion inmediata")

    def test_rechaza_tipo_no_permitido(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.crear("color", "Rojo", "Tipo fuera del alcance")

        self.assertIn("Tipo de catalogo no permitido", str(contexto.exception))

    def test_rechaza_nombre_demasiado_corto(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.crear("area", "TI", "Nombre corto")

        self.assertIn("al menos 3 caracteres", str(contexto.exception))

    def test_rechaza_catalogo_duplicado(self):
        self.service.crear("estado", "Nuevo", "Ticket recien creado")

        with self.assertRaises(ValueError) as contexto:
            self.service.crear("estado", "Nuevo", "Duplicado")

        self.assertIn("Ya existe un catalogo", str(contexto.exception))

    def test_validador_rechaza_campos_obligatorios_vacios(self):
        with self.assertRaises(ValueError) as contexto:
            validar_catalogo("", "Hardware")

        self.assertIn("obligatorios", str(contexto.exception))


if __name__ == "__main__":
    unittest.main()
