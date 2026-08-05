import sqlite3
import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from modules.usuarios.repository import UsuarioRepository
from modules.usuarios.service import UsuarioService
from modules.usuarios.validators import validar_usuario


class UsuarioRepositoryMemoria(UsuarioRepository):
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            """
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                usuario TEXT NOT NULL UNIQUE,
                rol TEXT NOT NULL,
                activo INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.commit()

    def crear(self, nombre, correo, usuario, rol):
        try:
            cursor = self.connection.execute(
                """
                INSERT INTO usuarios (nombre, correo, usuario, rol)
                VALUES (?, ?, ?, ?)
                """,
                (nombre, correo, usuario, rol),
            )
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "Ya existe un usuario con el mismo correo o nombre de usuario."
            ) from exc

    def listar(self, rol=None):
        if rol:
            rows = self.connection.execute(
                """
                SELECT id, nombre, correo, usuario, rol, activo, created_at
                FROM usuarios
                WHERE rol = ?
                ORDER BY nombre
                """,
                (rol,),
            ).fetchall()
        else:
            rows = self.connection.execute(
                """
                SELECT id, nombre, correo, usuario, rol, activo, created_at
                FROM usuarios
                ORDER BY nombre
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def obtener_por_usuario(self, usuario):
        row = self.connection.execute(
            """
            SELECT id, nombre, correo, usuario, rol, activo, created_at
            FROM usuarios
            WHERE usuario = ?
            """,
            (usuario,),
        ).fetchone()
        return dict(row) if row else None


class UsuarioServiceTest(unittest.TestCase):
    def setUp(self):
        self.repository = UsuarioRepositoryMemoria()
        self.service = UsuarioService(self.repository)

    def test_crear_y_listar_usuario_valido(self):
        nuevo_id = self.service.crear(
            "Ana Lopez", "ANA.LOPEZ@EMPRESA.COM", "ALopez", "Solicitante"
        )
        usuarios = self.service.listar()

        self.assertEqual(nuevo_id, 1)
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0]["correo"], "ana.lopez@empresa.com")
        self.assertEqual(usuarios[0]["usuario"], "alopez")
        self.assertEqual(usuarios[0]["rol"], "solicitante")

    def test_filtra_usuarios_por_rol(self):
        self.service.crear("Ana Lopez", "ana@empresa.com", "alopez", "solicitante")
        self.service.crear("Luis Perez", "luis@empresa.com", "lperez", "tecnico")

        tecnicos = self.service.listar("tecnico")

        self.assertEqual(len(tecnicos), 1)
        self.assertEqual(tecnicos[0]["usuario"], "lperez")

    def test_obtener_por_usuario(self):
        self.service.crear("Mario Admin", "mario@empresa.com", "madmin", "administrador")

        usuario = self.service.obtener_por_usuario("MAdmin")

        self.assertIsNotNone(usuario)
        self.assertEqual(usuario["rol"], "administrador")

    def test_rechaza_correo_invalido(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.crear("Ana Lopez", "correo-invalido", "alopez", "solicitante")

        self.assertIn("correo", str(contexto.exception))

    def test_rechaza_rol_no_permitido(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.crear("Invitado", "invitado@empresa.com", "invitado", "invitado")

        self.assertIn("Rol no permitido", str(contexto.exception))

    def test_rechaza_usuario_duplicado(self):
        self.service.crear("Ana Lopez", "ana@empresa.com", "alopez", "solicitante")

        with self.assertRaises(ValueError) as contexto:
            self.service.crear("Ana Otra", "ana2@empresa.com", "alopez", "solicitante")

        self.assertIn("Ya existe un usuario", str(contexto.exception))

    def test_validador_rechaza_campos_obligatorios_vacios(self):
        with self.assertRaises(ValueError) as contexto:
            validar_usuario("", "ana@empresa.com", "alopez", "solicitante")

        self.assertIn("obligatorios", str(contexto.exception))


if __name__ == "__main__":
    unittest.main()
