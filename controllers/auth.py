from flask import jsonify, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.tables import Users, db


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
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error creating user", "error": str(e)}), 500
    else:
        return jsonify({"message": "Request must be JSON"}), 415


def login_user():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']
        print(email, password)

        user = Users.query.filter_by(email=email).first()
        print("USER", user)
        print("user.user_name", user.user_name)
        print("user.password",user.password)

        if user and check_password_hash(user.password, password):
            db.session.add(user)
            db.session.commit()

            flash('You have been registered!', 'success')
            return jsonify({'message': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'message': 'Credenciales incorrectas'}), 401
