from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint("auth", __name__)

USERS = {
    "admin": "admin",
    "cantero": "cantero",
    "rodo": "rodo"
}

@auth_bp.route("/alert-login", methods=["GET", "POST"])
def alert_login():

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()

        if username in USERS and USERS[username] == password:
            session["alert_user"] = username
            return redirect(url_for("views.alertas_calidad"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


@auth_bp.route("/alert-logout")
def alert_logout():
    session.pop("alert_user", None)
    return redirect(url_for("views.index"))
