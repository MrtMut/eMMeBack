from datetime import timedelta
from flask import redirect, send_file, url_for
from flask_cors import cross_origin
from controllers.controller_auth import *
from app import app, login_manager
from flask_login import login_required


@app.route('/test')
def test():
    return 'Test'

@app.route('/fonts/roboto/v30/KFOlCnqEu92Fr1MmEU9fBBc4.woff2')
def serve_font():
    return send_file('path/to/font.woff2')


@app.before_request
def before_request():
    session.permanent = True  # Esto asegura que la sesión tenga el tiempo de vida configurado
    app.permanent_session_lifetime = timedelta(minutes=30)
    if current_user.is_authenticated:
        session.modified = True  # Esto renueva la sesión con cada solicitud


@app.errorhandler(401)
def session_expired(e):
    return jsonify({'message': 'Session expired', 'redirect': './login.html'}), 401


#### Project Routes #################################################
@app.route('/projects', methods=['GET'])
@login_manager.user_loader
def gets():
    return get_projects()


@app.route('/projects/<id>', methods=['GET'])
def get(id):
    return get_project(id)


@app.route('/projects', methods=['POST'])
def create():
    return create_project()


@app.route('/projects/<id>', methods=['PUT', 'GET', 'OPTIONS'])
@cross_origin(origins=["http://127.0.0.1:5500"], supports_credentials=True)
def update(id):
    return update_project(id)


@app.route('/projects/<id>', methods=['DELETE'])
def delete(id):
    return delete_project(id)


#### User Routes #################################################3

@app.route('/register', methods=['POST'])
def register():
    return register_user()


@app.route('/login', methods=['GET', 'POST'])
@cross_origin(origin='http://localhost:63343', supports_credentials=True)
def login():
    return login_user_controller()


@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    return check_login_controller()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return logout_user_controller()


@app.route('/home', methods=['GET'])
def home_route():
    return home_user_controller()
