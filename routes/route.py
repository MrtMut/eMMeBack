from controllers.controller_auth import *
from app import app


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





@app.route('/login', methods=['POST'])
def login():
    return login_post()


@app.route('/register', methods=['POST'])
def register():
    return register_user()


@app.route('/profile')
#@login_required
def profile():
    return 'Profile Page'
    #return profile_user()
