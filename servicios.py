# -*- coding: utf-8 -*-
"""
servicios.py
Rama: feature/gestion-servicios
Clase abstracta Servicio + ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
Cumple el contrato de reservas.py: atributos nombre y disponible,
validar_parametros() y calcular_costo(impuesto=..., descuento=...).
"""
from abc import ABC, abstractmethod

try:
    from excepciones import registrar_evento
except ImportError:
    # Respaldo temporal mientras llega excepciones.py
    import logging
    logging.basicConfig(filename="registro_eventos.log", level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        encoding="utf-8")
    _logger = logging.getLogger("servicios")

    def registrar_evento(mensaje):
        _logger.info(mensaje)


# ---------------- Excepciones propias del módulo ----------------
class ServicioError(Exception):
    """Base de los errores de servicios."""

class ServicioInvalidoError(ServicioError):
    """Datos o parámetros inválidos del servicio."""

class ServicioNoDisponibleError(ServicioError):
    """El servicio no está disponible."""

class CalculoError(ServicioError):
    """Error al calcular el costo."""


# ---------------- Clase abstracta ----------------
class Servicio(ABC):
    def __init__(self, id_servicio, nombre, tarifa_hora, disponible=True):
        try:
            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("El nombre no puede estar vacio.")
            if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
                raise ValueError("La tarifa debe ser un numero mayor que cero.")
        except ValueError as error:
            registrar_evento(f"[ERROR] Servicio invalido ({id_servicio}): {error}")
            raise ServicioInvalidoError(f"Servicio invalido: {error}") from error
        self._id_servicio = id_servicio
        self._nombre = nombre.strip()
        self._tarifa_hora = tarifa_hora
        self._disponible = disponible

    # Encapsulación: solo lectura
    @property
    def id_servicio(self):
        return self._id_servicio

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    # Disponibilidad
    def verificar_disponibilidad(self):
        if not self._disponible:
            mensaje = f"El servicio '{self._nombre}' no esta disponible."
            registrar_evento(f"[ERROR] {mensaje}")
            raise ServicioNoDisponibleError(mensaje)
        return True

    def marcar_no_disponible(self):
        self._disponible = False

    def liberar(self):
        self._disponible = True

    # Métodos que cada hijo sobrescribe (polimorfismo)
    @abstractmethod
    def validar_parametros(self, horas=1):
        ...

    @abstractmethod
    def _costo_base(self, horas):
        ...

    @abstractmethod
    def describir(self):
        ...

    # "Sobrecarga" con parámetros opcionales:
    # calcular_costo() / calcular_costo(2) / calcular_costo(2, 0.19) /
    # calcular_costo(2, 0.19, 0.10) / calcular_costo(impuesto=0.19)
    def calcular_costo(self, horas=1, impuesto=0.0, descuento=0.0):
        try:
            self.validar_parametros(horas)
            if not (0 <= impuesto <= 1) or not (0 <= descuento <= 1):
                raise CalculoError("Impuesto y descuento deben estar entre 0 y 1.")
            total = self._costo_base(horas) * (1 - descuento) * (1 + impuesto)
        except (ServicioInvalidoError, CalculoError) as error:
            registrar_evento(f"[ERROR] Costo de '{self._nombre}': {error}")
            raise
        except TypeError as error:
            registrar_evento(f"[ERROR] Tipo incorrecto en '{self._nombre}': {error}")
            raise CalculoError("Parametros de calculo invalidos.") from error
        else:
            registrar_evento(f"[OK] Costo de '{self._nombre}' calculado: {round(total, 2)}")
            return round(total, 2)


# ---------------- Servicios especializados ----------------
class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            registrar_evento(f"[ERROR] Capacidad invalida en sala {id_servicio}")
            raise ServicioInvalidoError("La capacidad debe ser un entero mayor que cero.")
        self._capacidad = capacidad

    def validar_parametros(self, horas=1):
        if not isinstance(horas, (int, float)) or not 0 < horas <= 12:
            raise ServicioInvalidoError("Una sala se reserva entre 0 y 12 horas.")

    def _costo_base(self, horas):
        return self._tarifa_hora * horas

    def describir(self):
        return f"Sala '{self._nombre}' para {self._capacidad} personas, ${self._tarifa_hora}/hora"


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_hora, deposito=0, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not isinstance(deposito, (int, float)) or deposito < 0:
            registrar_evento(f"[ERROR] Deposito invalido en equipo {id_servicio}")
            raise ServicioInvalidoError("El deposito no puede ser negativo.")
        self._deposito = deposito

    def validar_parametros(self, horas=1):
        if not isinstance(horas, (int, float)) or not 0 < horas <= 72:
            raise ServicioInvalidoError("Un equipo se alquila entre 0 y 72 horas.")

    def _costo_base(self, horas):
        return self._tarifa_hora * horas + self._deposito

    def describir(self):
        return f"Equipo '{self._nombre}', ${self._tarifa_hora}/hora + deposito ${self._deposito}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_hora, especialidad,
                 recargo_experto=0.25, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            registrar_evento(f"[ERROR] Especialidad invalida en asesoria {id_servicio}")
            raise ServicioInvalidoError("La especialidad es obligatoria.")
        self._especialidad = especialidad.strip()
        self._recargo_experto = recargo_experto

    def validar_parametros(self, horas=1):
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 8:
            raise ServicioInvalidoError("Una asesoria dura entre 0.5 y 8 horas.")

    def _costo_base(self, horas):
        return self._tarifa_hora * horas * (1 + self._recargo_experto)

    def describir(self):
        return (f"Asesoria de {self._especialidad} con '{self._nombre}', "
                f"${self._tarifa_hora}/hora (+{int(self._recargo_experto * 100)}% experto)")
