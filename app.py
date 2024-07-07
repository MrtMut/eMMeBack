import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:63343"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta donde se guardan los archivos subidos
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:123123123@localhost/emmedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Ajusta la duración de la sesión
app.config['SESSION_TYPE'] = 'filesystem'  # Opcional: para almacenar las sesiones en el sistema de archivos
app.config['SESSION_COOKIE_SECURE'] = True  # Opcional: para usar HTTPS en la sesión


db = SQLAlchemy(app)  #crea el objeto db de la clase SQLAlchemy
ma = Marshmallow(app)  #crea el objeto ma de la clase Marshmallow
migrate = Migrate(app, db)

from routes.route import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# programa principal *******************************
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # ejecuta el servidor Flask en el puerto 5000
