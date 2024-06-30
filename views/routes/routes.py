from flask import Blueprint
from models.tables import ma
from controllers.auth import register_user, login_post, profile_user
from controllers.projectCRUD import create_Project, delete_Project, get_Project, get_Projects, update_project
from flask_login import login_required

projects_bp = Blueprint('projects', __name__)
users_bp = Blueprint('users', __name__)


@projects_bp.route('/projects', methods=['GET'])
def gets():
    return get_Projects()


@projects_bp.route('/projects/<id>', methods=['GET'])
def get(id):
    return get_Project(id)


@projects_bp.route('/projects', methods=['POST'])
def create():
    return create_Project()


@projects_bp.route('/projects/<id>', methods=['PUT'])
def update(id):
    return update_project(id)


@projects_bp.route('/projects/<id>', methods=['DELETE'])
def delete(id):
    return delete_Project(id)


# ========session=============

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'image', 'admin', 'user_name', 'password')

user_schema = UsersSchema()


@users_bp.route('/login', methods=['POST'])
def login():
    return login_post()


@users_bp.route('/register', methods=['POST'])
def register():
    return register_user()


@users_bp.route('/profile')
@login_required
def profile():
    return profile_user()
