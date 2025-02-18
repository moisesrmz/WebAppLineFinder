from flask import Blueprint, render_template, request, send_file
from backend.services.excel_handler import buscar_numero_parte
import backend.config as config
import os
from datetime import datetime, timedelta

views_bp = Blueprint("views", __name__)  # ✅ Nombre del Blueprint "views"

def init_routes(app):
    app.register_blueprint(views_bp)

@views_bp.route("/", methods=["GET", "POST"], endpoint="index")  # ✅ Endpoint correcto
def index():
    mensaje = ""
    filas_resaltadas = []

    if request.method == "POST":
        numeros_parte = request.form["numero_parte"].strip().split()
        mensaje, filas_resaltadas = buscar_numero_parte(numeros_parte)

    ultima_actualizacion = "Archivo no encontrado"
    if os.path.exists(config.DATA_FILE):
        timestamp_modificacion = os.path.getmtime(config.DATA_FILE)
        #ultima_actualizacion = datetime.fromtimestamp(timestamp_modificacion).strftime('%Y-%m-%d %H:%M:%S')
        ultima_actualizacion = (datetime.fromtimestamp(timestamp_modificacion) - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')

    return render_template("index.html", mensaje=mensaje, filas_resaltadas=filas_resaltadas, ultima_actualizacion=ultima_actualizacion)

@views_bp.route("/descargar-excel")
def descargar_excel():
    ruta_archivo = os.path.join(os.getcwd(), "backend/data/AutomatedLines.xlsx")
    return send_file(ruta_archivo, as_attachment=True)