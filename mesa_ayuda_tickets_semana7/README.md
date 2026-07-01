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

