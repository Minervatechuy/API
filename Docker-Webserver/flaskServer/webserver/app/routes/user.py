from flask import jsonify, request
from app import db
from app.routes import user_bp
from app.models import Usuarios
from app.models import usuarios_schema
from sqlalchemy.sql import text
from datetime import datetime
import base64
import bcrypt
import json

@user_bp.route('/get_usuario', methods=['POST'], endpoint='get_usuario')
def get_usuario():
    # Parse the JSON data from the request
    info = request.json

    # Extract the 'usuario' from the JSON data
    usuario = info["usuario"]

    try:
        # Execute a SQLAlchemy query to retrieve user information
        user = Usuarios.query.filter_by(mail=usuario).first()

        if user:
            # Convert the 'imagen' field to base64-encoded string
            imagen_base64 = base64.b64encode(user.imagen).decode('utf-8') if user.imagen else None

            result = {
                "telefono": user.telefono,
                "nombre": user.nombre,
                "apellidos": user.apellidos,
                "imagen": imagen_base64,
            }
        else:
            result = {}

    except Exception as e:
        result = {}

    # Return the result as JSON
    return jsonify({'result': result})


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



@user_bp.route('/getUserEntities', methods=['POST'], endpoint='getUserEntities')
def get_user_entities():
    # Parse the JSON data from the request
    info = request.json

    # Extract the 'usuario' from the JSON data
    usuario = info["usuario"]

    # Create a SQL query to retrieve information about entities associated with the user
    sql_query = text("""
        SELECT e.nombre, e.telefono, e.direccion, e.type, e.descripcion, e.ID
        FROM usuarios u
        JOIN users_to_entities ue ON u.mail = ue.user_email
        JOIN entities e ON e.activo = 1 AND ue.entity_id = e.ID
        WHERE u.mail = :usuario
    """)

    # Execute the SQL query
    result = db.session.execute(sql_query, {'usuario': usuario})

    # Return the result as JSON
    return jsonify({'result': [dict(row) for row in result]})

@user_bp.route('/insert_usuario', methods=['POST'], endpoint='insert_usuario')
def insert_usuario():
        # Parse the JSON data from the request
        info = request.json

        # Extract information from the JSON data
        email = info["email"]
        password = info["password"]
        nombreCompleto = info["nombre"]
        nombre = ""
        apellidos = ""
        if nombreCompleto:
            parts = nombreCompleto.split()
            if len(parts) > 0:
                nombre = parts[0]
            if len(parts) > 1:
                apellidos = ' '.join(parts[1:])

        dir_ip = info["dir_ip"]
        ultimoAcceso = datetime.now()
        imagen = info.get("imagen")  # Get the Base64-encoded image

        # Check if the email already exists
        user = Usuarios.query.filter_by(mail=email).first()
        if user:
            return jsonify({'result': False})

        # Create a new user instance
        new_user = Usuarios(
            mail=email,
            password=password,
            telefono=None,
            nombre=nombre,
            ultimoAcceso=ultimoAcceso,
            ultimaIP=dir_ip,
            apellidos=apellidos,
            activo=True,
            imagen=imagen
        )

        # Add and commit the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'result': True})
