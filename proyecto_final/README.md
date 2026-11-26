# 🌱 Habit Tracker

Aplicación web para registrar hábitos diarios o semanales y medir tu constancia con rachas,
porcentajes de cumplimiento y gráficos. Está pensada **para usarse desde el móvil** (diseño
*mobile-first*, modo claro/oscuro) y también funciona en el ordenador.

Proyecto final del curso **Programación en Python – Nivel Inicial**.
Autor/a: **[TU NOMBRE]** · Repositorio: **[URL DEL REPOSITORIO]**

> 📸 *Añade aquí tus capturas* (`docs/img/hoy.png`, `docs/img/estadisticas.png`…) con
> `![Pantalla Hoy](docs/img/hoy.png)`. Mira la sección [Capturas](#capturas).

---

## Qué hace

- **Hoy:** lista de tus hábitos con un botón grande para marcarlos, barra de progreso del día y racha de cada uno.
- **Hábitos diarios o semanales:** «todos los días» o «N veces por semana» (de 1 a 6).
- **Rachas inteligentes:** en días consecutivos para los diarios y en semanas cumplidas para los semanales. No se rompen por no haber marcado *todavía* hoy.
- **Corregir el pasado:** puedes marcar o desmarcar cualquier día de las últimas 4 semanas.
- **Estadísticas:** cumplimiento de los últimos 28 días, evolución semanal, días de la semana en que más cumples y tabla resumen (análisis con pandas, gráficos con Matplotlib).
- **Mapa de calor** de 20 semanas por hábito, al estilo del calendario de contribuciones de GitHub.
- **Archivar, restaurar y eliminar** hábitos.
- **API JSON** de solo lectura para consultar los datos desde otra aplicación.
- **Tus datos son tuyos:** se guardan en dos ficheros CSV legibles, sin base de datos.

## Capturas

| Hoy | Detalle de un hábito | Estadísticas |
|-----|----------------------|--------------|
| `docs/img/hoy.png` | `docs/img/detalle.png` | `docs/img/estadisticas.png` |

Para generarlas: carga los datos de demostración (ver abajo), abre la app en el navegador, activa
la vista móvil de las herramientas de desarrollo (F12 → icono de móvil) y haz las capturas.

## Requisitos

- Python **3.10 o superior**
- Un navegador moderno

## Instalación

```bash
git clone [URL DEL REPOSITORIO]
cd [CARPETA]               # la carpeta del proyecto

python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Uso

```bash
python run.py
```

Abre <http://127.0.0.1:5000>. Los datos se guardan en la carpeta `datos/`.

**Datos de ejemplo** (5 hábitos con 90 días de historial, útil para ver las estadísticas y sacar capturas):

```bash
python -m scripts.datos_demo
```

### Abrirla desde el móvil

1. Conecta el móvil a la **misma wifi** que el ordenador.
2. Arranca la app escuchando en toda la red:
   - Linux / macOS: `HOST=0.0.0.0 python run.py`
   - Windows (PowerShell): `$env:HOST="0.0.0.0"; python run.py`
3. Averigua la IP de tu ordenador (`ipconfig` en Windows, `ip a` en Linux, `ifconfig` en macOS) y abre `http://TU_IP:5000` en el móvil.
4. En el navegador del móvil usa **«Añadir a la pantalla de inicio»** para tener un icono como el de cualquier app.

> ⚠️ La aplicación no tiene inicio de sesión. Úsala solo en redes de confianza.

### Variables de entorno

| Variable | Por defecto | Para qué sirve |
|----------|-------------|----------------|
| `HOST` | `127.0.0.1` | Dirección en la que escucha (`0.0.0.0` para acceder desde otros dispositivos) |
| `PORT` | `5000` | Puerto |
| `DEBUG` | *(vacío)* | `1` activa el modo desarrollo de Flask |
| `HABITOS_DATOS` | `datos` | Carpeta donde se guardan los CSV |
| `HABITOS_SECRET_KEY` | clave de desarrollo | Clave para los mensajes de aviso; cámbiala si publicas la app |

## Tests

```bash
pip install -r requirements-dev.txt
pytest                                   # ejecuta toda la batería
pytest --cov=habitos --cov=web           # con cobertura
ruff check .                             # estilo y errores comunes
```

La batería (más de 100 casos) cubre las rachas, el modelo, el gestor, el almacén CSV (incluidos ficheros
corruptos), el análisis con pandas, los gráficos y las rutas web.

## Estructura del proyecto

```
habit-tracker/
├── run.py                  # punto de entrada
├── habitos/                # NÚCLEO (sin Flask, sin print/input)
│   ├── excepciones.py      #   jerarquía de excepciones propia
│   ├── rachas.py           #   funciones puras de cálculo de rachas
│   ├── modelo.py           #   dataclass Habito
│   ├── gestor.py           #   GestorHabitos: colección y reglas del conjunto
│   ├── almacen.py          #   AlmacenCSV: lectura y escritura de ficheros
│   ├── analisis.py         #   análisis con pandas
│   └── graficos.py         #   gráficos con Matplotlib (PNG en base64)
├── web/                    # CAPA WEB (Flask)
│   ├── __init__.py         #   create_app()
│   ├── rutas.py            #   páginas, acciones y API
│   ├── formato.py          #   funciones de formato para las plantillas
│   ├── templates/          #   HTML (Jinja2)
│   └── static/             #   CSS e icono
├── tests/                  # pytest
├── scripts/datos_demo.py   # genera datos de ejemplo
├── docs/                   # documentación ampliada
└── datos/                  # CSV de la aplicación (no se suben a git)
```

## Documentación ampliada

- 📐 [Arquitectura y decisiones de diseño](docs/arquitectura.md): capas, diagrama de clases, reglas de las rachas, formato de los datos y API.
- 📖 [Manual de usuario](docs/manual_usuario.md)
- 🔀 [Guía de Git y entrega](docs/guia_git.md)

## API JSON (solo lectura)

| Método y ruta | Devuelve |
|---------------|----------|
| `GET /api/habitos` | Lista de hábitos con racha, total y cumplimiento |
| `GET /api/habitos/<id>` | Un hábito, con todas sus fechas |
| `GET /api/resumen` | Progreso de hoy e indicadores generales |

```bash
curl http://127.0.0.1:5000/api/resumen
```

## Conceptos del curso que se aplican

| Módulo | Dónde se ve en el proyecto |
|--------|----------------------------|
| Funciones y paquetes | Paquetes `habitos` y `web`; funciones puras en `rachas.py` |
| Colecciones | `set` de fechas, `dict` de hábitos, comprensiones, `sorted(key=...)`, `Counter` |
| POO | `@dataclass Habito` con estado siempre válido, composición `GestorHabitos` → `Habito`, métodos de consulta |
| Ficheros | `AlmacenCSV` con `with`, `encoding`, `newline=""` y escritura atómica |
| Excepciones y logging | Jerarquía propia, `raise ... from`, `logging` en el gestor, errores mostrados al usuario sin trazas |
| Tests | pytest con `parametrize`, fixtures y `tmp_path` |
| Ciencia de datos | pandas (`groupby`, `reindex`, máscaras, fechas) y Matplotlib |

## Limitaciones y mejoras futuras

- Un solo usuario y sin autenticación; sin protección CSRF (pensada para uso personal/local).
- Los datos viven en CSV: suficiente para un usuario, pero SQLite sería el siguiente paso (cambiar `AlmacenCSV` por un `AlmacenSQLite` sin tocar el resto gracias a las capas).
- Sin *service worker*: se puede añadir a la pantalla de inicio, pero no funciona sin conexión.
- Ideas: recordatorios, exportar a CSV desde la web, categorías de hábitos, objetivos con fecha límite.

## Licencia

[MIT](LICENSE)
