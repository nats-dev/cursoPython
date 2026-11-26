"""Genera datos de ejemplo para probar la aplicación y sacar capturas.

Uso:
    python -m scripts.datos_demo                 # escribe en datos/
    python -m scripts.datos_demo --carpeta otra  # escribe en otra carpeta

Usa una semilla fija, así que siempre genera los mismos datos.
"""

import argparse
import random
from datetime import date, timedelta

from habitos.almacen import AlmacenCSV
from habitos.gestor import GestorHabitos

DIAS_HISTORIAL = 90

# (nombre, descripción, veces por semana, probabilidad de cumplir cada día que toca)
HABITOS = [
    ("Leer 20 minutos", "Antes de dormir, sin móvil.", 7, 0.80),
    ("Beber 2 litros de agua", "", 7, 0.65),
    ("Salir a correr", "Mejor por la mañana.", 3, 0.55),
    ("Estudiar Python", "Una hora de práctica con el curso.", 5, 0.70),
    ("Meditar", "", 7, 0.35),
]


def generar(hoy: date, semilla: int = 42) -> GestorHabitos:
    azar = random.Random(semilla)
    inicio = hoy - timedelta(days=DIAS_HISTORIAL)
    gestor = GestorHabitos()
    for nombre, descripcion, veces, probabilidad in HABITOS:
        habito = gestor.crear(nombre, inicio, veces, descripcion)
        # los hábitos semanales se concentran en unos días fijos de la semana
        dias_buenos = sorted(azar.sample(range(7), veces))
        for n in range(DIAS_HISTORIAL + 1):
            dia = inicio + timedelta(days=n)
            if dia.weekday() in dias_buenos and azar.random() < probabilidad:
                gestor.marcar(habito.id, dia, hoy)
    return gestor


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--carpeta", default="datos", help="carpeta de destino (por defecto: datos)")
    args = parser.parse_args()

    gestor = generar(date.today())
    AlmacenCSV(args.carpeta).guardar(gestor)
    print(f"Datos de demostración guardados en {args.carpeta}/ ({len(gestor.todos())} hábitos).")


if __name__ == "__main__":
    main()
