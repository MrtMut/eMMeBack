from flask import Blueprint
from models.tables import ma
from controllers.auth import register_user, login_user
from controllers.projectCRUD import create_Project, delete_Project, get_Project, get_Projects, update_project

projects_bp = Blueprint('projects', __name__)
users_bp = Blueprint('users', __name__)


@projects_bp.route('/projects',methods=['GET'])
def gets():
    return get_Projects()


@projects_bp.route('/projects/<id>',methods=['GET'])
def get():
    return get_Project(id)


@projects_bp.route('/projects', methods=['POST']) 
def create():
    return create_Project()


@projects_bp.route('/projects/<id>' ,methods=['PUT'])
def update():
    return update_project()


@projects_bp.route('/projects/<id>',methods=['DELETE'])
def delete():
    return delete_Project()


# ========session=============

class UsersSchema(ma.Schema):
    class Meta:
        fields=('id','name','email','image','admin', 'user_name' , 'password')

user_schema=UsersSchema()  


@users_bp.route('/login', methods=['POST'])
def login():
    return login_user()



@users_bp.route('/register', methods=['POST'])
def register():
    return register_user()