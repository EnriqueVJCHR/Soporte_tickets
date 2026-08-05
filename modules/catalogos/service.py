from modules.catalogos.repository import CatalogoRepository
from modules.catalogos.validators import normalizar_texto, validar_catalogo


class CatalogoService:
    def __init__(self, repository=None):
        self.repository = repository or CatalogoRepository()

    def crear(self, tipo, nombre, descripcion=""):
        tipo_limpio, nombre_limpio = validar_catalogo(tipo, nombre)
        descripcion_limpia = normalizar_texto(descripcion) if descripcion else ""
        return self.repository.crear(tipo_limpio, nombre_limpio, descripcion_limpia)

    def listar(self, tipo=None):
        tipo_limpio = normalizar_texto(tipo).lower() if tipo else None
        return self.repository.listar(tipo_limpio)

