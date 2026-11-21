# -*- coding: utf-8 -*-
"""
demo_servicios.py
=================
Fase 4 | Rama: feature/gestion-servicios.

Demostracion del modulo servicios.py: clase abstracta Servicio y sus
derivadas (ReservaSala, AlquilerEquipo, AsesoriaEspecializada).

Es el archivo que busca main.py (importa `demo_servicios` y llama a
su funcion main()), por eso el nombre y la funcion main() no deben
cambiarse.

Ejecucion: python demo_servicios.py
"""

from servicios import (
    Servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    ServicioError,
)

SEPARADOR = "=" * 64
LINEA = "-" * 64


def _cabecera(titulo):
    """Imprime la cabecera de cada operacion del demo."""
    print(f"\n{SEPARADOR}")
    print(f" {titulo}")
    print(LINEA)


def main():
    """Ejecuta las 8 operaciones de demostracion del modulo de servicios."""
    print(SEPARADOR)
    print(" DEMO DE SERVICIOS - Fase 4")
    print(SEPARADOR)

    # Servicios validos que se reutilizan en varias operaciones.
    sala = ReservaSala("S1", "Sala Jupiter", 50000, 10)
    equipo = AlquilerEquipo("E1", "Proyector 4K", 20000, deposito=30000)
    asesoria = AsesoriaEspecializada("A1", "Ing. Perez", 80000, "Redes")

    # ------------------------------------------------------------------
    # Operacion 1 (VALIDA): polimorfismo con describir().
    # ------------------------------------------------------------------
    _cabecera("Operacion 1: creacion de 3 servicios y polimorfismo [OK]")
    for servicio in (sala, equipo, asesoria):
        # Mismo metodo, resultado distinto segun la clase hija.
        print(f" - {servicio.describir()}")

    # ------------------------------------------------------------------
    # Operacion 2 (VALIDA): calcular_costo sobrecargado.
    # ------------------------------------------------------------------
    _cabecera("Operacion 2: calcular_costo con parametros opcionales [OK]")
    try:
        print(f"Sala 2h (sin extras):               {sala.calcular_costo(2)}")
        print(f"Sala 2h + impuesto 19%:             {sala.calcular_costo(2, 0.19)}")
        print(f"Sala 2h + impuesto 19% + desc 10%:  "
              f"{sala.calcular_costo(2, 0.19, 0.10)}")
        print(f"Equipo 2h + impuesto + descuento:   "
              f"{equipo.calcular_costo(2, impuesto=0.19, descuento=0.10)}")
        print(f"Asesoria 2h + impuesto + descuento: "
              f"{asesoria.calcular_costo(2, impuesto=0.19, descuento=0.10)}")
    except ServicioError as error:
        print(f"[ERROR NO ESPERADO] {error}")

    # ------------------------------------------------------------------
    # Operacion 3 (INVALIDA): sala con capacidad no valida.
    # ------------------------------------------------------------------
    _cabecera("Operacion 3: sala con capacidad 0 [ERROR CONTROLADO]")
    try:
        ReservaSala("S2", "Sala Fantasma", 40000, 0)
    except ServicioError as error:
        print(f"[ERROR CONTROLADO] {type(error).__name__}: {error}")
    finally:
        print("El sistema continua funcionando despues del error.")

    # ------------------------------------------------------------------
    # Operacion 4 (INVALIDA): tarifa negativa (excepcion encadenada).
    # ------------------------------------------------------------------
    _cabecera("Operacion 4: equipo con tarifa negativa [ERROR CONTROLADO]")
    try:
        AlquilerEquipo("E2", "Portatil", -5000)
    except ServicioError as error:
        print(f"[ERROR CONTROLADO] {type(error).__name__}: {error}")
        # Encadenamiento: se muestra tambien la causa original.
        print(f" Causa original: {error.__cause__}")
    finally:
        print("El sistema continua funcionando despues del error.")

    # ------------------------------------------------------------------
    # Operacion 5 (INVALIDA): horas fuera del rango permitido.
    # ------------------------------------------------------------------
    _cabecera("Operacion 5: duracion fuera de rango [ERROR CONTROLADO]")
    for servicio, horas in ((sala, 50), (asesoria, 0.1)):
        try:
            servicio.calcular_costo(horas)
        except ServicioError as error:
            print(f"[ERROR CONTROLADO] {servicio.nombre} con {horas}h -> {error}")
        finally:
            print("El sistema continua funcionando despues del error.")

    # ------------------------------------------------------------------
    # Operacion 6 (INVALIDA): impuesto con tipo o valor incorrecto.
    # ------------------------------------------------------------------
    _cabecera("Operacion 6: impuesto invalido en el calculo [ERROR CONTROLADO]")
    for impuesto in ("abc", 5):
        try:
            sala.calcular_costo(2, impuesto)
        except ServicioError as error:
            print(f"[ERROR CONTROLADO] impuesto={impuesto!r} -> "
                  f"{type(error).__name__}: {error}")
            if error.__cause__ is not None:
                print(f" Causa original: {error.__cause__}")
        finally:
            print("El sistema continua funcionando despues del error.")

    # ------------------------------------------------------------------
    # Operacion 7 (INVALIDA y luego VALIDA): disponibilidad.
    # ------------------------------------------------------------------
    _cabecera("Operacion 7: servicio no disponible y liberacion [ERROR + OK]")
    equipo.marcar_no_disponible()
    print(f"Disponible: {equipo.disponible}")
    try:
        equipo.verificar_disponibilidad()
    except ServicioError as error:
        print(f"[ERROR CONTROLADO] {type(error).__name__}: {error}")
    finally:
        print("El sistema continua funcionando despues del error.")
    equipo.liberar()
    print(f"Tras liberar -> disponible: {equipo.verificar_disponibilidad()}")

    # ------------------------------------------------------------------
    # Operacion 8 (INVALIDA): la clase abstracta no se puede instanciar.
    # ------------------------------------------------------------------
    _cabecera("Operacion 8: instanciar clase abstracta [ERROR CONTROLADO]")
    try:
        Servicio("X1", "Generico", 1000)
    except TypeError as error:
        print(f"[ERROR CONTROLADO] TypeError: {error}")
    finally:
        print("El sistema continua funcionando despues del error.")

    # ------------------------------------------------------------------
    print(f"\n{SEPARADOR}")
    print(" RESULTADO: 8 operaciones ejecutadas, el sistema sigue vivo.")
    print(SEPARADOR)


if __name__ == "__main__":
    main()
