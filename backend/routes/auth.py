from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint("auth", __name__)

USERS = {
    "admin": "admin",
    "auditorqa": "MQA2026",
    "rodo": "rodo"
}

@auth_bp.route("/alert-login", methods=["GET", "POST"])
def alert_login():

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()

        if username in USERS and USERS[username] == password:
            #session.permanent = True
            session["alert_user"] = username
            #flash(f"Bienvenido {username.capitalize()} 👋", "success")
            return redirect(url_for("views.alertas_calidad"))
        else:
            flash("Usuario o contraseña incorrectos ❌", "danger")

    return render_template("login.html")


@auth_bp.route("/alert-logout")
def alert_logout():
    session.pop("alert_user", None)
    return redirect(url_for("views.index"))
