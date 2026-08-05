import re


ROLES_PERMITIDOS = {"solicitante", "tecnico", "administrador"}
CORREO_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalizar_texto(valor):
    return " ".join(valor.strip().split())


def validar_usuario(nombre, correo, usuario, rol):
    if not nombre or not correo or not usuario or not rol:
        raise ValueError("Nombre, correo, usuario y rol son obligatorios.")

    nombre_limpio = normalizar_texto(nombre)
    correo_limpio = normalizar_texto(correo).lower()
    usuario_limpio = normalizar_texto(usuario).lower()
    rol_limpio = normalizar_texto(rol).lower()

    if len(nombre_limpio) < 3:
        raise ValueError("El nombre debe tener al menos 3 caracteres.")

    if len(usuario_limpio) < 4:
        raise ValueError("El usuario debe tener al menos 4 caracteres.")

    if not CORREO_REGEX.match(correo_limpio):
        raise ValueError("El correo no tiene un formato valido.")

    if rol_limpio not in ROLES_PERMITIDOS:
        permitidos = ", ".join(sorted(ROLES_PERMITIDOS))
        raise ValueError(f"Rol no permitido. Use: {permitidos}.")

    return nombre_limpio, correo_limpio, usuario_limpio, rol_limpio
