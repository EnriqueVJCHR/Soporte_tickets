# Prompts y contexto para probar con otras IAs

## Contexto base para pegar antes de pedir pruebas

Estamos trabajando en un proyecto academico llamado Mesa de Ayuda y Tickets de Mantenimiento de Equipos. El sistema busca registrar, administrar y dar seguimiento a tickets de soporte tecnico y mantenimiento dentro de una organizacion.

En Semana 7 se implemento el primer modulo: Cat?logos. Este modulo administra datos base que despues usara el modulo de Tickets: categorias, prioridades, areas, estados y equipos.

La persistencia elegida es SQLite. El modulo tiene esta separacion:

- config/database.py: crea la conexion SQLite e inicializa la tabla catalogos.
- modules/catalogos/validators.py: valida tipo permitido, campos obligatorios y longitud minima.
- modules/catalogos/repository.py: ejecuta operaciones SQL para crear y listar catalogos.
- modules/catalogos/service.py: coordina validacion y persistencia.

Requerimientos relacionados:

- RF-37: El administrador/supervisor debe poder administrar catalogos basicos.
- RF-38: El sistema debe validar que no se registren elementos duplicados.

Historias relacionadas:

- HU-37: Como administrador/supervisor, quiero registrar y consultar catalogos para clasificar correctamente los tickets.
- HU-38: Como administrador/supervisor, quiero evitar catalogos duplicados para mantener informacion consistente.

Criterios de aceptacion:

- Dado un tipo y nombre validos, cuando se registra el catalogo, entonces el sistema lo guarda y lo muestra en la lista.
- Dado un catalogo existente con el mismo tipo y nombre, cuando se intenta registrar otra vez, entonces el sistema rechaza la operacion y muestra un error.

Tipos permitidos: categoria, prioridad, area, estado, equipo.

## Prompt 1 - Revision del modulo antes de probar

Actua como revisor tecnico y especialista en pruebas. Con el contexto anterior, analiza el modulo Cat?logos antes de generar pruebas. Responde:

1. Que responsabilidades debe cumplir el modulo.
2. Que entradas y salidas debe manejar.
3. Que reglas de validacion deben probarse.
4. Que partes pertenecen a logica de negocio y que partes a persistencia.
5. Que dudas o inconsistencias detectas.

No generes codigo todavia.

## Prompt 2 - Estrategia de pruebas

Actua como especialista en pruebas de software. Prop?n una estrategia de pruebas para el modulo Cat?logos.

Incluye:

1. Pruebas unitarias necesarias.
2. Casos normales.
3. Casos limite.
4. Casos de error.
5. Datos de prueba.
6. Resultado esperado para cada prueba.
7. Archivos que se deberian crear o modificar.
8. Como aislar la base de datos real usando una base de datos temporal.

No modifiques archivos todavia.

## Prompt 3 - Generacion de pruebas unitarias

Ahora implementa pruebas unitarias para el modulo Cat?logos usando Python y unittest.

Reglas:

- No modifiques la logica principal sin autorizacion.
- Crea las pruebas en tests/test_catalogos.py.
- Incluye al menos un caso normal, un caso limite y un caso de error.
- Usa una base de datos temporal o en memoria para no modificar data/mesa_ayuda.db.
- Prueba crear, listar, duplicados, tipo no permitido, nombre demasiado corto y campos vacios.
- Explica que valida cada prueba.

## Prompt 4 - Depuracion a partir de error

Ejecute las pruebas y obtuve este error:

[PEGAR ERROR COMPLETO]

Ayudame a analizarlo. Primero explica:

1. Que significa el error.
2. Cual es la causa probable.
3. Que archivos estan involucrados.
4. Que opciones de correccion existen.
5. Cual correccion recomiendas y por que.

No modifiques codigo todavia.

## Prompt 5 - Mejorar cobertura

Con base en las pruebas existentes del modulo Cat?logos, sugiere pruebas adicionales para mejorar cobertura sin avanzar a otros modulos.

Incluye pruebas para:

- Normalizacion de espacios.
- Mayusculas y minusculas en tipo.
- Ordenamiento de resultados.
- Descripciones vacias.
- Integridad de la restriccion UNIQUE(tipo, nombre).
- Separacion entre servicio y repositorio.

## Prompt 6 - Actualizar README

Ayudame a actualizar el README del proyecto para documentar como ejecutar las pruebas unitarias.

Incluye:

1. Requisitos.
2. Comando para ejecutar el programa principal.
3. Comando para ejecutar pruebas.
4. Explicacion de que las pruebas usan base temporal.
5. Resultado esperado.
6. Relacion con RF-37 y RF-38.

## Prompt 7 - Redactar bitacora de Codex

Con base en el trabajo de pruebas del modulo Cat?logos, redacta una bitacora breve con columnas:

- Fase.
- Prompt usado.
- Resultado de la IA.
- Que aceptamos.
- Que modificamos.
- Responsable.

Fases: contexto, estrategia de pruebas, generacion de pruebas, depuracion, documentacion.
