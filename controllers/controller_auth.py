from flask import jsonify, request, session, flash  # , url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from models.model_tables import Users, Projects
from flask_login import login_user, current_user, logout_user, login_required
from app import db, ma

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'image', 'admin', 'user_name', 'password')

user_schema = UsersSchema()


def register_user():
    if request.is_json:
        data = request.get_json()
        try:
            hashed_password = generate_password_hash(data['password'])
            new_user = Users(
                name=data['name'],
                email=data['email'],
                image=data['image'],
                user_name=data['user_name'],
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "Usuario creado exitosamente"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error creando usuario", "error": str(e)}), 500
    else:
        return jsonify({"message": "Request must be JSON"}), 415


def login_user_controller():
    if request.is_json:
        data = request.get_json()
        email = data['email']
        password = data['password']
        remember = True if data['remember-me'] else False
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return jsonify({'message': 'Login exitoso', 'redirect': next_page}), 200
            return jsonify({'message': 'Login exitoso'}), 200
        else:
            return (jsonify({'message': 'Login erróneo. Revise su Usuario y Contraseña',
                             'loginSuccess': 'false'}),
                    401)
    else:
        return jsonify({'message': 'Request must be JSON', 'loginSuccess': 'false'}), 415

def logout_user_controller():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'Logout exitoso'}), 200
    else:
        return login_user_controller()
        #return jsonify({'message': 'page'}), 200


def home_user_controller():
    if current_user.is_authenticated:
        return jsonify({'message': f'Bienvenido: {current_user.user_name}'}), 200
    else:
        return jsonify({'message': 'Usuario no autenticado'})




############# PROJECTS ##########

class ProjectsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_project', 'category', 'description', 'image', 'user_id')


project_schema = ProjectsSchema()
projects_schema = ProjectsSchema(many=True)


def get_projects():
    all_projects = Projects.query.all()  # el metodo query.all() lo hereda de db.Model
    print(all_projects)
    if all_projects:
        result = projects_schema.dump(all_projects)
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Proyecto no encontrado'}), 404


def get_project(id):
    project = Projects.query.get(id)

    if project:
        return project_schema.jsonify(project), 200  # retorna el JSON de un producto recibido como parametro
    else:
        return jsonify({'message': 'Proyecto no encontrado'}), 404


def delete_project(id):
    project = Projects.query.get(id)
    if project:
        project_data = project_schema.dump(project)
        db.session.delete(project)
        db.session.commit()  # confirma el delete
    return project_schema.jsonify(project), 200  # me devuelve un json con el registro eliminado


def create_project():
    print(request.json)  # request.json contiene el json que envio el cliente
    name_project = request.json['name_project']
    category = request.json['category']
    description = request.json['description']
    image = request.json['image']
    user_id = 1

    new_project = Projects(name_project, category, description, image, user_id)
    db.session.add(new_project)
    db.session.commit()  # confirma el alta
    return project_schema.jsonify(new_project), 200


def update_project(id):
    project = Projects.query.get(id)
    project.name_project = request.json['name_project']
    project.category = request.json['category']
    project.description = request.json['description']
    project.image = request.json['image']
    db.session.commit()  # confirma el cambio
    return project_schema.jsonify(project), 200  # y retorna un json con el producto
