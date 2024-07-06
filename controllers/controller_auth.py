from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.model_tables import User, Project
from flask_login import login_user, current_user, logout_user
from app import db, ma, login_manager


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'image', 'admin', 'username', 'password')


user_schema = UserSchema()


def register_user():
    if current_user.is_authenticated:
        return jsonify({'message': 'You are already logged in!'}), 401
    else:
        if request.is_json:
            data = request.get_json()
            try:
                hashed_password = generate_password_hash(data['password'])
                new_user = User(
                    name=data['name'],
                    email=data['email'],
                    image=data['image'],
                    username=data['username'],
                    password=hashed_password
                )
                if User.query.filter_by(email=data['email']).first():
                    return jsonify({"message": "Usuario ya registrado"}), 409
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
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember-me', False)
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Usuario incorrecto o no esta registrado"}), 401
        if not check_password_hash(user.password, password):
            return jsonify({"message": "Contraseña incorrecta"}), 401
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            session['username'] = user.username  # Assuming 'username' is an attribute of your User model
            print("SESSION 1:", session['username'])  # ACA DA BIEN
            session.modified = True  # Asegúrate de que la sesión se guarde
            next_page = request.args.get('next')
            if next_page:
                return jsonify({'message': 'Login exitoso', 'redirect': next_page}), 200
            return jsonify({'message': 'Login exitoso', 'loginStatus': 'success', 'username': user.username}), 200
        else:
            return jsonify({'message': 'Login erróneo. Revise su Usuario y Contraseña', 'loginStatus': 'failed'}), 401
    else:
        return jsonify({'message': 'Request must be JSON', 'loginStatus': 'failed'}), 415


def check_login_controller():
    username = session.get('username')
    if username:
        return jsonify({'logged_in': True, 'username': username})
    return jsonify({'logged_in': False})


def logout_user_controller():
    if current_user.is_authenticated:
        logout_user()
        session.pop('username', None)
        session.pop('email', None)
        return jsonify({'message': 'Logout exitoso'}), 200
    else:
        return login_user_controller()


def home_user_controller():
    if current_user.is_authenticated:
        return jsonify({'message': f'Bienvenido: {current_user.username}'}), 200
    else:
        return jsonify({'message': 'Usuario no autenticado'})


# PROJECTS ##########

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_project', 'category', 'description', 'image', 'user_id')


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


def get_projects():
    if current_user.is_authenticated:
        username = current_user.username
        print('username', username)
        all_projects = Project.query.all()  # el método query.all() lo hereda de db.Model
        if all_projects:
            result = projects_schema.dump(all_projects)
            return jsonify({'message': 'Proyectos encontrados', 'result': result, 'username': username}), 200
        else:
            return jsonify({'message': 'Proyecto no encontrado'}), 404
    else:
        return jsonify({'message': 'Usuario no autenticado'}), 401


def get_project(id):
    project = Project.query.get(id)
    if project:
        return project_schema.jsonify(project), 200  # retorna el JSON de un producto recibido como parámetro
    else:
        return jsonify({'message': 'Proyecto no encontrado'}), 404


def delete_project(id):
    print("current_user.admin:", current_user.admin)
    if current_user.is_authenticated and current_user.admin:
        project = Project.query.get(id)
        if project:
            project_schema.dump(project)
            db.session.delete(project)
            db.session.commit()  # confirma el delete
        return project_schema.jsonify(project), 200  # me devuelve un json con el registro eliminado


def create_project():
    if current_user.is_authenticated and current_user.admin:
        name_project = request.json['name_project']
        category = request.json['category']
        description = request.json['description']
        image = request.json['image']
        user_id = current_user.id
        new_project = Project(name_project, category, description, image, user_id)
        db.session.add(new_project)
        db.session.commit()  # confirma el alta
        return project_schema.jsonify(new_project), 200
    else:
        return jsonify({'message': 'Usuario no Administrador'}), 401


def update_project(id):
    if current_user.is_authenticated and current_user.admin:
        project = Project.query.get(id)
        project.name_project = request.json['name_project']
        project.category = request.json['category']
        project.description = request.json['description']
        project.image = request.json['image']
        db.session.commit()  # confirma el cambio
        return project_schema.jsonify(project), 200  # y retorna un json con el producto
    else:
        return jsonify({'message': 'Usuario no Administrador'}), 401