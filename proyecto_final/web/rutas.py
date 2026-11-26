"""Rutas de la aplicación.

Cada petición carga los datos del CSV, aplica el cambio en el gestor y, si
hubo cambio, guarda. Así no hay estado global y la web es fácil de probar.
"""

from datetime import date, timedelta

from flask import (Blueprint, current_app, flash, jsonify, redirect,
                   render_template, request, url_for)

from habitos import analisis, graficos
from habitos.almacen import AlmacenCSV
from habitos.excepciones import ErrorHabitos, FechaInvalida, HabitoNoEncontrado
from habitos.gestor import GestorHabitos
from habitos.modelo import MAX_DESCRIPCION, MAX_NOMBRE, Habito
from habitos.rachas import lunes_de

bp = Blueprint("rutas", __name__)

SEMANAS_CALENDARIO = 4   # semanas del calendario interactivo del detalle
SEMANAS_MAPA_CALOR = 20  # semanas del mapa de calor


# ---- utilidades ------------------------------------------------------------
def _hoy() -> date:
    return current_app.config["HOY"]()


def _almacen() -> AlmacenCSV:
    return AlmacenCSV(current_app.config["CARPETA_DATOS"])


def _cargar() -> GestorHabitos:
    return _almacen().cargar()


def _leer_fecha(texto: str | None) -> date:
    """Convierte el campo ``fecha`` del formulario; vacío significa hoy."""
    if not texto:
        return _hoy()
    try:
        return date.fromisoformat(texto)
    except ValueError:
        raise FechaInvalida("La fecha debe tener el formato AAAA-MM-DD.") from None


def _leer_veces(texto: str | None) -> int:
    try:
        return int(texto)
    except (TypeError, ValueError):
        return 0  # el modelo lo rechazará con un mensaje claro


def _destino(por_defecto: str) -> str:
    """Adónde volver tras un POST. Solo se aceptan rutas internas."""
    siguiente = request.form.get("next", "")
    if siguiente.startswith("/") and not siguiente.startswith("//"):
        return siguiente
    return url_for(por_defecto)


def _habito_a_dict(habito: Habito, hoy: date) -> dict:
    return {
        "id": habito.id,
        "nombre": habito.nombre,
        "descripcion": habito.descripcion,
        "veces_semana": habito.veces_semana,
        "creado": habito.creado.isoformat(),
        "archivado": habito.archivado,
        "hecho_hoy": habito.cumplido(hoy),
        "racha_actual": habito.racha_actual(hoy),
        "mejor_racha": habito.mejor_racha(),
        "unidad_racha": "dias" if habito.es_diario else "semanas",
        "total": habito.total,
        "cumplimiento_28_dias": round(habito.cumplimiento(hoy), 4),
    }


def _calendario(habito: Habito, hoy: date) -> list[list[dict]]:
    """Cuadrícula de las últimas semanas (lunes a domingo) para marcar días pasados."""
    inicio = lunes_de(hoy) - timedelta(weeks=SEMANAS_CALENDARIO - 1)
    semanas = []
    for s in range(SEMANAS_CALENDARIO):
        semana = []
        for d in range(7):
            dia = inicio + timedelta(weeks=s, days=d)
            semana.append({"fecha": dia, "hecho": habito.cumplido(dia),
                           "futuro": dia > hoy, "hoy": dia == hoy})
        semanas.append(semana)
    return semanas


# ---- páginas ---------------------------------------------------------------
@bp.get("/")
def hoy():
    gestor = _cargar()
    hoy_ = _hoy()
    hechos, total = gestor.progreso_hoy(hoy_)
    return render_template(
        "index.html", hoy=hoy_, habitos=gestor.activos(),
        hechos=hechos, total=total,
        proporcion=round(100 * hechos / total) if total else 0,
    )


@bp.get("/habitos")
def habitos():
    gestor = _cargar()
    return render_template("habitos.html", hoy=_hoy(),
                           activos=gestor.activos(), archivados=gestor.archivados())


@bp.route("/habitos/nuevo", methods=["GET", "POST"])
def nuevo():
    datos = {"nombre": "", "descripcion": "", "veces_semana": 7}
    if request.method == "POST":
        datos = {"nombre": request.form.get("nombre", ""),
                 "descripcion": request.form.get("descripcion", ""),
                 "veces_semana": _leer_veces(request.form.get("veces_semana"))}
        gestor = _cargar()
        try:
            habito = gestor.crear(datos["nombre"], _hoy(), datos["veces_semana"], datos["descripcion"])
            _almacen().guardar(gestor)
        except ErrorHabitos as e:
            flash(str(e), "error")
        else:
            flash(f"Hábito «{habito.nombre}» creado.", "ok")
            return redirect(url_for("rutas.hoy"))
    return render_template("formulario.html", titulo="Nuevo hábito", datos=datos,
                           max_nombre=MAX_NOMBRE, max_descripcion=MAX_DESCRIPCION)


@bp.route("/habitos/<int:id_habito>/editar", methods=["GET", "POST"])
def editar(id_habito: int):
    gestor = _cargar()
    habito = gestor.obtener(id_habito)
    datos = {"nombre": habito.nombre, "descripcion": habito.descripcion,
             "veces_semana": habito.veces_semana}
    if request.method == "POST":
        datos = {"nombre": request.form.get("nombre", ""),
                 "descripcion": request.form.get("descripcion", ""),
                 "veces_semana": _leer_veces(request.form.get("veces_semana"))}
        try:
            gestor.editar(id_habito, datos["nombre"], datos["veces_semana"], datos["descripcion"])
            _almacen().guardar(gestor)
        except ErrorHabitos as e:
            flash(str(e), "error")
        else:
            flash("Cambios guardados.", "ok")
            return redirect(url_for("rutas.detalle", id_habito=id_habito))
    return render_template("formulario.html", titulo="Editar hábito", datos=datos,
                           max_nombre=MAX_NOMBRE, max_descripcion=MAX_DESCRIPCION)


@bp.get("/habitos/<int:id_habito>")
def detalle(id_habito: int):
    gestor = _cargar()
    habito = gestor.obtener(id_habito)
    hoy_ = _hoy()
    df = analisis.registros_df(gestor)
    df_habito = df[df["habito_id"] == id_habito]
    mapa = graficos.mapa_calor(analisis.matriz_semanal(df_habito, hoy_, SEMANAS_MAPA_CALOR), hoy_)
    return render_template("detalle.html", habito=habito, hoy=hoy_,
                           calendario=_calendario(habito, hoy_), mapa=mapa)


@bp.get("/estadisticas")
def estadisticas():
    gestor = _cargar()
    hoy_ = _hoy()
    df = analisis.registros_df(gestor, incluir_archivados=False)
    tabla = analisis.tabla_habitos(gestor, hoy_)
    graficas = None
    if len(df):
        graficas = {
            "semanas": graficos.grafico_semanas(analisis.registros_por_semana(df, hoy_)),
            "dias": graficos.grafico_dias_semana(analisis.registros_por_dia_semana(df)),
            "cumplimiento": graficos.grafico_cumplimiento(tabla),
        }
    return render_template("estadisticas.html", ind=analisis.indicadores(gestor, hoy_),
                           tabla=tabla.to_dict("records"), graficas=graficas)


# ---- acciones (POST) ---------------------------------------------------------
@bp.post("/habitos/<int:id_habito>/alternar")
def alternar(id_habito: int):
    gestor = _cargar()
    try:
        gestor.alternar(id_habito, _leer_fecha(request.form.get("fecha")), _hoy())
        _almacen().guardar(gestor)
    except HabitoNoEncontrado:
        raise  # lo gestiona el manejador de errores 404
    except ErrorHabitos as e:
        flash(str(e), "error")
    return redirect(_destino("rutas.hoy"))


@bp.post("/habitos/<int:id_habito>/archivar")
def archivar(id_habito: int):
    gestor = _cargar()
    gestor.archivar(id_habito)
    _almacen().guardar(gestor)
    flash("Hábito archivado. Puedes restaurarlo desde «Hábitos».", "ok")
    return redirect(url_for("rutas.habitos"))


@bp.post("/habitos/<int:id_habito>/restaurar")
def restaurar(id_habito: int):
    gestor = _cargar()
    try:
        gestor.restaurar(id_habito)
        _almacen().guardar(gestor)
    except ErrorHabitos as e:
        flash(str(e), "error")
    else:
        flash("Hábito restaurado.", "ok")
    return redirect(url_for("rutas.habitos"))


@bp.post("/habitos/<int:id_habito>/eliminar")
def eliminar(id_habito: int):
    gestor = _cargar()
    gestor.eliminar(id_habito)
    _almacen().guardar(gestor)
    flash("Hábito eliminado definitivamente.", "ok")
    return redirect(url_for("rutas.habitos"))


# ---- API JSON (solo lectura) -------------------------------------------------
@bp.get("/api/habitos")
def api_habitos():
    gestor = _cargar()
    hoy_ = _hoy()
    return jsonify([_habito_a_dict(h, hoy_) for h in gestor.todos()])


@bp.get("/api/habitos/<int:id_habito>")
def api_habito(id_habito: int):
    habito = _cargar().obtener(id_habito)
    datos = _habito_a_dict(habito, _hoy())
    datos["fechas"] = [f.isoformat() for f in sorted(habito.fechas)]
    return jsonify(datos)


@bp.get("/api/resumen")
def api_resumen():
    gestor = _cargar()
    hoy_ = _hoy()
    hechos, total = gestor.progreso_hoy(hoy_)
    return jsonify({"fecha": hoy_.isoformat(), "hechos_hoy": hechos, "tocan_hoy": total,
                    **analisis.indicadores(gestor, hoy_)})


# ---- PWA ---------------------------------------------------------------------
@bp.get("/manifest.webmanifest")
def manifest():
    respuesta = jsonify({
        "name": "Habit Tracker",
        "short_name": "Hábitos",
        "description": "Registra tus hábitos y mide tu constancia.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#f6f7f9",
        "theme_color": "#16a34a",
        "icons": [{"src": url_for("static", filename="icon.svg"), "sizes": "any",
                   "type": "image/svg+xml", "purpose": "any"}],
    })
    respuesta.mimetype = "application/manifest+json"
    return respuesta
