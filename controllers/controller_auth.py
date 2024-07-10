from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.model_tables import User, Project
from flask_login import login_user, current_user, logout_user
from app import db, ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'image', 'admin', 'username', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)



def register_user():
    if current_user.is_authenticated:
        return jsonify({'message': 'Ya estas autenticado!'}), 401
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
            return jsonify({"message": "La solicitud debe ser JSON"}), 415


def login_user_controller():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if next_page:
            return jsonify({'message': 'Login exitoso', 'redirect': next_page}), 200
        return jsonify({'message': 'Ya estas autenticado!', 'loginStatus': 'success', 'username': current_user.username}), 200

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
        return jsonify({"message": "Usuario incorrecto o no esta registrado"}), 401


def check_login_controller():
    if current_user.is_authenticated:
        username = session.get('username')
        if username:
            return jsonify({'logged_in': True, 'username': username}), 200
        return jsonify({'logged_in': False}), 401
    else:
        return jsonify({'logged_in': False}), 401


def logout_user_controller():   
    if current_user.is_authenticated:
        logout_user()
        session.pop('username', None)
        session.pop('email', None)
        return jsonify({'logoutStatus': 'success'}), 200
    else:
        return jsonify({"message": "Usuario incorrecto o no esta registrado"}), 401

def get_user_controller():
    all_users = User.query.all()
    if all_users:
        print("all_users", all_users)
        result = users_schema.dump(all_users)
        return jsonify({'message': 'Usuarios encontrados', 'users': result}), 200
    else:
        return jsonify({'message': 'Usuario no Administrador'}), 401
    


    

def user_update_controller(id):    
    if current_user.is_authenticated and current_user.admin:
        user = User.query.get(id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        data = request.json    
        print("DATAAAA", data.get('is_admin'))   
        print("USERRR", user.admin)
        if data.get('is_admin') == 'true':
            user.admin = True
            db.session.commit()
        elif data.get('is_admin') == 'false':
            user.admin = False
            db.session.commit()
        else:
            return jsonify({"message": "No se ha cambiado el estado del usuario"}), 200
        
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200          
    else:
        return jsonify({'message': 'Usuario no Administrador'}), 401



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
    #username = current_user.username
    #print('username', username)
    all_projects = Project.query.all()  # el método query.all() lo hereda de db.Model
    if all_projects:
        result = projects_schema.dump(all_projects)
        return jsonify({'message': 'Proyectos encontrados', 'result': result}), 200
    else:
        return jsonify({'message': 'Proyecto no encontrado'}), 404



def get_project(id):
    project = Project.query.get(id)
    if project:
        return project_schema.jsonify(project), 200  # retorna el JSON de un producto recibido como parámetro
    else:
        return jsonify({'message': 'Proyecto no encontrado'}), 404


def delete_project(id):
    if current_user.is_anonymous:
        return jsonify({'message': 'Usuario no autenticado'}), 401
    if current_user.is_authenticated and current_user.admin:
        project = Project.query.get(id)
        if project:
            project_schema.dump(project)
            db.session.delete(project)
            db.session.commit()  # confirma el delete
        return project_schema.jsonify(project), 200  # me devuelve un json con el registro eliminado
    else:
        return jsonify({'message': 'Usuario no Administrador'}), 401

def create_project():
    if current_user.is_anonymous:
        return jsonify({'message': 'Usuario no autenticado'}), 401
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
    if current_user.is_anonymous:
        return jsonify({'message': 'Usuario no autenticado'}), 401
    if current_user.is_authenticated and current_user.admin:
        project = Project.query.get(id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        data = request.json
        print(data)
        required_keys = ['name_project', 'category', 'description', 'client', 'image']
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"'{key}' is required"}), 400
        print("current_user.admin:", current_user.admin)
        try:
            project.name_project = data.get('name_project')
            project.category = data.get('category')
            project.description = data.get('description')
            project.user_id = data.get('client')
            project.image = data.get('image')
            db.session.commit()  # confirma el cambio
            return jsonify({"message": "Project updated successfully"}), 200
            # return ({'message': 'Proyecto actualizado', 'project': project_schema.jsonify(project)}),
            # 200  # me devuelve un json con el registro actualizado
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
            # project_schema.jsonify(project), 200)  # y retorna un json con el producto
    else:
        return jsonify({'message': 'Usuario no Administrador'}), 401
