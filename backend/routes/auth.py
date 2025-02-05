from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

USER_CREDENTIALS = {
    "username": "admin",
    "password": "1234"
}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
            session["user"] = username
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("editor.edit_excel"))

        flash("❌ Usuario o contraseña incorrectos", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Sesión cerrada", "info")
    return redirect(url_for("auth.login"))
