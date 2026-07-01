import sqlite3

from config.database import get_connection


class CatalogoRepository:
    def crear(self, tipo, nombre, descripcion=""):
        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO catalogos (tipo, nombre, descripcion)
                    VALUES (?, ?, ?)
                    """,
                    (tipo, nombre, descripcion),
                )
                connection.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"Ya existe un catalogo de tipo '{tipo}' con el nombre '{nombre}'."
            ) from exc

    def listar(self, tipo=None):
        with get_connection() as connection:
            if tipo:
                rows = connection.execute(
                    """
                    SELECT id, tipo, nombre, descripcion, activo, created_at
                    FROM catalogos
                    WHERE tipo = ?
                    ORDER BY tipo, nombre
                    """,
                    (tipo,),
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT id, tipo, nombre, descripcion, activo, created_at
                    FROM catalogos
                    ORDER BY tipo, nombre
                    """
                ).fetchall()

        return [dict(row) for row in rows]

