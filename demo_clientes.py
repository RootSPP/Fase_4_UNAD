# -*- coding: utf-8 -*-
# Importamos la clase Cliente
from cliente import Cliente

import sys


def main():
    """Ejecuta las 5 pruebas del módulo de clientes (1 válida y 4 inválidas).

    Este archivo lo ejecuta el integrador main.py del sistema, por eso
    las pruebas viven dentro de la función main().
    """
    # Configuramos la consola para que muestre bien las tildes
    sys.stdout.reconfigure(encoding="utf-8")

    # Creamos un cliente con datos válidos
    cliente1 = Cliente(
        "María López",
        "12345678",
        "3001234567",
        "maria@gmail.com"
    )
    cliente1.validar()

    # Mostramos la información del cliente
    print("CLIENTE REGISTRADO CORRECTAMENTE")
    print(cliente1.obtener_informacion())

    # Probamos el registro de un cliente con un nombre inválido
    try:
        cliente2 = Cliente(
            "María123",
            "12345678",
            "3001234567",
            "maria@gmail.com"
        )
    except Exception as error:
        print("ERROR AL REGISTRAR CLIENTE:", error)

    # Probamos una identificación inválida
    try:
        cliente3 = Cliente(
            "Carlos Pérez",
            "123",
            "3001234567",
            "carlos@gmail.com"
        )
    except Exception as error:
        print("ERROR DE IDENTIFICACIÓN:", error)

    # Probamos un teléfono inválido
    try:
        cliente4 = Cliente(
            "Carlos Pérez",
            "12345678",
            "123",
            "carlos@gmail.com"
        )
    except Exception as error:
        print("ERROR DE TELÉFONO:", error)

    # Probamos un correo electrónico inválido
    try:
        cliente5 = Cliente(
            "Carlos Pérez",
            "12345678",
            "3001234567",
            "carlosgmail.com"
        )
    except Exception as error:
        print("ERROR DE CORREO:", error)


if __name__ == "__main__":
    main()
