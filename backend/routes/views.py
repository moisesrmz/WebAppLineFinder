from flask import Blueprint, render_template, request, send_file, session, redirect, url_for
from backend.services.excel_handler import buscar_numero_parte, buscar_modulo
import backend.config as config
import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, send_file, session, redirect, url_for, jsonify
from backend.services.excel_handler import buscar_numero_parte, buscar_modulo, leer_alertas, guardar_alertas

views_bp = Blueprint("views", __name__)

def init_routes(app):
    app.register_blueprint(views_bp)

@views_bp.route("/", methods=["GET", "POST"], endpoint="index")
def index():

    mensaje = ""
    filas_resaltadas = []

    if request.method == "POST":
        entrada = request.form["numero_parte"].strip()

        if entrada.isdigit() and len(entrada) == 10:
            mensaje, filas_resaltadas = buscar_numero_parte([entrada])
        else:
            mensaje, filas_resaltadas = buscar_modulo(entrada)

    ultima_actualizacion = "Archivo no encontrado"
    if os.path.exists(config.DATA_FILE):
        timestamp_modificacion = os.path.getmtime(config.DATA_FILE)
        ultima_actualizacion = (
            datetime.fromtimestamp(timestamp_modificacion) - timedelta(hours=6)
        ).strftime('%Y-%m-%d %H:%M:%S')

    return render_template(
        "index.html",
        mensaje=mensaje,
        filas_resaltadas=filas_resaltadas,
        ultima_actualizacion=ultima_actualizacion
    )


@views_bp.route("/descargar-excel")
def descargar_excel():
    ruta_archivo = os.path.join(os.getcwd(), "backend/data/AutomatedLines.xlsx")
    return send_file(ruta_archivo, as_attachment=True)


@views_bp.route("/alertas-calidad")
def alertas_calidad():

    # 🔒 SOLO proteger esta sección
    if "alert_user" not in session:
        return redirect(url_for("auth.alert_login"))

    return render_template(
        "alertas_calidad.html",
        user=session.get("alert_user")
    )


# ============================================================
# 🚨 API ALERTAS DE CALIDAD
# ============================================================

@views_bp.route("/api/alertas", methods=["GET"])
def api_leer_alertas():

    if "alert_user" not in session:
        return jsonify({"error": "No autorizado"}), 403

    alertas = leer_alertas()
    return jsonify(alertas)


@views_bp.route("/api/alertas", methods=["POST"])
def api_guardar_alertas():

    if "alert_user" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Formato inválido"}), 400

    try:
        guardar_alertas(data)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno al guardar"}), 500

@views_bp.route("/descargar")
def descargar_alertas():

    if "alert_user" not in session:
        return redirect(url_for("auth.alert_login"))

    from backend.services.excel_handler import ALERTAS_FILE

    if not os.path.exists(ALERTAS_FILE):
        return "No existe archivo de alertas aún."

    return send_file(
        ALERTAS_FILE,
        as_attachment=True,
        download_name="AlertasCalidad.xlsx"
    )
