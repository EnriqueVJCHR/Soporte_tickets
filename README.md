# Mesa de Ayuda y Tickets de Mantenimiento de Equipos

Version final candidata - Semana 13

Proyecto academico para la materia Desarrollo de Utilerias y Manejadores.

## Equipo

- Christian Patricio Perez Landin
- Enrique Velez Jaime

## Objetivo del sistema

Desarrollar una utileria modular para una mesa de ayuda que permita administrar datos base, usuarios/roles y registrar tickets de mantenimiento de equipos con persistencia en SQLite.

## Alcance final congelado

Semana 13 congela el alcance. No se agregan funcionalidades grandes nuevas. La version candidata demuestra el flujo principal minimo:

```text
Entrada de datos
-> Validacion
-> Procesamiento
-> Persistencia SQLite
-> Salida verificable
```

## Modulos incluidos

```text
config/
|-- database.py
modules/
|-- catalogos/
|   |-- repository.py
|   |-- service.py
|   |-- validators.py
|-- usuarios/
|   |-- repository.py
|   |-- service.py
|   |-- validators.py
|-- tickets/
|   |-- repository.py
|   |-- service.py
|   |-- validators.py
tests/
|-- test_catalogos.py
|-- test_usuarios.py
|-- test_tickets.py
|-- test_flujo_principal_semana13.py
|-- prueba_manual_catalogos.py
|-- prueba_manual_usuarios.py
|-- prueba_manual_tickets.py
```

## Persistencia

Se usa SQLite. La base de datos se crea en:

```text
data/mesa_ayuda.db
```

Tablas principales:

- `catalogos`
- `roles`
- `usuarios`
- `tickets`

## Requisitos

- Windows 11 o sistema compatible.
- Python 3.10 o superior.
- No requiere instalar librerias externas para ejecutar pruebas basicas.

## Instalacion

1. Extraer el ZIP del proyecto.
2. Abrir la carpeta `mesa_ayuda_tickets_semana7` en Visual Studio Code.
3. Abrir una terminal en la raiz del proyecto.
4. Verificar Python:

```bash
python --version
```

## Ejecucion principal

```bash
python main.py
```

El programa prepara catalogos, crea/consulta un usuario solicitante, registra un ticket y muestra folio, solicitante, categoria, prioridad y estado.

## Prueba manual del flujo principal

```bash
python tests/prueba_manual_tickets.py
```

Salida esperada:

```text
Flujo principal Semana 12
Entrada: usuario, categoria, prioridad y descripcion del ticket
Validacion: datos y referencias aceptadas
Procesamiento: folio generado y estado inicial asignado
Persistencia: ticket guardado en SQLite
Salida:
- Folio: TCK-...
- Solicitante: Ana Solicitante
- Categoria: Hardware
- Prioridad: Alta
- Estado: Nuevo
```

## Pruebas finales Semana 13

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Resultado final esperado:

```text
Ran 23 tests

OK
```

## Requerimientos cubiertos

- RF-04: Manejar roles.
- RF-06: Registrar usuarios.
- RF-07: Evitar usuarios duplicados.
- RF-08: Consultar usuarios.
- RF-09 a RF-13: Registrar ticket, validar datos, generar folio, fecha y estado inicial.
- RF-16: Consultar detalle del ticket.
- RF-37: Administrar catalogos.
- RF-38: Evitar catalogos duplicados.

## Limitaciones conocidas

- La autenticacion completa queda parcial/no implementada.
- Los permisos por rol quedan documentados como pendiente.
- La asignacion de tecnico y transiciones de estado quedan como mejora futura.
- El seguimiento, solucion y cierre del ticket no forman parte de esta version candidata.
- La interfaz web basica queda pendiente; la demostracion se realiza por consola.
- No se incluyen adjuntos, dashboard, reportes, correo, chat ni app movil.

## Mejoras futuras

- Inicio/cierre de sesion.
- Permisos por rol.
- Asignacion de tickets a tecnico.
- Estados del ticket: Nuevo, Asignado, En proceso, Resuelto, Cerrado.
- Historial de cambios y comentarios.
- Interfaz web para la demostracion final.
- Reportes y metricas.

## Evidencias incluidas

- `evidencia_pruebas_finales_semana13.txt`
- `evidencia_flujo_final_semana13.txt`
- `evidencia_demo_main_semana13.txt`
- `evidencia_git_status_semana13.txt`
- `Entregable_Semana_13_Cierre_Tecnico.docx`
- `Presentacion_Preliminar_Semana_14_Mesa_Ayuda.pptx`

## Commit sugerido

```bash
git status
git add .
git commit -m "chore: cierre tecnico semana 13"
```

## Version visual candidata con Flask

Para que la entrega ya se pueda mostrar como sistema web, se agrego una interfaz visual minimalista en Flask. Esta version no intenta cerrar todas las funciones de Semana 14; funciona como demo avanzada para presentar el flujo principal.

### Instalar dependencia web

```bash
pip install -r requirements.txt
```

### Ejecutar la aplicacion web

```bash
python app.py
```

Despues abrir en el navegador:

```text
http://127.0.0.1:5000
```

### Pantallas disponibles

- Dashboard: resumen de tickets, usuarios y catalogos.
- Tickets: crear, listar, consultar, actualizar y eliminar tickets.
- Usuarios: crear y listar usuarios para alimentar tickets.
- Catalogos: crear y listar categorias/prioridades para alimentar tickets.

### Alcance de la vista web

La vista web cubre una demo CRUD minima y visual del sistema. Quedan fuera de esta version: login completo, permisos reales por rol, asignacion avanzada, reportes, adjuntos, chat y app movil.
