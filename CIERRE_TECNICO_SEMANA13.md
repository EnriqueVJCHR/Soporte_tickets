# Cierre tecnico Semana 13

## Regla aplicada
No se agregaron funcionalidades grandes nuevas. El trabajo se concentro en estabilizar, probar, documentar y preparar la entrega.

## Alcance final congelado

| Bloque | Estado | Decision |
|---|---|---|
| Catalogos | Implementado | Conservar en version candidata |
| Usuarios y roles | Implementado | Conservar en version candidata |
| Tickets basicos | Implementado | Conservar en version candidata |
| Persistencia SQLite | Implementado | Conservar en version candidata |
| Pruebas unitarias e integracion | Implementado | Conservar en version candidata |
| Autenticacion | Parcial/Pendiente | Cierre futuro |
| Permisos por rol | Parcial/Pendiente | Cierre futuro |
| Asignacion y estados | Pendiente | Mejora futura |
| Seguimiento y cierre | Pendiente | Mejora futura |
| Interfaz web | Pendiente | Mejora futura |
| Adjuntos/reportes/chat/correo/app movil | Fuera de alcance | Mejora futura |

## Errores corregidos

1. Folio duplicado al crear tickets demasiado rapido.
   - Correccion: se agrego sufijo unico con `uuid4`.
2. Prueba final con SQLite temporal bloqueado en Windows.
   - Correccion: se ajusto la prueba para no borrar el archivo mientras Windows puede tenerlo ocupado.
3. README con caracteres raros por codificacion.
   - Correccion: se reescribio el README en ASCII y con enfoque de version final candidata.

## Evidencia final

- Pruebas finales: `Ran 23 tests / OK`.
- Flujo principal manual: ticket creado, persistido y consultado.
- Demo principal: `python main.py`.

## Preparacion para Semana 14

- Usar `GUIA_DEMO_SEMANA13.md` como guion operativo.
- Abrir el proyecto en Visual Studio Code.
- Ejecutar primero pruebas, despues flujo manual.
- Tener evidencia alternativa en TXT si falla la demo en vivo.
