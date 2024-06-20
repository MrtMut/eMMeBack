
from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.tablas import db, Users

def register_user():
    name = request.json.get('name')
    email = request.json.get('email')
    image = request.json.get('image')
    admin = request.json.get('admin')
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    
    hashed_password = generate_password_hash(password, method='pbkdf2', salt_length = 16)
    
    new_user = Users(
        name = name,
        email = email,
        image = image,
        admin = admin,
        user_name = user_name,
        password = hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

def login_user():
    email = request.json.get('email')
    password = request.json.get('password')
    
    user = Users.query.filter_by(email = email).first()
    
    if user and check_password_hash(user.password, password):
        session['usuario'] = user.email
        session['logged_in'] = True
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    
    return jsonify({'message': 'Credenciales incorrectas'}), 401