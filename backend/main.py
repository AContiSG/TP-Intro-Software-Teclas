from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS
from models import db, Usuario, Pelicula, Reseña

load_dotenv()

app = Flask(__name__)
CORS(app)
port = 5000
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def login():
    return """<html>
              <body>
                <h1>Welcome to my API</h1>
                <a href="/usuarios">Ver todos los usuarios</a>
                <a href="/peliculas">Ver todas las peliculas</a>
                <a href="/reseñas">Ver todas las reseñas</a>
              </body>
              </html>
"""


"""

------------------------------------- Usuarios -------------------------------------

"""


@app.route("/usuarios")
def obtener_usuarios():
    try:
        usuarios = Usuario.query.all()
        usuarios_data = []
        for usuario in usuarios:
            usuario_data = {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "edad": usuario.edad,
                "genero": usuario.genero,
            }
            usuarios_data.append(usuario_data)
        return jsonify(usuarios_data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/usuarios/<id_usuario>")
def obtener_usuario_id(id_usuario):
    try:
        usuario = db.session.query(Usuario).filter_by(id=id_usuario).one_or_none()
        if not usuario:
            return jsonify({"message": "No se encontró el usuario"}), 404

        usuario_data = {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad,
            "genero": usuario.genero,
        }
        return jsonify(usuario_data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/usuarios/nombre/<nombre_usuario>")
def obtener_usuario_nombre(nombre_usuario):
    try:
        usuario = (
            db.session.query(Usuario).filter_by(nombre=nombre_usuario).one_or_none()
        )
        if not usuario:
            return jsonify({"message": "No se encontró el usuario"}), 404

        usuario_data = {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad,
            "genero": usuario.genero,
        }
        return jsonify(usuario_data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/usuarios", methods=["POST"])
def nuevo_usuario():
    try:
        data = request.json
        nombre = data.get("nombre")
        edad = data.get("edad")
        genero = data.get("genero")
        nuevo_usuario = Usuario(nombre=nombre, edad=edad, genero=genero)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return (
            jsonify(
                {
                    "id": nuevo_usuario.id,
                    "nombre": nuevo_usuario.nombre,
                    "edad": nuevo_usuario.edad,
                    "genero": nuevo_usuario.genero,
                }
            ),
            201,
        )
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/usuarios/<id_usuario>", methods=["PUT"])
def modificar_usuario_id(id_usuario):
    try:
        usuario = db.session.query(Usuario).filter_by(id=id_usuario).one_or_none()
        # usuario = Usuario.query.get(id_usuario)
        data = request.json

        # Los if son porque si la request no tiene todos los campos completos, los que no están los va a modificar poniendoles null
        if "nombre" in data:
            usuario.nombre = data.get("nombre")
        if "edad" in data:
            usuario.edad = data.get("edad")
        if "genero" in data:
            usuario.genero = data.get("genero")
        db.session.commit()
        return jsonify(data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/usuarios/<id_usuario>", methods=["DELETE"])
def eliminar_usuario_id(id_usuario):
    try:
        usuario = db.session.query(Usuario).filter_by(id=id_usuario).one_or_none()
        if not usuario:
            return jsonify({"message": "No se encontró el usuario"}), 404

        db.session.delete(usuario)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "edad": usuario.edad,
                    "genero": usuario.genero,
                }
            ),
            200,
        )

    except Exception as error:
        print(error)
        return jsonify({"message": error}), 500


"""

------------------------------------- Peliculas -------------------------------------

"""


@app.route("/peliculas")
def obtener_peliculas():
    try:
        peliculas = Pelicula.query.all()
        peliculas_data = []
        for pelicula in peliculas:
            pelicula_data = {
                "id": pelicula.id,
                "nombre": pelicula.nombre,
                "director": pelicula.director,
                "año_estreno": pelicula.año_estreno,
                "genero": pelicula.genero,
                "imagen": pelicula.imagen,
            }
            peliculas_data.append(pelicula_data)
        return jsonify(peliculas_data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/peliculas/<id_pelicula>")
def obtener_pelicula_id(id_pelicula):
    try:
        pelicula = db.session.query(Pelicula).filter_by(id=id_pelicula).one_or_none()
        if not pelicula:
            return jsonify({"message": "No se encontró la pelicula"}), 404

        pelicula_data = {
            "id": pelicula.id,
            "nombre": pelicula.nombre,
            "director": pelicula.director,
            "año_estreno": pelicula.año_estreno,
            "genero": pelicula.genero,
            "imagen": pelicula.imagen,
        }
        return jsonify(pelicula_data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/peliculas", methods=["POST"])
def nueva_pelicula():
    try:
        data = request.json
        nombre = data.get("nombre")
        director = data.get("director")
        año_estreno = data.get("año_estreno")
        genero = data.get("genero")
        imagen = data.get("imagen")
        nueva_pelicula = Pelicula(
            nombre=nombre,
            director=director,
            año_estreno=año_estreno,
            genero=genero,
            imagen=imagen,
        )
        db.session.add(nueva_pelicula)
        db.session.commit()
        return (
            jsonify(
                {
                    "id": nueva_pelicula.id,
                    "nombre": nueva_pelicula.nombre,
                    "director": nueva_pelicula.director,
                    "año_estreno": nueva_pelicula.año_estreno,
                    "genero": nueva_pelicula.genero,
                    "imagen": nueva_pelicula.imagen,
                }
            ),
            201,
        )
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/peliculas/<id_pelicula>", methods=["PUT"])
def modificar_pelicula_id(id_pelicula):
    try:
        pelicula = db.session.query(Pelicula).filter_by(id=id_pelicula).one_or_none()
        data = request.json

        # Los if son porque si la request no tiene todos los campos completos, los que no están los va a modificar poniendoles null
        if "pelicula" in data:
            pelicula.nombre = data.get("nombre")
        if "director" in data:
            pelicula.director = data.get("director")
        if "genero" in data:
            pelicula.genero = data.get("genero")
        if "año_estreno" in data:
            pelicula.año_estreno = data.get("año_estreno")
        if "imagen" in data:
            pelicula.imagen = data.get("imagen")

        db.session.commit()
        return jsonify(data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/peliculas/<id_pelicula>", methods=["DELETE"])
def eliminar_pelicula_id(id_pelicula):
    try:
        pelicula = db.session.query(Pelicula).filter_by(id=id_pelicula).one_or_none()
        if not pelicula:
            return jsonify({"message": "No se encontró la pelicula"}), 404

        db.session.delete(pelicula)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": pelicula.id,
                    "nombre": pelicula.nombre,
                    "director": pelicula.director,
                    "año_estreno": pelicula.año_estreno,
                    "genero": pelicula.genero,
                    "imagen": pelicula.imagen,
                }
            ),
            200,
        )
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


"""

------------------------------------- Reseñas -------------------------------------

"""


@app.route("/reseñas")
def obtener_reseñas():
    try:
        reseñas = Reseña.query.all()
        reseñas_data = []
        for reseña in reseñas:
            reseña_data = {
                "id": reseña.id,
                "id_usuario": reseña.id_usuario,
                "id_pelicula": reseña.id_pelicula,
                "puntaje": reseña.puntaje,
                "reseña_corta": reseña.reseña_corta,
            }
            reseñas_data.append(reseña_data)
        return jsonify(reseñas_data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/reseñas/<id_resena>")
def obtener_reseña_id(id_resena):
    try:
        reseña = db.session.query(Reseña).filter_by(id=id_resena).one_or_none()
        if not reseña:
            return jsonify({"message": "No se encontró la reseña"}), 404

        reseña_data = {
            "id": reseña.id,
            "id_usuario": reseña.id_usuario,
            "id_pelicula": reseña.id_pelicula,
            "puntaje": reseña.puntaje,
            "reseña_corta": reseña.reseña_corta,
        }
        return jsonify(reseña_data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/reseñas", methods=["POST"])
def nueva_reseña():
    try:
        data = request.json
        id_usuario = data.get("id_usuario")
        id_pelicula = data.get("id_pelicula")
        puntaje = data.get("puntaje")
        reseña_corta = data.get("reseña_corta")
        nueva_reseña = Reseña(
            id_usuario=id_usuario,
            id_pelicula=id_pelicula,
            puntaje=puntaje,
            reseña_corta=reseña_corta,
        )

        db.session.add(nueva_reseña)
        db.session.commit()
        return (
            jsonify(
                {
                    "id": nueva_reseña.id,
                    "id_usuario": nueva_reseña.id_usuario,
                    "id_pelicula": nueva_reseña.id_pelicula,
                    "puntaje": nueva_reseña.puntaje,
                    "reseña_corta": nueva_reseña.reseña_corta,
                }
            ),
            201,
        )
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/reseñas/<id_resena>", methods=["PUT"])
def modificar_reseña_id(id_resena):
    try:
        reseña = db.session.query(Reseña).filter_by(id=id_resena).one_or_none()
        data = request.json

        # Los if son porque si la request no tiene todos los campos completos, los que no están los va a modificar poniendoles null
        if "id_usuario" in data:
            reseña.id_usuario = data.get("id_usuario")
        if "id_pelicula" in data:
            reseña.id_pelicula = data.get("id_pelicula")
        if "puntaje" in data:
            reseña.puntaje = data.get("puntaje")
        if "reseña_corta" in data:
            reseña.reseña_corta = data.get("reseña_corta")

        db.session.commit()
        return jsonify(data), 200
    except Exception as error:
        print(error)
        return jsonify({"mensaje": error}), 500


@app.route("/reseñas/<id_resena>", methods=["DELETE"])
def eliminar_reseña_id(id_resena):
    try:
        reseña = db.session.query(Reseña).filter_by(id=id_resena).one_or_none()
        if not reseña:
            return jsonify({"message": "No se encontró la reseña"}), 404

        db.session.delete(reseña)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": reseña.id,
                    "id_usuario": reseña.id_usuario,
                    "id_pelicula": reseña.id_pelicula,
                    "puntaje": reseña.puntaje,
                    "reseña_corta": reseña.reseña_corta,
                }
            ),
            200,
        )

    except Exception as error:
        print(error)
        return jsonify({"message": error}), 500


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=port)
