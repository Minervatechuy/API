from flask import jsonify, request
from app import db
from app.routes import entitie_bp
from app.models import Entities, UsersToEntities, Usuarios

@entitie_bp.route('/createEntidad', methods=['POST'], endpoint='createEntidad')
def createEntidad():
    info = request.get_json()

    identificador = info["identificador"]
    nombre = info["nombre"]
    telefono = info["telefono"]
    direccion = info["direccion"]
    tipo = info["tipo"]
    descripcion = info["descripcion"]
    usuario = info["usuario"]

    # Check if entity with given ID exists
    existing_entity = Entities.query.filter_by(ID=identificador).first()
    if existing_entity:
        return jsonify({'tipo': "error", "mensaje": "No se ha creado la entidad, porque existe una entidad registrada con ese RUT o CI"})

    # Create entity
    new_entity = Entities(ID=identificador, nombre=nombre, telefono=telefono, direccion=direccion, type=tipo, activo='1', descripcion=descripcion)
    db.session.add(new_entity)

    # Create user-to-entity relationship
    user_to_entity = UsersToEntities(user_id=usuario, entity_id=identificador)
    db.session.add(user_to_entity)

    db.session.commit()

    return jsonify({'tipo': "success", "mensaje": "Entidad creada correctamente"})


@entitie_bp.route('/editEntidad', methods=['POST'], endpoint='editEntidad')
def editEntidad():
    info = request.get_json()

    identificador = info["identificador"]
    nombre = info["nombre"]
    telefono = info["telefono"]
    direccion = info["direccion"]
    tipo = info["tipo"]

    # Update entity
    entity = Entities.query.get(identificador)
    if entity:
        entity.ID = identificador
        entity.nombre = nombre
        entity.telefono = telefono
        entity.direccion = direccion
        entity.type = tipo

        db.session.commit()

        return jsonify({'result': True})
    else:
        return jsonify({'result': False, 'message': 'Entidad no encontrada'})
    
@entitie_bp.route('/getEntidad', methods=['POST'], endpoint='getEntidad')
def getEntidad():
    info = request.get_json()

    entidad_id = info["entidad_id"]

    entity = Entities.query.get(entidad_id)

    if entity:
        result = {
            'ID': entity.ID,
            'nombre': entity.nombre,
            'telefono': entity.telefono,
            'direccion': entity.direccion,
            'type': entity.type
        }
    else:
        result = None

    return jsonify({'result': result})

@entitie_bp.route('/deleteEntidad', methods=['POST'], endpoint='deleteEntidad')
def deleteEntidad():
    info = request.get_json()

    entidad_id = info["entidad_id"]

    # Delete entity and related user-to-entity relationships
    entity = Entities.query.get(entidad_id)
    if entity:
        UsersToEntities.query.filter_by(entity_id=entidad_id).delete()
        db.session.delete(entity)
        db.session.commit()

        return jsonify({'result': True})
    else:
        return jsonify({'result': False, 'message': 'Entidad no encontrada'})


@entitie_bp.route('/addUsuarioEntidad', methods=['POST'], endpoint='addUsuarioEntidad')
def addUsuarioEntidad():
    info = request.get_json()

    new_user_email = info["new_user_email"]
    entidad_id = info["entidad_id"]

    # Check if user with given email exists
    result = UsersToEntities.query.filter_by(user_email=new_user_email, entity_id=entidad_id).count()
    if result > 0:
        return jsonify({'tipo': 'info', 'mensaje':'El usuario ya esta en la entidad'})

    # Add user to entity
    new_user_to_entity = UsersToEntities(user_email=new_user_email, entity_id=entidad_id)
    db.session.add(new_user_to_entity)
    db.session.commit()

    return jsonify({'tipo': 'success', 'mensaje':'Usuario añadido a la entidad.'})


@entitie_bp.route('/getUsuariosEntidad', methods=['POST'], endpoint='getUsuariosEntidad')
def getUsuariosEntidad():
    info = request.get_json()

    entidad_id = info["entidad_id"]
    email = info["email"]

    result = Usuarios.query.join(UsersToEntities, Usuarios.mail == UsersToEntities.user_email).filter(UsersToEntities.entity_id == entidad_id, Usuarios.mail != email).with_entities(UsersToEntities.user_email, UsersToEntities.entity_id, Usuarios.nombre, Usuarios.apellidos).all()

    result_dict = [{'user_email': row[0], 'entity_id': row[1], 'nombre': row[2], 'apellidos': row[3]} for row in result]

    return jsonify({'result': result_dict})


@entitie_bp.route('/deleteUsuarioEntidad', methods=['POST'], endpoint='deleteUsuarioEntidad')
def deleteUsuarioEntidad():
    info = request.get_json()

    entidad_id = info["entidad_id"]
    email = info["email"]

    user_to_entity = UsersToEntities.query.filter_by(user_email=email,entity_id=entidad_id).first()

    if user_to_entity:
        db.session.delete(user_to_entity)
        db.session.commit()

        return jsonify({'result': True})
    else:
        return jsonify({'result': False, 'message': 'Asociación usuario-entidad no encontrada'})

