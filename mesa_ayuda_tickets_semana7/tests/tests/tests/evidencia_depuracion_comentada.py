"""Demostracion documental de depuracion.

Este archivo NO es parte de las pruebas finales. Sirve para explicar el error
controlado revisado durante Semana 8.

Caso incorrecto inicial:
    service.crear("estado", "Nuevo", "Ticket recien creado")
    service.crear("estado", "Nuevo", "Duplicado")

Ese segundo registro lanza ValueError porque RF-38 exige no permitir duplicados.

Forma correcta de probarlo:
    with self.assertRaises(ValueError):
        service.crear("estado", "Nuevo", "Duplicado")
"""
