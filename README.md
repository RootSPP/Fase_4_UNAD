# Sistema de Gestión de Clientes, Servicios y Reservas — Software FJ

**Curso:** Programación 213023 — Fase 4 · Universidad Nacional Abierta y a Distancia (UNAD)
**Repositorio:** https://github.com/RootSPP/Fase_4_UNAD

## Descripción

Sistema integral orientado a objetos, **sin uso de bases de datos**, que gestiona
clientes, servicios y reservas para la empresa **Software FJ**, la cual ofrece tres
tipos de servicios: reserva de salas, alquiler de equipos y asesorías especializadas.

El sistema demuestra los principios de **abstracción, herencia, polimorfismo y
encapsulamiento**, junto con **manejo avanzado de excepciones** (excepciones
personalizadas, bloques `try/except/else/finally` y encadenamiento de excepciones).
Toda la información se maneja mediante objetos y listas; el único archivo persistente
es el **log de eventos y errores**.


## Estructura del proyecto

```text
Fase_4_UNAD/
├── main.py               # Integrador: ejecuta las 3 demos del equipo
├── excepciones.py        # Excepciones personalizadas + registrar_evento()
├── entidad.py            # Clase abstracta Entidad
├── cliente.py            # Cliente con validaciones y encapsulamiento
├── servicios.py          # Servicio abstracto + 3 servicios derivados
├── reservas.py           # Clase Reserva + máquina de estados
├── demo_clientes.py      # Demo: 5 operaciones (válidas e inválidas)
├── demo_servicios.py     # Demo: 8 operaciones (válidas e inválidas)
├── demo_reservas.py      # Demo: 4 operaciones (válidas e inválidas)
└── registro_eventos.log  # Log de eventos y errores (no se versiona)
```

## Cómo ejecutar

Solo se necesita Python 3 (sin dependencias externas):

```bash
python main.py          # simulación completa (17 operaciones)
python demo_clientes.py # solo el módulo de clientes
python demo_servicios.py
python demo_reservas.py
```

## Archivo de logs

Cada ejecución registra eventos y errores con fecha y hora en
`registro_eventos.log`. Gracias al manejo de excepciones, el sistema
**continúa funcionando** después de cada error.

## Operaciones simuladas

17 operaciones que mezclan registros válidos e inválidos:

- **Clientes (5):** 1 válido + 4 inválidos (nombre, cédula, teléfono, correo).
- **Servicios (8):** 2 válidas (polimorfismo y sobrecarga de costos) + 6 inválidas
  (capacidad, tarifa, duración, impuesto, disponibilidad, clase abstracta).
- **Reservas (4):** 1 válida (confirmar → procesar) + 3 inválidas (servicio no
  disponible, duración inválida, cancelar y luego procesar).

## Convención del equipo

- Ramas: `feature/<modulo>` → Pull Request → `main` (orden: clientes → servicios → reservas).
- Commits pequeños con mensajes claros.
- No se suben logs ni secretos (ver `.gitignore`).
