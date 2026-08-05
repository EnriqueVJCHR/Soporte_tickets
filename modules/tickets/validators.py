from modules.catalogos.validators import normalizar_texto


DESCRIPCION_MINIMA = 10


def validar_ticket(solicitante_id, categoria_id, prioridad_id, descripcion):
    if not solicitante_id or not categoria_id or not prioridad_id or not descripcion:
        raise ValueError(
            "Solicitante, categoria, prioridad y descripcion son obligatorios."
        )

    try:
        solicitante_limpio = int(solicitante_id)
        categoria_limpia = int(categoria_id)
        prioridad_limpia = int(prioridad_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("Los identificadores deben ser numeros enteros.") from exc

    if solicitante_limpio <= 0 or categoria_limpia <= 0 or prioridad_limpia <= 0:
        raise ValueError("Los identificadores deben ser mayores a cero.")

    descripcion_limpia = normalizar_texto(descripcion)
    if len(descripcion_limpia) < DESCRIPCION_MINIMA:
        raise ValueError(
            f"La descripcion debe tener al menos {DESCRIPCION_MINIMA} caracteres."
        )

    return (
        solicitante_limpio,
        categoria_limpia,
        prioridad_limpia,
        descripcion_limpia,
    )
