from flask import Flask, session
from flask_cors import CORS
from models.tables import db, ma
from views.routes.routes import projects_bp, users_bp
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

app = Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app)  #modulo cors es para que me permita acceder desde el frontend al backend
load_dotenv()
password = os.getenv("DB_PASSWORD")
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{password}@localhost/emmedb'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #none
db.init_app(app)
ma.init_app(app)  #crea el objeto ma de de la clase Marshmallow
app.secret_key = os.getenv("SESSION_PASSWORD")

# registrar los blueprints
app.register_blueprint(projects_bp)
app.register_blueprint(users_bp)

# crea las tablas de la BBDD si no existen
with app.app_context():
    db.create_all()  # aqui crea todas las tablas si es que no estan creadas


# programa principal *******************************
if __name__ == '__main__':
    app.run(debug=True, port=5005)  # ejecuta el servidor Flask en el puerto 5005