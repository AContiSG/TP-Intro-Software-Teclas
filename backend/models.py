from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    peliculas = db.relationship('UsuarioPeliculas', backref='usuario', cascade='all, delete-orphan')

class Pelicula(db.Model):
    __tablename__ = "peliculas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    año_estreno = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(200), nullable=False)
    usuarios = db.relationship('UsuarioPeliculas', backref='pelicula', cascade='all, delete-orphan')


class UsuarioPeliculas(db.Model):
    __tablename__ = "usuario_peliculas"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_pelicula = db.Column(db.Integer, db.ForeignKey("peliculas.id"), nullable=False)
    puntaje = db.Column(db.Integer)
    reseña = db.Column(db.String(200))
