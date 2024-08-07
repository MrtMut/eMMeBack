from flask_login import UserMixin
from app import app, db


# Definición de la tabla Users
class User(db.Model, UserMixin):  # La clase Users hereda de db.Model de SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)  # Define los campos de la tabla
    name = db.Column(db.String(30))
    email = db.Column(db.String(30), nullable=False, unique=True)
    image = db.Column(db.String(500))
    admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    def __init__(self, name, email, image, username, password):  # Constructor de la clase
        self.name = name  # No hace falta id porque lo crea sola MySQL por ser auto_incremento
        self.email = email
        self.image = image
        self.username = username
        self.password = password


# Definición de la tabla Projects
class Project(db.Model):  # La clase Projects hereda de db.Model de SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)  # Define los campos de la tabla
    name_project = db.Column(db.String(30))
    category = db.Column(db.String(30))
    description = db.Column(db.String(1000))
    image = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Llave foránea

    def __init__(self, name_project, category, description, image, user_id):  # Constructor de la clase
        self.name_project = name_project  # No hace falta id porque lo crea sola MySQL por ser auto_incremento
        self.category = category
        self.description = description
        self.image = image
        self.user_id = user_id


# Definición de la tabla Tasks
with app.app_context():
    db.create_all()  # aquí crea todas las tablas
