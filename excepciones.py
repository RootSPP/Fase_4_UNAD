#Importamos herramientas para la fecha y hora del log
from datetime import datetime

#Archivo donde se registran los eventos y errores del sistema
ARCHIVO_LOG = "registro_eventos.log"


#Clase base para las excepciones personalizadas
class ErrorCliente(Exception):
    "Excepción base para los errores relacionados con clientes."
    pass

#Excepción para cuando la cédula no es válida
class ErrorIdentificacion(ErrorCliente):
    pass

#Excepción para cuando el nombre no es válido
class ErrorNombre(ErrorCliente):
    pass

#Excepción para cuando el teléfono no es válido
class ErrorTelefono(ErrorCliente):
    pass

#Excepción para cuando el correo electrónico no es válido
class ErrorCorreo(ErrorCliente):
    pass


#Función para registrar eventos y errores en el archivo de logs
def registrar_evento(mensaje):
    """Escribe un evento o error en el archivo de logs del sistema.

    Cada linea queda con fecha y hora para poder rastrear la secuencia
    de eventos. El archivo se abre en modo 'append' para no borrar el
    historial de ejecuciones anteriores.
    """
    marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(f"{marca} [EVENTO] {mensaje}\n")
