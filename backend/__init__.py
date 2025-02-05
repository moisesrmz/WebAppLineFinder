from flask import Flask
from backend.routes.views import init_routes  # Asegurar import correcto
import backend.config as config

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.config.from_object(config)

init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)


         