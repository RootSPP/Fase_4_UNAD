# -*- coding: utf-8 -*-
"""
demo_reservas.py
================
Fase 4 | Rama: feature/gestion-reservas.
Ejecucion:  python demo_reservas.py
"""

from reservas import Reserva, ReservaError

SEPARADOR = "=" * 64
LINEA = "-" * 64


class _ClientePrueba:
    """Stub que cumple el contrato de Cliente (entidades.py).

    Solo existe para probar este modulo de forma aislada: se sustituye
    automaticamente por la clase real en la integracion final.
    """

    def __init__(self, nombre, cedula, es_valido=True):
        self.nombre = nombre
        self.cedula = cedula
        self._es_valido = es_valido

    def validar(self):
        """Simula la validacion del cliente real."""
        if not self._es_valido:
            raise ValueError(f"Cliente '{self.nombre}': datos invalidos.")


class _ServicioPrueba:
    """Stub que cumple el contrato de Servicio (servicios.py)."""

    def __init__(self, nombre, disponible=True, costo_base=100000.0):
        self.nombre = nombre
        self.disponible = disponible
        self._costo_base = costo_base

    def validar_parametros(self, *args, **kwargs):
        """En el stub los parametros siempre son validos."""
        return True

    def calcular_costo(self, impuesto=0.0, descuento=0.0, **kwargs):
        """Formula simple de prueba: base + impuesto - descuento %.

        El descuento se maneja como porcentaje (0.0 a 1.0), igual que
        el servicio real del modulo servicios.py.
        """
        subtotal = self._costo_base * (1 + impuesto)
        return max(subtotal * (1 - descuento), 0.0)


def _cabecera(titulo):
    """Imprime la cabecera de cada operacion del demo."""
    print(f"\n{SEPARADOR}")
    print(f"  {titulo}")
    print(LINEA)


def main():
    """Ejecuta las 4 operaciones de demostracion del modulo de reservas."""
    print(SEPARADOR)
    print("  DEMO DE RESERVAS - Fase 4")
    print(SEPARADOR)

    # ------------------------------------------------------------------
    # Operacion 1 (VALIDA): reserva confirmada y procesada con exito.
    # ------------------------------------------------------------------
    _cabecera("Operacion 1: reserva valida -> confirmar -> procesar [OK]")
    try:
        cliente = _ClientePrueba("Laura Gomez", "1032456789")
        servicio = _ServicioPrueba(
            "Alquiler de equipo de video", costo_base=150000.0
        )
        reserva = Reserva(cliente, servicio, duracion=3)

        cotizacion = reserva.calcular_total(impuesto=0.19, descuento=0.10)
        print(f"Cotizacion (impuesto 19%, descuento 10%): {cotizacion}")

        reserva.confirmar()
        print(f"Estado despues de confirmar: '{reserva.estado}'")

        total = reserva.procesar(impuesto=0.19, descuento=0.10)
        print(f"Estado despues de procesar: '{reserva.estado}'")
        print(f"Total pagado: {total}")
        print(f"Resumen: {reserva}")
    except ReservaError as error:
        print(f"[ERROR NO ESPERADO] {error}")

    # ------------------------------------------------------------------
    # Operacion 2 (INVALIDA): servicio no disponible al confirmar.
    # ------------------------------------------------------------------
    _cabecera("Operacion 2: servicio NO disponible [ERROR CONTROLADO]")
    try:
        cliente = _ClientePrueba("Pedro Rojas", "1014235678")
        servicio = _ServicioPrueba(
            "Reserva de sala de juntas", disponible=False
        )
        reserva = Reserva(cliente, servicio, duracion=2)
        reserva.confirmar()  # Aqui debe fallar: el servicio no esta disponible.
    except ReservaError as error:
        print(f"[ERROR CONTROLADO] {error}")
    finally:
        print("El sistema continua funcionando despues del error.")

    # ------------------------------------------------------------------
    # Operacion 3 (INVALIDA): duracion no valida al crear la reserva.
    # ------------------------------------------------------------------
    _cabecera("Operacion 3: duracion invalida [ERROR CONTROLADO]")
    try:
        cliente = _ClientePrueba("Ana Torres", "1045678123")
        servicio = _ServicioPrueba(
            "Asesoria especializada", costo_base=200000.0
        )
        Reserva(cliente, servicio, duracion=0)  # Aqui debe fallar.
    except ReservaError as error:
        print(f"[ERROR CONTROLADO] {error}")
        # Encadenamiento: se muestra tambien la causa original del error.
        print(f"  Causa original: {error.__cause__}")
    finally:
        print("El sistema continua funcionando despues del error.")

    # ------------------------------------------------------------------
    # Operacion 4 (INVALIDA): cancelar y luego intentar procesar.
    # ------------------------------------------------------------------
    _cabecera("Operacion 4: cancelar y luego procesar [ERROR CONTROLADO]")
    try:
        cliente = _ClientePrueba("Carlos Diaz", "1053456721")
        servicio = _ServicioPrueba(
            "Reserva de sala de juntas", costo_base=120000.0
        )
        reserva = Reserva(cliente, servicio, duracion=1)
        reserva.confirmar()
        reserva.cancelar()
        print(f"Estado despues de cancelar: '{reserva.estado}'")
        reserva.procesar()  # Aqui debe fallar: ya esta cancelada.
    except ReservaError as error:
        print(f"[ERROR CONTROLADO] {error}")
        print(f"  Causa original: {error.__cause__}")
    finally:
        print("El sistema continua funcionando despues del error.")

    # ------------------------------------------------------------------
    print(f"\n{SEPARADOR}")
    print("  RESULTADO: 4 operaciones ejecutadas, el sistema sigue vivo.")
    print(SEPARADOR)


if __name__ == "__main__":
    main()
