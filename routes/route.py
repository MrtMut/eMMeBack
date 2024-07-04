from controllers.controller_auth import *
from app import app
from flask_login import login_required


@app.route('/test')
def test():
    return 'Test'



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
        return login_user_controller()


@app.route('/logout', methods=['POST'])
def logout():
    return logout_user_controller()


@app.route('/home', methods=['GET'])
def home_route():
    return home_user_controller()
