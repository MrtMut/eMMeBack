
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


# Definición de la tabla Users
class Users(db.Model):   # La clase Users hereda de db.Model de SQLAlchemy   
    id = db.Column(db.Integer, primary_key=True)  # Define los campos de la tabla
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(1000))
    admin = db.Column(db.Boolean, nullable=False)
    user_name = db.Column(db.String(100))
    password = db.Column(db.String(400))
    
    def __init__(self, name, email, image, admin, user_name, password):  # Constructor de la clase
        self.name = name  # No hace falta el id porque lo crea sola MySQL por ser auto_incremento
        self.email = email
        self.image = image
        self.admin = admin
        self.user_name = user_name
        self.password = password

# Definición de la tabla Projects
class Projects(db.Model):   # La clase Projects hereda de db.Model de SQLAlchemy   
    id = db.Column(db.Integer, primary_key=True)  # Define los campos de la tabla
    name_project = db.Column(db.String(100))
    category = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Llave foránea
    
    def __init__(self, name_project, category, description, image, user_id):  # Constructor de la clase
        self.name_project = name_project  # No hace falta el id porque lo crea sola MySQL por ser auto_incremento
        self.category = category
        self.description = description
        self.image = image
        self.user_id = user_id