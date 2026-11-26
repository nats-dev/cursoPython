"""Persistencia en CSV.

Dos ficheros en la carpeta de datos:

* ``habitos.csv``   → id, nombre, descripcion, veces_semana, creado, archivado
* ``registros.csv`` → habito_id, fecha   (una fila por día cumplido)

Se escribe primero en un fichero temporal y después se renombra, de modo que
un fallo a mitad de escritura nunca deja un CSV a medias.
"""

import csv
import os
from datetime import date
from pathlib import Path

from habitos.excepciones import ErrorAlmacen, ErrorHabitos
from habitos.gestor import GestorHabitos
from habitos.modelo import Habito

CAMPOS_HABITOS = ["id", "nombre", "descripcion", "veces_semana", "creado", "archivado"]
CAMPOS_REGISTROS = ["habito_id", "fecha"]


class AlmacenCSV:
    def __init__(self, carpeta):
        self.carpeta = Path(carpeta)

    @property
    def ruta_habitos(self) -> Path:
        return self.carpeta / "habitos.csv"

    @property
    def ruta_registros(self) -> Path:
        return self.carpeta / "registros.csv"

    # ---- lectura ---------------------------------------------------------
    def cargar(self) -> GestorHabitos:
        """Lee los ficheros y devuelve un gestor. Si no existen, un gestor vacío."""
        habitos = self._leer_habitos()
        self._leer_registros(habitos)
        return GestorHabitos(habitos.values())

    def _leer_habitos(self) -> dict[int, Habito]:
        ruta = self.ruta_habitos
        habitos: dict[int, Habito] = {}
        if not ruta.exists():
            return habitos
        try:
            with open(ruta, encoding="utf-8", newline="") as f:
                for n, fila in enumerate(csv.DictReader(f), start=2):
                    try:
                        habito = Habito(
                            id=int(fila["id"]),
                            nombre=fila["nombre"],
                            veces_semana=int(fila["veces_semana"]),
                            descripcion=fila["descripcion"],
                            creado=date.fromisoformat(fila["creado"]),
                            archivado=fila["archivado"] == "1",
                        )
                    except (KeyError, TypeError, ValueError, ErrorHabitos) as e:
                        raise ErrorAlmacen(f"{ruta.name}, línea {n}: {e}") from e
                    if habito.id in habitos:
                        raise ErrorAlmacen(f"{ruta.name}, línea {n}: id {habito.id} repetido")
                    habitos[habito.id] = habito
        except OSError as e:
            raise ErrorAlmacen(f"No se pudo leer {ruta}: {e}") from e
        return habitos

    def _leer_registros(self, habitos: dict[int, Habito]) -> None:
        ruta = self.ruta_registros
        if not ruta.exists():
            return
        try:
            with open(ruta, encoding="utf-8", newline="") as f:
                for n, fila in enumerate(csv.DictReader(f), start=2):
                    try:
                        id_habito = int(fila["habito_id"])
                        fecha = date.fromisoformat(fila["fecha"])
                    except (KeyError, TypeError, ValueError) as e:
                        raise ErrorAlmacen(f"{ruta.name}, línea {n}: {e}") from e
                    if id_habito not in habitos:
                        raise ErrorAlmacen(f"{ruta.name}, línea {n}: el hábito {id_habito} no existe")
                    habitos[id_habito].fechas.add(fecha)
        except OSError as e:
            raise ErrorAlmacen(f"No se pudo leer {ruta}: {e}") from e

    # ---- escritura -------------------------------------------------------
    def guardar(self, gestor: GestorHabitos) -> None:
        habitos = gestor.todos()
        filas_habitos = [
            {
                "id": h.id,
                "nombre": h.nombre,
                "descripcion": h.descripcion,
                "veces_semana": h.veces_semana,
                "creado": h.creado.isoformat(),
                "archivado": int(h.archivado),
            }
            for h in habitos
        ]
        filas_registros = [
            {"habito_id": h.id, "fecha": fecha.isoformat()}
            for h in habitos
            for fecha in sorted(h.fechas)
        ]
        try:
            self.carpeta.mkdir(parents=True, exist_ok=True)
            self._escribir(self.ruta_habitos, CAMPOS_HABITOS, filas_habitos)
            self._escribir(self.ruta_registros, CAMPOS_REGISTROS, filas_registros)
        except OSError as e:
            raise ErrorAlmacen(f"No se pudo guardar en {self.carpeta}: {e}") from e

    @staticmethod
    def _escribir(ruta: Path, campos: list[str], filas: list[dict]) -> None:
        temporal = ruta.parent / (ruta.name + ".tmp")
        with open(temporal, "w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(filas)
        os.replace(temporal, ruta)
