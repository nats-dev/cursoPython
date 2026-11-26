"""Punto de entrada: ``python run.py``.

Variables de entorno opcionales:
  HOST (127.0.0.1 por defecto; usa 0.0.0.0 para abrirla desde el móvil),
  PORT (5000), DEBUG (1 para modo desarrollo),
  HABITOS_DATOS (carpeta de los CSV), HABITOS_SECRET_KEY.
"""

import logging
import os

from web import create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("DEBUG") == "1",
    )
