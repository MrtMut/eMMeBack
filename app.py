from flask import Flask  # session, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
from models.tables import db, ma, Users
from views.routes.routes import projects_bp, users_bp
#import os
#from dotenv import load_dotenv

app = Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app)  # modulo cors es para que me permita acceder desde el frontend al backend
#load_dotenv()
#password = os.getenv("DB_PASSWORD")
#app.secret_key = os.getenv("SESSION_PASSWORD")
PASSWORD = '123123123'
SESSION_PASSWORD = '123123123'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = 'tu_clave_secreta_sarasa'
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{PASSWORD}@localhost/emmedb'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #none

db.init_app(app)
migrate = Migrate(app, db)
ma.init_app(app)  #crea el objeto ma de de la clase Marshmallow
login_manager = LoginManager(app)
login_manager.login_view = 'views.routes.users.login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


app.register_blueprint(projects_bp)
app.register_blueprint(users_bp)

# crea las tablas de la BBDD si no existen
with app.app_context():
    db.create_all()  # aqui crea todas las tablas si es que no estan creadas

# programa principal *******************************
if __name__ == '__main__':
    app.run(debug=True, port=5005)  # ejecuta el servidor Flask en el puerto 5005
