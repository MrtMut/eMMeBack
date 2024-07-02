from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)  # modulo cors es para que me permita acceder desde el frontend al backend

app.config['SECRET_KEY'] = 'tu_clave_secreta_sarasa'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:123123123@localhost/emmedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma = Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

from routes.route import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Definición de la tabla Tasks
with app.app_context():
    db.create_all()  # aqui crea todas las tablas

# programa principal *******************************
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # ejecuta el servidor Flask en el puerto 5000
