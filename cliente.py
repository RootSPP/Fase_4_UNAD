#Importamos la clase abstracta Entidad
from entidad import Entidad

#Importamos las excepciones personalizadas
from excepciones import (
    ErrorCliente,
    ErrorIdentificacion,
    ErrorNombre,
    ErrorTelefono,
    ErrorCorreo,
    registrar_evento
)

#Importamos herramientas para validar los datos
import re

#Clase que representa  a los clientes del sistema
class Cliente(Entidad):
    
    
    
       #Constructor de la clase
       def __init__(self, nombre, identificacion, telefono, correo):
           
           #Validamos los datos antes de almacenarlos
           self.validar_nombre(nombre)
           self.validar_identificacion(identificacion)
           self.validar_telefono(telefono)
           self.validar_correo(correo)
           
           #Encapsulamos los datos personales
           self.__nombre = nombre
           self.__identificacion = identificacion
           self.__telefono = telefono
           self.__correo = correo
           
       #Validamos que el nombre contenga únicamente letras y espacios
       @staticmethod
       def validar_nombre(nombre):
          if not isinstance(nombre, str) or not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+",nombre.strip()):
            raise ErrorNombre("El nombre solo debe contener letras y espacios.")
    
       #Validamos que la identificación contega entre 6 y 12 dígitos
       @staticmethod
       def validar_identificacion(identificacion):
         if not str(identificacion). isdigit() or not (6 <= len(str(identificacion))<= 12):
           raise ErrorIdentificacion("La cédula debe contener entre 6 y 12 dígitos.")
    
       #Validamos que el teléfono contenga entre 7 y 10 dígitos 
       @staticmethod
       def validar_telefono(telefono):
         if not str(telefono).isdigit() or not (7 <= len(str(telefono)) <= 10):
            raise ErrorTelefono("El teléfono debe contener entre 7 y 10 dígitos.")
    
       #Validamos que el correo tenga un estructura válida
       @staticmethod
       def validar_correo(correo):
         patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
         if not isinstance(correo, str) or not re.fullmatch(patron, correo):
            raise ErrorCorreo("El correo electrónico no tiene un formato válido.")         
        
        #Métodos para consultar los datos del cliente
       def obtener_nombre(self):
          return self.__nombre

       def obtener_identificacion(self):
          return self.__identificacion

       def obtener_telefono(self):
          return self.__telefono

       def obtener_correo(self):
          return self.__correo

      #Propiedades para cumplir el contrato del sistema
      #(reservas.py usa .nombre y .cedula)
       @property
       def nombre(self):
          return self.__nombre

       @property
       def cedula(self):
          return self.__identificacion

      #Validamos todos los datos y dejamos constancia en el log
       def validar(self):
          try:
              self.validar_nombre(self.__nombre)
              self.validar_identificacion(self.__identificacion)
              self.validar_telefono(self.__telefono)
              self.validar_correo(self.__correo)
          except ErrorCliente as error:
              registrar_evento(f"[ERROR] Cliente rechazado: {error}")
              raise
          else:
              registrar_evento(
                  f"[OK] Cliente registrado: {self.__nombre} "
                  f"(cedula {self.__identificacion})."
              )
              return True

      #Implementamos el método abstracto heredado de Entidad
       def obtener_informacion(self):
          return(
               f"Nombre: {self.__nombre}, "
               f"Identificación: {self.__identificacion}, "
               f"Teléfono: {self.__telefono}, "
               f"Correo: {self.__correo}"
               )
          
           
     