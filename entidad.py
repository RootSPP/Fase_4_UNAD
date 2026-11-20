#Importamos las herramientas necesarias para crear una clase abstracta
from abc import ABC, abstractmethod

#Clase abstracta que representa las entidades generales del sistema 
class Entidad(ABC):
    
    #Método abstracto para obtener la información de cada entidad
    @abstractmethod
    def obtener_informacion(self):
        pass
    
