from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from backend.services.excel_handler import leer_hoja, guardar_cambios_excel

editor_bp = Blueprint("editor", __name__, url_prefix="/editor")  # ✅ Prefijo /editor

@editor_bp.route("/editar_excel", methods=["GET"])
def edit_excel():
    if "user" not in session:  # ✅ Si no hay usuario en sesión, redirige al login
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for("auth.login"))
    return render_template("edit_excel.html")  # ✅ Renderiza la página correcta

@editor_bp.route("/cargar_hoja", methods=["POST"])
def cargar_hoja():
    hoja = request.json.get("hoja")
    print(f"Cargando hoja: {hoja}")  # 👀 Depuración para ver qué hoja se está cargando
    datos = leer_hoja(hoja)

    if isinstance(datos, dict) and "error" in datos:
        return jsonify({"error": f"No se pudo cargar la hoja {hoja}: {datos['error']}"})

    return jsonify(datos)

@editor_bp.route("/guardar_cambios", methods=["POST"])
def guardar_cambios():
    hoja = request.json.get("hoja")
    datos = request.json.get("datos")

    if not datos or len(datos) <= 1:  # Evita guardar si solo hay encabezados
        return jsonify({"mensaje": "⚠️ No hay datos válidos para guardar."})

    resultado = guardar_cambios_excel(hoja, datos)
    return jsonify({"mensaje": resultado})
