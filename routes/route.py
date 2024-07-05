from flask import send_file, jsonify, request, session
from controllers.controller_auth import *
from app import app
from flask_login import login_required


@app.route('/test')
def test():
    return 'Test'

@app.route('/fonts/roboto/v30/KFOlCnqEu92Fr1MmEU9fBBc4.woff2')
def serve_font():
    return send_file('path/to/font.woff2')

##################### Project Routes ##########
@app.route('/')
def index():
    return 'Hello World'


@app.route('/projects', methods=['GET'])
def gets():
    return get_projects()


@app.route('/projects/<id>', methods=['GET'])
def get(id):
    return get_project(id)


@app.route('/projects', methods=['POST'])
def create():
    return create_project()


@app.route('/projects/<id>', methods=['PUT'])
def update(id):
    return update_project(id)


@app.route('/projects/<id>', methods=['DELETE'])
def delete(id):
    return delete_project(id)

##################### User Routes ##########

@app.route('/register', methods=['POST'])
def register():
    return register_user()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            remember = data.get('remember-me', False)
            #remember = True if data['remember-me'] else False
            user = Users.query.filter_by(email=email).first()
            if not user:
                return jsonify({"message": "Usuario incorrecto o no esta registrado"}), 401
            if not check_password_hash(user.password, password):
                return jsonify({"message": "Contraseña incorrecta"}), 401
            if user and check_password_hash(user.password, password):
                login_user(user, remember=remember)
                session['username'] = user.username  # Assuming 'username' is an attribute of your User model
                print("SESSION 1:", session['username']) # ACA DA BIEN
                session.modified = True  # Asegúrate de que la sesión se guarde
                next_page = request.args.get('next')
                if next_page:
                    return jsonify({'message': 'Login exitoso', 'redirect': next_page}), 200
                return jsonify({'message': 'Login exitoso', 'loginStatus': 'success'}), 200
            else:
                return jsonify({'message': 'Login erróneo. Revise su Usuario y Contraseña', 'loginSuccess': 'false'}), 401
        else:
            return jsonify({'message': 'Request must be JSON', 'loginSuccess': 'false'}), 415

@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    print("SESSION DATA:", session) # ACA NO DA BIEN
    username = session.get('username')
    print("USERNAME:", username)

    if username:
        return jsonify({'logged_in': True, 'username': username})
    return jsonify({'logged_in': False})


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return logout_user_controller()


@app.route('/home', methods=['GET'])
def home_route():
    return home_user_controller()
