from flask import jsonify, request, current_app
from app import db
from app.routes import user_bp
from app.models import User
from app.models import user_schema

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return user_schema.jsonify(users, many=True)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return user_schema.jsonify(user)

@user_bp.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    surname = request.json['surname']
    email = request.json['email']
    password = request.json['password']

    user = User(name, surname, email, password)
    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    user.name = request.json['name']
    user.surname = request.json['surname']
    user.email = request.json['email']
    user.password = request.json['password']

    db.session.commit()
    return user_schema.jsonify(user)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
