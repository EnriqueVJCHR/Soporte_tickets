import sqlite3

from config.database import get_connection


class TicketRepository:
    def crear(
        self,
        folio,
        solicitante_id,
        categoria_id,
        prioridad_id,
        descripcion,
        estado="Nuevo",
    ):
        try:
            with get_connection() as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                cursor = connection.execute(
                    """
                    INSERT INTO tickets (
                        folio,
                        solicitante_id,
                        categoria_id,
                        prioridad_id,
                        descripcion,
                        estado
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        folio,
                        solicitante_id,
                        categoria_id,
                        prioridad_id,
                        descripcion,
                        estado,
                    ),
                )
                connection.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "No se pudo crear el ticket. Verifique folio, usuario y catalogos."
            ) from exc

    def listar(self):
        with get_connection() as connection:
            rows = connection.execute(self._select_base() + " ORDER BY t.created_at DESC, t.id DESC").fetchall()
        return [dict(row) for row in rows]

    def obtener_por_folio(self, folio):
        with get_connection() as connection:
            row = connection.execute(
                self._select_base() + " WHERE t.folio = ?",
                (folio,),
            ).fetchone()
        return dict(row) if row else None

    def actualizar(self, folio, categoria_id, prioridad_id, descripcion, estado):
        with get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE tickets
                SET categoria_id = ?, prioridad_id = ?, descripcion = ?, estado = ?
                WHERE folio = ?
                """,
                (categoria_id, prioridad_id, descripcion, estado, folio),
            )
            connection.commit()
        return cursor.rowcount

    def eliminar(self, folio):
        with get_connection() as connection:
            cursor = connection.execute("DELETE FROM tickets WHERE folio = ?", (folio,))
            connection.commit()
        return cursor.rowcount

    def existe_usuario_activo(self, usuario_id):
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT id
                FROM usuarios
                WHERE id = ? AND activo = 1
                """,
                (usuario_id,),
            ).fetchone()
        return row is not None

    def existe_catalogo_activo(self, catalogo_id, tipo):
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT id
                FROM catalogos
                WHERE id = ? AND tipo = ? AND activo = 1
                """,
                (catalogo_id, tipo),
            ).fetchone()
        return row is not None

    def _select_base(self):
        return """
            SELECT
                t.id,
                t.folio,
                t.solicitante_id,
                u.nombre AS solicitante,
                t.categoria_id,
                c.nombre AS categoria,
                t.prioridad_id,
                p.nombre AS prioridad,
                t.descripcion,
                t.estado,
                t.created_at
            FROM tickets t
            JOIN usuarios u ON u.id = t.solicitante_id
            JOIN catalogos c ON c.id = t.categoria_id
            JOIN catalogos p ON p.id = t.prioridad_id
        """
