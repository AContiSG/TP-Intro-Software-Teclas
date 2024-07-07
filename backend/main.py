from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Usuario, Pelicula, UsuarioPeliculas

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://<nombre_usuario>:<contraseña>@localhost:5432/<nombre_baseDeDatos>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


@app.route('/')
def login():
    return """<html>
              <body>
                <h1>Welcome to my API</h1>
                <a href="/usuarios">Ver todos los usuarios</a>
                <a href="/peliculas">Ver todas las peliculas</a>
              </body>
              </html>
"""


@app.route('/usuarios')
def obtener_usuarios():
    try:
        usuarios = Usuario.query.all()
        usuarios_data = []
        for usuario in usuarios:
            usuario_data = {
                'id':usuario.id,
                'nombre':usuario.nombre,
                'edad':usuario.edad,
                'genero':usuario.genero
            }
            usuarios_data.append(usuario_data)
        return jsonify(usuarios_data)
    except Exception as error:
        print(error)
        return jsonify({"mensaje": "No hay usuarios."})


@app.route('/usuarios', methods=["POST"])
def nuevo_usuario():
    try:
        data = request.json
        nombre = data.get('nombre')
        edad = data.get('edad')
        genero = data.get('genero')
        nuevo_usuario = Usuario(nombre=nombre, edad=edad, genero=genero)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({'usuario':{'id': nuevo_usuario.id, 'nombre': nuevo_usuario.nombre, 'edad': nuevo_usuario.edad, 'genero':nuevo_usuario.genero}})
    except Exception as error:
        print(error)
        return jsonify({'message':'No se pudo crear el usuario'}), 500


@app.route('/usuarios/<id_usuario>')
def obtener_usuario(id_usuario):
    try:
        usuario = Usuario.query.get(id_usuario)
        usuario_data = {
        'id':usuario.id,
        'nombre':usuario.nombre,
        'edad':usuario.edad,
        'genero':usuario.genero
        }
        return jsonify(usuario_data)
    except:
        return jsonify({"mensaje": "El usuario no existe"})


@app.route('/usuarios/<id_usuario>', methods=["PUT"])
def modificar_usuario_id(id_usuario):
    id = request.json.get("id")
    nombre = request.json.get("nombre")
    edad = request.json.get("edad")
    genero = request.json.get("genero")
    usuario = {
        "id": id,
        "nombre": nombre,
        "edad": edad,
        "genero": genero
    }
    return {"success": modificar_usuario(usuario), "id": id}



@app.route('/usuarios/<id_usuario>', methods=["DELETE"])
def eliminar_usuario_id(id_usuario):
    return {"success": eliminar_usuario(id)}


@app.route('/peliculas')
def mostrar_peliculas():
    try:
        peliculas = Pelicula.query.all()
        peliculas_data = []
        for pelicula in peliculas:
            pelicula_data = {
                'id_pelicula':pelicula.id_pelicula,
                'nombre':pelicula.nombre,
                'director':pelicula.director,
                'año_estreno':pelicula.año_estreno,
                'genero':pelicula.genero,
                'imagen':pelicula.imagen
            }
            peliculas_data.append(pelicula_data)
        return jsonify(peliculas_data)
    except Exception as error:
        print(error)
        return jsonify({"mensaje": "No hay peliculas."})


@app.route('/peliculas',methods=["POST"])
def nueva_pelicula():
    try:
        data = request.json
        nombre = data.get('nombre')
        director = data.get('director')
        año_estreno = data.get('año_estreno')
        genero = data.get('genero')
        imagen = data.get('imagen')
        nueva_pelicula = Usuario(nombre=nombre, director=director, año_estreno=año_estreno, genero=genero, imagen=imagen)
        db.session.add(nueva_pelicula)
        db.session.commit()
        return jsonify({'pelicula':{'id_pelicula': nueva_pelicula.id_pelicula, 'nombre': nueva_pelicula.nombre, 'director': nueva_pelicula.director, 'año_estreno':nueva_pelicula.año_estreno, 'genero':nueva_pelicula.genero, 'imagen':nueva_pelicula.imagen}})
    except Exception as error:
        print(error)
        return jsonify({'message':'No se pudo crear la pelicula'}), 500


@app.route('/peliculas/<id_pelicula>')
def obtener_pelicula(id_pelicula):
    try:
        pelicula = Pelicula.query.get(id_pelicula)
        pelicula_data = {
        'id_pelicula':pelicula.id_pelicula,
        'nombre':pelicula.nombre,
        'director':pelicula.director,
        'año_estreno':pelicula.año_estreno,
        'imagen':pelicula.imagen
        }
        return jsonify(pelicula_data)
    except Exception as error:
        print(error)
        return jsonify({"mensaje": "La pelicula no existe"})


@app.route('/peliculas/id_pelicula', methods=["PUT"])
def modificar_pelicula():
    id_pelicula = request.json.get("id_pelicula")
    nombre = request.json.get("nombre")
    director = request.json.get("director")
    año_estreno = request.json.get("año_estreno")
    genero = request.json.get("genero")
    imagen = request.json.get("imagen")
    pelicula = {
        "id_pelicula": id_pelicula,
        "nombre": nombre,
        "director": director,
        "año_estreno": año_estreno,
        "genero": genero,
        "imagen": imagen
    }
    return {"success": modificar_usuario(pelicula), "id_pelicula": id_pelicula}


@app.route('/peliculas/<id_pelicula>', methods=["DELETE"])
def eliminar_pelicula_id(id_pelicula):
    return {"success": eliminar_pelicula(id)}



if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
