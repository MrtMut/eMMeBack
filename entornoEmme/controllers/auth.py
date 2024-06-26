
from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.tablas import db, Users

def register_user():
    if request.is_json:
        data = request.get_json()
        try:
            hashed_password = generate_password_hash(data['password'], method='pbkdf2', salt_length = 16)
            new_user = Users(
                name=data['name'],
                email=data['email'],
                image='url', 
                admin=1,
                user_name='lalala',
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error creating user", "error": str(e)}), 500
    else:
        return jsonify({"message": "Request must be JSON"}), 415

def login_user():
    email = request.json.get('email')
    password = request.json.get('password')
    
    user = Users.query.filter_by(email = email).first()
    
    if user and check_password_hash(user.password, password):
        session['usuario'] = user.email
        session['logged_in'] = True
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    
    return jsonify({'message': 'Credenciales incorrectas'}), 401