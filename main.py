"""
main.py
=======
Ejecucion:  python main.py

Version mejorada (carpeta mejoras/). Sobre el integrador original agrega:
1. Registro del inicio y fin de la simulacion en el log del sistema.
2. Conteo de demos ejecutadas, pendientes y fallidas, con resumen final.
"""

import importlib

# Registro de eventos del sistema (definido en excepciones.py)
try:
    from excepciones import registrar_evento
except ImportError:
    def registrar_evento(mensaje):
        """Respaldo vacio si el modulo de logs no existe."""

SEPARADOR = "=" * 64

# Orden de ejecucion: respeta el orden de integracion acordado en el
# contrato de interfaces (clientes -> servicios -> reservas).
DEMOS = [
    ("demo_clientes", "Clientes (feature/gestion-clientes)"),
    ("demo_servicios", "Servicios (feature/gestion-servicios)"),
    ("demo_reservas", "Reservas (feature/gestion-reservas)"),
]


def _ejecutar_demo(nombre_modulo, descripcion):
    """Ejecuta UNA demo del equipo con control total de errores.

    Devuelve uno de estos estados:
    - "ok":        la demo se ejecuto completa.
    - "pendiente": el modulo aun no existe en el proyecto.
    - "fallida":   la demo fallo en ejecucion (error capturado).
    """
    print(f"\n{SEPARADOR}")
    print(f"  Ejecutando: {nombre_modulo} ({descripcion})")
    print(SEPARADOR)

    try:
        # Import dinamico: el modulo puede existir o no segun el avance
        # de cada rama del equipo.
        modulo = importlib.import_module(nombre_modulo)
    except ModuleNotFoundError:
        print(f"[PENDIENTE] El modulo '{nombre_modulo}' aun no existe.")
        print("           Se activara cuando su rama se fusione a main.")
        return "pendiente"

    try:
        modulo.main()
    except Exception as error:
        # El integrador NO debe morir: registra el error y continua.
        print(f"[ERROR CONTROLADO] La demo fallo: "
              f"{type(error).__name__}: {error}")
        print("El sistema continua con la siguiente demo.")
        return "fallida"
    print("El sistema continua con la siguiente demo.")
    return "ok"


def main():
    """Ejecuta las demos de todo el equipo y muestra un resumen final."""
    registrar_evento("[OK] Inicio de la simulacion del sistema.")
    print(SEPARADOR)
    print("  SISTEMA DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS")
    print("  Fase 4 - Simulacion de las operaciones del equipo")
    print(SEPARADOR)

    resultados = []
    for nombre, descripcion in DEMOS:
        resultados.append((nombre, _ejecutar_demo(nombre, descripcion)))

    # Resumen final: conteo de demos por estado.
    ejecutadas = sum(1 for _, estado in resultados if estado == "ok")
    pendientes = sum(1 for _, estado in resultados if estado == "pendiente")
    fallidas = sum(1 for _, estado in resultados if estado == "fallida")

    print(f"\n{SEPARADOR}")
    print("  RESUMEN DE LA SIMULACION")
    print("-" * 64)
    print(f"  Demos ejecutadas: {ejecutadas}")
    print(f"  Demos pendientes: {pendientes}")
    print(f"  Demos fallidas:   {fallidas}")
    print(SEPARADOR)

    registrar_evento(
        f"[OK] Fin de la simulacion: {ejecutadas} ejecutadas, "
        f"{pendientes} pendientes, {fallidas} fallidas."
    )
    print("  FIN DE LA SIMULACION: el sistema termino sin interrumpirse.")
    print(SEPARADOR)


if __name__ == "__main__":
    main()
