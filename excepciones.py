#Clase base para las excepciones personalizadas
class ErrorCliente(Exception):
    "Excepción base para los errores relacionados con clientes."
    pass

#Excepción para cuando la cédula no es válida
class ErrorIdentificacion(ErrorCliente):
    pass

#Excepción para cuando el nombre no es válido
class ErrorNmbre(ErrorCliente):
    pass

#Excepción para cuando el teléfono no es válido
class ErrorTelefono(ErrorCliente):
    pass

#Excepción para cuando el correo electrónico no es válido
class ErrorCorrero(ErrorCliente):
    pass

    