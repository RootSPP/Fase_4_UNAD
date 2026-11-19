# -*- coding: utf-8 -*-
"""
reservas.py
===========
Fase 4 - Sistema Integral de Gestion de Clientes, Servicios y Reservas.
Rama: feature/gestion-reservas.

Este modulo implementa la clase `Reserva` (que integra cliente, servicio,
duracion y estado) junto con el manejo avanzado de excepciones que exige
el ejercicio: excepciones personalizadas, bloques try/except/else/finally
y encadenamiento de excepciones (raise ... from ...).

------------------------------------------------------------
CONTRATO DE INTERFAZ CON LOS OTROS MODULOS DEL EQUIPO
------------------------------------------------------------
Este modulo fue escrito contra interfaces (duck typing) y NO importa
los modulos de los demas integrantes: recibe los objetos por parametro
y solo exige que cumplan lo siguiente:

* Cliente (modulo `entidades.py`):
    - atributo publico `nombre` (str)
    - atributo publico `cedula` (str)
    - metodo `validar()` que lanza una excepcion si el cliente es invalido

* Servicio (modulo `servicios.py`):
    - atributo publico `nombre` (str)
    - atributo publico `disponible` (bool)
    - metodo `validar_parametros(*args, **kwargs)` que lanza una excepcion
      si los parametros del servicio no son validos
    - metodo `calcular_costo(impuesto=..., descuento=..., **kwargs)` que
      devuelve el costo (float). Debe aceptar como minimo los argumentos
      por palabra clave `impuesto` y `descuento`.

* Registro de eventos (modulo `excepciones.py`):
    - funcion `registrar_evento(mensaje: str) -> None` que escribe el
      evento/error en el archivo de logs del sistema.
      Mientras ese modulo no exista, este archivo usa un respaldo con el
      modulo estandar `logging` (ver `_registrar_evento_equipo`).
"""

from enum import Enum


# ---------------------------------------------------------------------------
# 1. Excepciones personalizadas del dominio de reservas
# ---------------------------------------------------------------------------
class ReservaError(Exception):
    """Clase base de todos los errores del dominio de reservas.

    Todas las excepciones de este modulo heredan de aqui, de modo que
    quien use la clase Reserva pueda capturarlas en bloque con un unico
    `except ReservaError`.
    """


class ReservaInvalidaError(ReservaError):
    """Los datos con los que se intento crear la reserva no son validos.

    Se lanza cuando el cliente o el servicio no pasan su validacion, o
    cuando la duracion es menor o igual a cero.
    """


class EstadoReservaError(ReservaError):
    """Se intento una transicion de estado no permitida.

    Ejemplos: confirmar una reserva ya cancelada, o procesar una reserva
    que nunca fue confirmada.
    """


class ServicioNoDisponibleError(ReservaError):
    """El servicio solicitado no esta disponible para reservar."""


# ---------------------------------------------------------------------------
# 2. Estados del ciclo de vida de una reserva (constantes tipadas)
# ---------------------------------------------------------------------------
class EstadoReserva(Enum):
    """Estados posibles de una reserva.

    Usar Enum evita comparar cadenas sueltas ("confirmada", "cancela",
    etc.) y previene errores de digitacion.
    """

    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    COMPLETADA = "completada"

    def __str__(self):
        """Permite imprimir 'confirmada' en vez de 'EstadoReserva.CONFIRMADA'."""
        return self.value


# ---------------------------------------------------------------------------
# 3. Registro de eventos (respaldo local mientras llega excepciones.py)
# ---------------------------------------------------------------------------
try:
    # Si el modulo de logs del sistema ya esta disponible, se usa su funcion.
    # De esta forma TODOS los modulos escriben en el mismo archivo.
    from excepciones import registrar_evento as _registrar_evento_equipo
except ImportError:
    # Respaldo temporal: el modulo estandar logging escribe en un archivo
    # local mientras el modulo real del equipo no exista.
    import logging

    logging.basicConfig(
        filename="registro_eventos.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8",
    )
    _logger = logging.getLogger("reservas")

    def _registrar_evento_equipo(mensaje):
        """Escribe el mensaje en el log local (respaldo temporal)."""
        _logger.info(mensaje)


# ---------------------------------------------------------------------------
# 4. Clase Reserva
# ---------------------------------------------------------------------------
class Reserva:
    """Reserva de un servicio por parte de un cliente.

    Integra: cliente, servicio, duracion y estado. El estado solo puede
    cambiarse a traves de los metodos confirmar(), cancelar() y
    procesar() (encapsulamiento: no existe setter publico del estado).
    """

    # Tabla de transiciones validas de estado (maquina de estados).
    # CANCELADA y COMPLETADA son estados finales: no aparecen como clave.
    _TRANSICIONES = {
        EstadoReserva.PENDIENTE: {EstadoReserva.CONFIRMADA, EstadoReserva.CANCELADA},
        EstadoReserva.CONFIRMADA: {EstadoReserva.CANCELADA, EstadoReserva.COMPLETADA},
    }

    def __init__(self, cliente, servicio, duracion, estado=EstadoReserva.PENDIENTE):
        """Crea la reserva validando cliente, servicio y duracion.

        Si algo no es valido se lanza ReservaInvalidaError conservando la
        causa original mediante encadenamiento (`raise ... from error`),
        de forma que el rastreo de la causa raiz no se pierda.
        """
        try:
            # Validaciones basicas de presencia y tipos.
            if cliente is None:
                raise ValueError("El cliente es obligatorio (None).")
            if servicio is None:
                raise ValueError("El servicio es obligatorio (None).")
            if not isinstance(duracion, (int, float)) or duracion <= 0:
                raise ValueError("La duracion debe ser un numero mayor que cero.")

            # Validaciones delegadas a los objetos recibidos (contrato).
            cliente.validar()
            servicio.validar_parametros()
        except Exception as error:
            # Encadenamiento: se conserva la excepcion original como causa.
            raise ReservaInvalidaError(f"Reserva invalida: {error}") from error

        # Encapsulamiento: los atributos se guardan privados y se exponen
        # solo a traves de propiedades de lectura.
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = float(duracion)
        self._estado = estado

        _registrar_evento_equipo(
            f"[OK] Reserva creada para {cliente.nombre} "
            f"(servicio: {servicio.nombre}, duracion: {duracion})."
        )

    # ------------------------------------------------------------------
    # Propiedades (solo lectura) -> encapsulamiento de los datos.
    # ------------------------------------------------------------------
    @property
    def cliente(self):
        """Cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self):
        """Servicio asociado a la reserva."""
        return self._servicio

    @property
    def duracion(self):
        """Duracion de la reserva en horas."""
        return self._duracion

    @property
    def estado(self):
        """Estado actual de la reserva.

        Es de solo lectura a proposito: el cambio de estado solo ocurre
        a traves de confirmar(), cancelar() y procesar().
        """
        return self._estado

    # ------------------------------------------------------------------
    # Metodo auxiliar: valida la maquina de estados.
    # ------------------------------------------------------------------
    def _validar_transicion(self, destino):
        """Verifica que el paso al estado `destino` este permitido.

        Lanza EstadoReservaError si la transicion no existe en la tabla.
        """
        permitidos = self._TRANSICIONES.get(self._estado, set())
        if destino not in permitidos:
            raise EstadoReservaError(
                f"Transicion no permitida: '{self._estado}' -> '{destino}'."
            )

    # ------------------------------------------------------------------
    # Operaciones de la reserva (con try/except/else/finally).
    # ------------------------------------------------------------------
    def confirmar(self):
        """Confirma la reserva si esta pendiente y el servicio disponible.

        Uso didactico de try/except/else/finally:
        - try:     valida el estado y la disponibilidad.
        - except:  registra el error y lo relanza.
        - else:    solo se ejecuta si NO hubo error (cambia el estado).
        - finally: se ejecuta SIEMPRE (registra el intento en el log).
        """
        try:
            self._validar_transicion(EstadoReserva.CONFIRMADA)
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre}' no esta disponible."
                )
        except (EstadoReservaError, ServicioNoDisponibleError) as error:
            # Se registra el error y se relanza: quien llame decide.
            _registrar_evento_equipo(f"[ERROR] Confirmacion fallida: {error}")
            raise
        else:
            self._estado = EstadoReserva.CONFIRMADA
            _registrar_evento_equipo(
                f"[OK] Reserva de {self.cliente.nombre} confirmada."
            )
            return True
        finally:
            _registrar_evento_equipo(
                f"[EVENTO] Intento de confirmacion terminado "
                f"(estado final: '{self._estado}')."
            )

    def cancelar(self):
        """Cancela la reserva si aun es posible.

        Solo se puede cancelar una reserva PENDIENTE o CONFIRMADA.
        Misma estructura try/except/else/finally que confirmar().
        """
        try:
            self._validar_transicion(EstadoReserva.CANCELADA)
        except EstadoReservaError as error:
            _registrar_evento_equipo(f"[ERROR] Cancelacion fallida: {error}")
            raise
        else:
            self._estado = EstadoReserva.CANCELADA
            _registrar_evento_equipo(
                f"[OK] Reserva de {self.cliente.nombre} cancelada."
            )
            return True
        finally:
            _registrar_evento_equipo(
                f"[EVENTO] Intento de cancelacion terminado "
                f"(estado final: '{self._estado}')."
            )

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Procesa una reserva confirmada y devuelve el costo total.

        - Solo se puede procesar una reserva CONFIRMADA.
        - El costo se calcula delegando en el servicio, con impuesto y
          descuento opcionales (la "sobrecarga" del calculo de costos
          vive en el modulo de servicios).
        - Demuestra encadenamiento: cualquier error del servicio se
          relanza envuelto en ReservaError con `raise ... from ...`
          para no perder la causa raiz.
        """
        try:
            self._validar_transicion(EstadoReserva.COMPLETADA)
            costo_total = self.servicio.calcular_costo(
                impuesto=impuesto, descuento=descuento
            )
        except EstadoReservaError as error:
            raise ReservaError(f"No se puede procesar la reserva: {error}") from error
        except Exception as error:
            raise ReservaError(
                f"Error calculando el costo del servicio: {error}"
            ) from error
        else:
            self._estado = EstadoReserva.COMPLETADA
            _registrar_evento_equipo(
                f"[OK] Reserva de {self.cliente.nombre} procesada "
                f"(costo total: {costo_total})."
            )
            return costo_total
        finally:
            _registrar_evento_equipo(
                f"[EVENTO] Intento de procesamiento terminado "
                f"(estado final: '{self._estado}')."
            )

    def calcular_total(self, impuesto=0.0, descuento=0.0, **opciones):
        """Calcula el costo SIN cambiar el estado de la reserva.

        Util para cotizar antes de confirmar. Los parametros opcionales
        los resuelve el servicio (sobrecarga de metodos).
        """
        try:
            return self.servicio.calcular_costo(
                impuesto=impuesto, descuento=descuento, **opciones
            )
        except Exception as error:
            raise ReservaError(
                f"No se pudo calcular el total de la reserva: {error}"
            ) from error

    # ------------------------------------------------------------------
    # Representacion en texto.
    # ------------------------------------------------------------------
    def __str__(self):
        """Descripcion legible de la reserva."""
        return (
            f"Reserva(cliente={self.cliente.nombre}, "
            f"servicio={self.servicio.nombre}, "
            f"duracion={self.duracion}h, estado='{self.estado}')"
        )

    def __repr__(self):
        """Representacion para depuracion (usa la misma que str)."""
        return self.__str__()
