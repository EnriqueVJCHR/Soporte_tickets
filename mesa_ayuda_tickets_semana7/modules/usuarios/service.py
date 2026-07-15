from modules.usuarios.repository import UsuarioRepository
from modules.usuarios.validators import normalizar_texto, validar_usuario


class UsuarioService:
    def __init__(self, repository=None):
        self.repository = repository or UsuarioRepository()

    def crear(self, nombre, correo, usuario, rol):
        nombre_limpio, correo_limpio, usuario_limpio, rol_limpio = validar_usuario(
            nombre, correo, usuario, rol
        )
        return self.repository.crear(
            nombre_limpio, correo_limpio, usuario_limpio, rol_limpio
        )

    def listar(self, rol=None):
        rol_limpio = normalizar_texto(rol).lower() if rol else None
        return self.repository.listar(rol_limpio)

    def obtener_por_usuario(self, usuario):
        usuario_limpio = normalizar_texto(usuario).lower()
        return self.repository.obtener_por_usuario(usuario_limpio)
