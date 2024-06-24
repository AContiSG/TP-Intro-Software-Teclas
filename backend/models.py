import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Test(db.Model):
    __tablename__ = "Tablatest"
    id = db.Column(db.Integer, primary_key=True)
    testInt = db.Column(db.Integer)
