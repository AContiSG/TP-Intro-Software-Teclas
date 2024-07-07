from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)

class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id_pelicula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    año_estreno = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(50), nullable=False)

class UsuarioPeliculas(db.Model):
    __tablename__ = 'usuario_peliculas'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    id_pelicula = db.Column(db.Integer, db.ForeignKey('peliculas.id_pelicula'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('usuario_peliculas', cascade='all, delete-orphan'))
    pelicula = db.relationship('Pelicula', backref=db.backref('usuario_peliculas', cascade='all, delete-orphan'))


