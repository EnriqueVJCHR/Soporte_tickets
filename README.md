# Mesa de Ayuda y Tickets de Mantenimiento - Semana 7

Proyecto académico para la práctica de codificación inicial por módulos con apoyo de Codex.

## Objetivo

Desarrollar la estructura inicial de una utilería para un sistema de mesa de ayuda y tickets de mantenimiento de equipos, implementando primero el módulo de Catálogos.

## Primer módulo implementado

El primer módulo implementado es `catalogos`, responsable de administrar datos base del sistema:

- Categorías
- Prioridades
- Áreas
- Estados
- Equipos

Estos datos serán utilizados posteriormente por el módulo de Tickets para clasificar y registrar incidencias.

## Persistencia

Se usa SQLite porque el sistema requiere conservar información después de cerrar el programa. La base de datos se crea en `data/mesa_ayuda.db`.

## Ejecutar prueba manual

Desde Visual Studio Code o una terminal:

```bash
python main.py
```

El programa:

1. Crea la base de datos si no existe.
2. Inserta catálogos iniciales.
3. Lista los catálogos registrados.
4. Intenta insertar un duplicado para demostrar la validación de RF-38.

## Estructura

```text
mesa_ayuda_tickets_semana7/
|-- main.py
|-- config/
|   |-- database.py
|-- data/
|-- modules/
|   |-- catalogos/
|   |   |-- repository.py
|   |   |-- service.py
|   |   |-- validators.py
|-- tests/
|   |-- prueba_manual_catalogos.py
|-- README.md
```



## Semana 8 - Pruebas unitarias

Se agregaron pruebas unitarias para el modulo `catalogos`, validando RF-37 y RF-38.

Para ejecutar las pruebas desde esta misma carpeta del proyecto:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Archivos agregados para Semana 8:

- `tests/test_catalogos.py`
- `tests/evidencia_depuracion_comentada.py`
- `evidencia_pruebas_semana8.txt`
- `evidencia_error_depuracion_semana8.txt`
- `PROMPTS_OTRAS_IAS.md`
- `evidencias/evidencia_pruebas_unitarias_windows.png`
- `evidencias/evidencia_error_duplicado_windows.png`

Como ahora Semana 8 esta dentro de esta misma carpeta, el commit se hace aqui:

```bash
git status
git add .
git commit -m "Agrega pruebas y evidencias semana 8"
```

## Segundo modulo implementado - Usuarios y roles

Para fortalecer el avance del segundo parcial se agrego el modulo `usuarios`.
Este modulo permite registrar y consultar usuarios con rol, preparando el camino
para autenticacion, permisos y asignacion de tickets.

Roles usados en codigo:

- `solicitante`
- `tecnico`
- `administrador`

En la documentacion, el rol `administrador` representa al administrador/supervisor.

Archivos agregados:

```text
modules/
|-- usuarios/
|   |-- repository.py
|   |-- service.py
|   |-- validators.py
tests/
|-- test_usuarios.py
|-- prueba_manual_usuarios.py
```

Requerimientos relacionados:

- RF-04: El sistema debe manejar roles de solicitante, tecnico y administrador/supervisor.
- RF-06: El administrador/supervisor debe poder registrar nuevos usuarios.
- RF-07: El sistema debe evitar registrar usuarios duplicados.
- RF-08: El administrador/supervisor debe poder consultar usuarios registrados.

Ejecutar prueba manual del modulo:

```bash
python tests/prueba_manual_usuarios.py
```

Ejecutar todas las pruebas:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Resultado esperado:

```text
Ran 13 tests

OK
```
