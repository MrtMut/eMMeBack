from flask import Flask 
from flask_cors import CORS    
from models.products import db, ma, Products
from views.routes.routes import productos_bp
import os
from dotenv import load_dotenv

app = Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend
load_dotenv()
password = os.getenv("DB_PASSWORD")

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://root:{password}@localhost/emmedb'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db.init_app(app)
ma.init_app(app)  #crea el objeto ma de de la clase Marshmallow

app.register_blueprint(productos_bp)




with app.app_context():
    db.create_all()  # aqui crea todas las tablas si es que no estan creadas
#  ************************************************************


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)   # ejecuta el servidor Flask en el puerto 5000