from flask import Flask, session
from backend.routes.views import init_routes
from backend.routes.editor import editor_bp
from backend.routes.auth import auth_bp  # ✅ Importamos autenticación
import backend.config as config

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.config.from_object(config)
app.secret_key = "supersecretkey"  # ✅ Clave para manejar sesiones

# ✅ Registrar Blueprints
init_routes(app)
app.register_blueprint(editor_bp)
app.register_blueprint(auth_bp)  # ✅ Registrar autenticación

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  
    app.run(host="0.0.0.0", port=port, debug=True)  

