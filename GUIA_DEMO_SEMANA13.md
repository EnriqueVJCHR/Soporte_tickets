# Guion de demostracion final candidata - Semana 13

## Objetivo de la demo
Mostrar que el sistema ejecuta el flujo principal minimo de una mesa de ayuda:
entrada, validacion, procesamiento, persistencia y salida verificable.

## Preparacion
1. Abrir la carpeta del proyecto en Visual Studio Code.
2. Abrir terminal integrada.
3. Verificar que se esta en la raiz `mesa_ayuda_tickets_semana7`.
4. Ejecutar pruebas finales.

## Comandos

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python tests/prueba_manual_tickets.py
python main.py
```

## Recorrido para explicar
1. `config/database.py` crea tablas de catalogos, usuarios, roles y tickets.
2. `modules/catalogos` administra categorias y prioridades.
3. `modules/usuarios` registra solicitantes, tecnicos y administradores.
4. `modules/tickets` registra el ticket, genera folio y asigna estado Nuevo.
5. La prueba manual consulta el ticket para comprobar persistencia.

## Evidencia alternativa si falla la demo
Usar estos archivos incluidos en el proyecto:

- `evidencia_pruebas_finales_semana13.txt`
- `evidencia_flujo_final_semana13.txt`
- `Entregable_Semana_13_Cierre_Tecnico.docx`

## Mensaje de cierre para exposicion
La version final candidata no pretende cubrir todo el sistema completo original. El alcance se congelo en el flujo principal minimo: catalogos, usuarios/roles y registro/consulta de tickets con persistencia SQLite y pruebas basicas.

## Demo visual Flask

1. Instalar dependencias si es primera ejecucion:

```bash
pip install -r requirements.txt
```

2. Ejecutar la app:

```bash
python app.py
```

3. Abrir navegador:

```text
http://127.0.0.1:5000
```

4. Recorrido sugerido:

- Entrar a Dashboard.
- Revisar Catalogos y Usuarios.
- Crear un ticket en la pantalla Tickets.
- Abrir el detalle del ticket.
- Cambiar estado a En proceso.
- Regresar a Dashboard y mostrar el conteo actualizado.

Frase para explicar al profe:

La version web no agrega todo el cierre de Semana 14; integra visualmente el flujo principal existente para que la version candidata ya pueda demostrarse como sistema.
