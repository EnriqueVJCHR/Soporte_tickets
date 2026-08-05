from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "mesa_ayuda.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS catalogos (
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
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
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
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folio TEXT NOT NULL UNIQUE,
                solicitante_id INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                prioridad_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Nuevo',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (solicitante_id) REFERENCES usuarios(id),
                FOREIGN KEY (categoria_id) REFERENCES catalogos(id),
                FOREIGN KEY (prioridad_id) REFERENCES catalogos(id)
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_tickets_solicitante
            ON tickets (solicitante_id)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_tickets_folio
            ON tickets (folio)
            """
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO roles (nombre, descripcion)
            VALUES (?, ?)
            """,
            [
                ("solicitante", "Usuario que registra y consulta sus tickets."),
                ("tecnico", "Usuario responsable de atender tickets asignados."),
                (
                    "administrador",
                    "Administrador/supervisor con permisos de gestion.",
                ),
            ],
        )
        connection.commit()
