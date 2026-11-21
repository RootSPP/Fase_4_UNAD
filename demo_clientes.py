# -*- coding: utf-8 -*-
# Importamos la clase Cliente
from cliente import Cliente

# Importamos las excepciones propias del modulo de clientes
from excepciones import ErrorCliente

import sys


def main():
    """Ejecuta las 5 pruebas del módulo de clientes (1 válida y 4 inválidas).

    Mejora: se captura la excepcion especifica ErrorCliente (en lugar de
    Exception) y se indica tras cada error que el sistema continua
    funcionando, igual que en las otras demos.
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
    except ErrorCliente as error:
        print("ERROR AL REGISTRAR CLIENTE:", error)
        print("El sistema continua funcionando despues del error.")

    # Probamos una identificación inválida
    try:
        cliente3 = Cliente(
            "Carlos Pérez",
            "123",
            "3001234567",
            "carlos@gmail.com"
        )
    except ErrorCliente as error:
        print("ERROR DE IDENTIFICACIÓN:", error)
        print("El sistema continua funcionando despues del error.")

    # Probamos un teléfono inválido
    try:
        cliente4 = Cliente(
            "Carlos Pérez",
            "12345678",
            "123",
            "carlos@gmail.com"
        )
    except ErrorCliente as error:
        print("ERROR DE TELÉFONO:", error)
        print("El sistema continua funcionando despues del error.")

    # Probamos un correo electrónico inválido
    try:
        cliente5 = Cliente(
            "Carlos Pérez",
            "12345678",
            "3001234567",
            "carlosgmail.com"
        )
    except ErrorCliente as error:
        print("ERROR DE CORREO:", error)
        print("El sistema continua funcionando despues del error.")


if __name__ == "__main__":
    main()
