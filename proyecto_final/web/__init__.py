"""Capa web (Flask). Solo traduce entre HTTP y el núcleo ``habitos``."""

import os
from datetime import date
from pathlib import Path

from flask import Flask, render_template

from habitos.excepciones import ErrorAlmacen, HabitoNoEncontrado
from web import formato
from web.rutas import bp


def create_app(carpeta_datos=None, hoy=None) -> Flask:
    """Crea la aplicación.

    :param carpeta_datos: carpeta de los CSV (por defecto ``datos/`` o la
        variable de entorno ``HABITOS_DATOS``).
    :param hoy: función sin argumentos que devuelve la fecha de hoy; permite
        fijar el día en los tests.
    """
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("HABITOS_SECRET_KEY", "clave-de-desarrollo-cambiala"),
        CARPETA_DATOS=Path(carpeta_datos or os.environ.get("HABITOS_DATOS", "datos")),
        HOY=hoy or date.today,
    )

    app.jinja_env.filters["fecha_larga"] = formato.fecha_larga
    app.jinja_env.globals["racha_texto"] = formato.racha_texto
    app.jinja_env.globals["etiqueta_frecuencia"] = formato.etiqueta_frecuencia
    app.jinja_env.globals["porcentaje"] = formato.porcentaje
    app.jinja_env.globals["unidad"] = formato.unidad

    app.register_blueprint(bp)

    @app.errorhandler(404)
    @app.errorhandler(HabitoNoEncontrado)
    def no_encontrado(_error):
        return render_template("error.html", titulo="No encontrado",
                               mensaje="Esa página o ese hábito no existe."), 404

    @app.errorhandler(ErrorAlmacen)
    def error_almacen(error):
        return render_template("error.html", titulo="Problema con los datos",
                               mensaje=str(error)), 500

    return app
