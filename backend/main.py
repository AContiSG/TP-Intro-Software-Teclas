from flask import Flask, request, jsonify
from models import db

app = Flask(__name__)


@app.route("/")
def inicio():
    return "Encendido"


@app.route("/test")
def test():
    return "funciona esta ruta"


if __name__ == "__main__":
    print("Iniciando servidor")
    app.run(host="0.0.0.0", debug=True, port=5000)
    # db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    #     app.run(host="0.0.0.0", debug=True, port=5000)
    #     print("Iniciado")
