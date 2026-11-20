# Importamos la clase Cliente
from cliente import Cliente


# Creamos un cliente con datos válidos
cliente1 = Cliente(
    "María López",
    "12345678",
    "3001234567",
    "maria@gmail.com"
)

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