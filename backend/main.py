from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from models import db

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def inicio():
    return "Encendido"


@app.route("/test")
def test():
    return "funciona esta ruta"


@app.route("/data/<section>")
def data(section):
    return section


if __name__ == "__main__":
    print("Iniciando servidor")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=5000)
    print("Iniciado")
