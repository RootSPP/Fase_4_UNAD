"""
main.py
=======
Ejecucion:  python main.py
"""

import importlib

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

    Nunca lanza excepciones hacia afuera: cualquier falla se reporta y
    el sistema sigue con la siguiente demo.
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
        return

    try:
        modulo.main()
    except Exception as error:
        # El integrador NO debe morir: registra el error y continua.
        print(f"[ERROR CONTROLADO] La demo fallo: "
              f"{type(error).__name__}: {error}")
    finally:
        print("El sistema continua con la siguiente demo.")


def main():
    """Ejecuta las demos de todo el equipo en el orden acordado."""
    print(SEPARADOR)
    print("  SISTEMA DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS")
    print("  Fase 4 - Simulacion de las operaciones del equipo")
    print(SEPARADOR)

    for nombre, descripcion in DEMOS:
        _ejecutar_demo(nombre, descripcion)

    print(f"\n{SEPARADOR}")
    print("  FIN DE LA SIMULACION: el sistema termino sin interrumpirse.")
    print(SEPARADOR)


if __name__ == "__main__":
    main()
