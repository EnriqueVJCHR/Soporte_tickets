import sqlite3

from config.database import get_connection


class UsuarioRepository:
    def crear(self, nombre, correo, usuario, rol):
        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO usuarios (nombre, correo, usuario, rol)
                    VALUES (?, ?, ?, ?)
                    """,
                    (nombre, correo, usuario, rol),
                )
                connection.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "Ya existe un usuario con el mismo correo o nombre de usuario."
            ) from exc

    def listar(self, rol=None):
        with get_connection() as connection:
            if rol:
                rows = connection.execute(
                    """
                    SELECT id, nombre, correo, usuario, rol, activo, created_at
                    FROM usuarios
                    WHERE rol = ?
                    ORDER BY nombre
                    """,
                    (rol,),
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT id, nombre, correo, usuario, rol, activo, created_at
                    FROM usuarios
                    ORDER BY nombre
                    """
                ).fetchall()

        return [dict(row) for row in rows]

    def obtener_por_usuario(self, usuario):
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, nombre, correo, usuario, rol, activo, created_at
                FROM usuarios
                WHERE usuario = ?
                """,
                (usuario,),
            ).fetchone()

        return dict(row) if row else None
