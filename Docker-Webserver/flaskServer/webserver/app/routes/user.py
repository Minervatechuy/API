from flask import jsonify, request, current_app
from app import db
from app.routes import user_bp
from app.models import Usuarios
from app.models import usuarios_schema
from sqlalchemy.sql import text
import bcrypt

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = Usuarios.query.all()
    return usuarios_schema.jsonify(users, many=True)

@user_bp.route('/get_usuario', methods=['POST'], endpoint='get_usuario')
def get_usuario():
    # Parse the JSON data from the request
    info = request.json

    # Extract the 'usuario' field from the JSON data
    usuario = info["usuario"]

    # Define the input arguments for the stored procedure
    args = [usuario]

    try:
        # Execute the stored procedure using SQLAlchemy
        result = db.session.execute("CALL get_usuario(:email)", {"email": usuario}).fetchall()
        result = [dict(row) for row in result]

    except Exception as e:
        result = []

    # Return the result to the view
    return jsonify({'result': result})

@user_bp.route('/users', methods=['POST'])
def create_user():
    name = request.json['nombre']
    apellidos = request.json['apellidos']
    email = request.json['mail']
    password = request.json['pass']
    telefono = request.json['telefono']
    ultimoAcceso = request.json['ultimoAcceso']
    ultimaIP = request.json['ultimaIP']
    activo = request.json['activo']
    imagen = request.json['imagen']

    user = Usuarios(
        mail=email,
        password=password,
        telefono=telefono,
        nombre=name,
        ultimoAcceso=ultimoAcceso,
        ultimaIP=ultimaIP,
        apellidos=apellidos,
        activo=activo,
        imagen=imagen
    )

    db.session.add(user)
    db.session.commit()

    return usuarios_schema.jsonify(user), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Usuarios.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    user.mail = request.json.get('mail', user.mail)
    user.password = request.json.get('pass', user.password)
    user.telefono = request.json.get('telefono', user.telefono)
    user.nombre = request.json.get('nombre', user.nombre)
    user.ultimoAcceso = request.json.get('ultimoAcceso', user.ultimoAcceso)
    user.ultimaIP = request.json.get('ultimaIP', user.ultimaIP)
    user.apellidos = request.json.get('apellidos', user.apellidos)
    user.activo = request.json.get('activo', user.activo)
    user.imagen = request.json.get('imagen', user.imagen)

    db.session.commit()
    return usuarios_schema.jsonify(user)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Usuarios.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return usuarios_schema.jsonify(user)


@user_bp.route('/exist_usuario', methods=['POST'], endpoint='exist_usuario')
def exist_usuario():
    # Parse the JSON data from the request
    info = request.json

    # Extract the 'usuario' and 'pwd' fields from the JSON data
    usuario = info['usuario']
    pwd = info['pwd']

    # Retrieve the user based on the provided email
    user = Usuarios.query.filter_by(mail=usuario).first()

    if user is not None and bcrypt.checkpw(pwd.encode('utf-8'), user.password.encode('utf-8')):
        # User exists and the password is correct
        return jsonify({'result': True})
    else:
        # User doesn't exist or the password is incorrect
        return jsonify({'result': False})

@user_bp.route('/getCalcsInfo', methods=['POST'], endpoint='getCalcsInfo')
def get_calculators_info():
    # Parse the JSON data from the request
    info = request.json

    # Extract the 'user' from the JSON data for the database query
    user = info["user"]

    # Create a SQL query to retrieve information about calculators
    sql_query = text("""
        SELECT c.name, c.url, c.ip, c.formula, c.entity_ID, c.name AS calculator_name, c.activo, c.token
        FROM usuarios u
        JOIN users_to_calculators utc ON u.mail = utc.user_email
        JOIN calculators c ON c.activo = 1 AND utc.calculator_token = c.token
        WHERE u.mail = :user
    """)

    # Execute the SQL query
    result = db.session.execute(sql_query, {'user': user})

    # Return the result as JSON
    return jsonify({'result': [dict(row) for row in result]})     
