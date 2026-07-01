TIPOS_PERMITIDOS = {"categoria", "prioridad", "area", "estado", "equipo"}


def normalizar_texto(valor):
    return " ".join(valor.strip().split())


def validar_catalogo(tipo, nombre):
    if not tipo or not nombre:
        raise ValueError("El tipo y el nombre del catalogo son obligatorios.")

    tipo_limpio = normalizar_texto(tipo).lower()
    nombre_limpio = normalizar_texto(nombre)

    if tipo_limpio not in TIPOS_PERMITIDOS:
        permitidos = ", ".join(sorted(TIPOS_PERMITIDOS))
        raise ValueError(f"Tipo de catalogo no permitido. Use: {permitidos}.")

    if len(nombre_limpio) < 3:
        raise ValueError("El nombre del catalogo debe tener al menos 3 caracteres.")

    return tipo_limpio, nombre_limpio

