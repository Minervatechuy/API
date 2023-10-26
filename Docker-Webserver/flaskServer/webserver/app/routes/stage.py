from flask import jsonify, request
from app import db
from app.routes import stage_bp
from app.models import Etapa, EtapaData, EtapaOpcion

@stage_bp.route('/getStagesGeneralInfo', methods=['POST'], endpoint='getStagesGeneralInfo')
def get_stages_general_info():
    # Parse the JSON data from the request
    info = request.json

    # Retrieve the 'token' from the JSON data
    token = info.get('token')

    # Check if 'token' is provided
    if token is None:
        return jsonify({'result': 'Token not provided'})

    # Perform a database query to fetch stage information
    stages = []
    try:
        stages = Etapa.query.filter_by(token=token).order_by(Etapa.posicion.asc()).all()
    except Exception as e:
        return jsonify({'result': 'Error fetching stage information'})

    # Transform the stage objects to a JSON-serializable format
    result = [{key: getattr(stage, key) for key in stage.__table__.columns.keys()} for stage in stages]

    return jsonify({'result': result})


@stage_bp.route('/editStagePos', methods=['POST'], endpoint='editStagePos')
def edit_stage_position():
    # Parse the JSON data from the request
    info = request.json

    # Retrieve the 'stage_id' and 'pos' from the JSON data
    stage_id = info.get('stage_id')
    pos = info.get('pos')

    # Check if 'stage_id' and 'pos' are provided
    if stage_id is None or pos is None:
        return jsonify({'result': 'Stage ID or position not provided'})

    # Perform a database query or execute a stored procedure to update the stage position
    try:
        # Modify this part to execute the stored procedure or query
        # Here's an example using SQLAlchemy assuming you have an Etapa model
        stage = Etapa.query.get(stage_id)
        if stage:
            stage.posicion = pos
            db.session.commit()
        else:
            return jsonify({'result': 'Stage not found'})
    except Exception as e:
        return jsonify({'result': 'Error updating stage position'})

    return jsonify({'result': True})


@stage_bp.route('/createStage', methods=['POST'], endpoint='createStage')
def create_stage():
    info = request.json

    # Extract information from the JSON data
    usuario = info.get('usuario', '')
    token = info.get('token', '')
    tipo = info.get('tipo', '')
    titulo = info.get('titulo', '')
    subtitulo = info.get('subtitulo', '')

    # Create a new stage
    new_stage = Etapa(token=token, tipo=tipo, titulo=titulo, subtitulo=subtitulo, posicion = 0)
    db.session.add(new_stage)
    db.session.flush()  # This ensures that the stage is assigned an ID

    etapa_id = new_stage.id  # Get the ID of the newly created stage

    # Create stage data records
    stage_data = info.copy()
    del stage_data['usuario']
    del stage_data['token']
    del stage_data['tipo']
    del stage_data['titulo']
    del stage_data['subtitulo']

    for meta_key, meta_value in stage_data.items():
        new_stage_data = EtapaData(etapa_id=etapa_id, meta_key=meta_key, meta_value=meta_value)
        db.session.add(new_stage_data)

    db.session.commit()

    return jsonify({'result': True, 'id_etapa': etapa_id})

@stage_bp.route('/getStageGeneralInfo', methods=['POST'], endpoint='getStageGeneralInfo')
def getStageGeneralInfo():
    try:
        # Parse the JSON data from the request
        info = request.json     

        # Extract the 'identificador' from the JSON data
        identificador = info['identificador']

        # Query the database to get general information about the specified stage
        stage = Etapa.query.filter_by(id=identificador).first()

        # Check if the stage with the specified ID exists
        if stage:
            result = {
                'id': stage.id,
                'token': stage.token,
                'tipo': stage.tipo,
                'titulo': stage.titulo,
                'subtitulo': stage.subtitulo,
                'posicion': stage.posicion
            }
        else:
            result = None

        # Return the result as JSON
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})
    
@stage_bp.route('/getStageInfo', methods=['POST'], endpoint='getStageInfo')
def getStageInfo():
    try:
        # Parse the JSON data from the request
        info = request.json

        # Extract the 'identificador' from the JSON data
        identificador = info['identificador']

        # Query the database to get detailed information about the specified stage and related stage data
        stage = Etapa.query.get(identificador)
        stage_data = EtapaData.query.filter_by(etapa_id=identificador).all()

        # Check if the stage with the specified ID exists
        if stage:
            result = {
                'id': stage.id,
                'token': stage.token,
                'tipo': stage.tipo,
                'titulo': stage.titulo,
                'subtitulo': stage.subtitulo,
                'posicion': stage.posicion,
                'stage_data': [{'meta_key': data.meta_key, 'meta_value': data.meta_value} for data in stage_data]
            }
        else:
            result = None

        # Return the result as JSON
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})

@stage_bp.route('/editEtapa', methods=['POST'], endpoint='editEtapa')
def editEtapa():
    try:
        # Parse the JSON data from the request
        info = request.json

        # Extract the stage ID, title, and sub-title from the JSON
        etapa_id = info['etapa_id']
        titulo = info['titulo']
        subtitulo = info['subtitulo']

        # Update the stage information in the database
        stage = Etapa.query.get(etapa_id)
        if stage:
            stage.titulo = titulo
            stage.subtitulo = subtitulo
            db.session.commit()

        # Extract and update the stage data
        for key, value in info.items():
            if key not in ['usuario_context', 'url_context', 'debug_context', 'etapa_id', 'titulo', 'subtitulo']:
                stage_data = EtapaData.query.filter_by(etapa_id=etapa_id, meta_key=key).first()
                if stage_data:
                    stage_data.meta_value = value
                    db.session.commit()

        return jsonify({'result': True})

    except Exception as e:
        return jsonify({'result': False, 'error': str(e)})



@stage_bp.route('/deleteEtapa', methods=['POST'], endpoint='deleteEtapa')
def deleteEtapa():
    info = request.get_json()
    etapa_id = info["etapa_id"]

    # Delete related EtapaData
    EtapaData.query.filter_by(etapa_id=etapa_id).delete()

    EtapaOpcion.query.filter_by(etapa_id=etapa_id).delete()

    # Get token and posicion
    etapa = Etapa.query.get(etapa_id)
    if etapa:
        token = etapa.token
        posicion = etapa.posicion

        # Delete Etapa
        db.session.delete(etapa)

        # Update positions for remaining Etapas
        Etapa.query.filter(Etapa.token == token, Etapa.posicion > posicion).update({Etapa.posicion: Etapa.posicion - 1})

        db.session.commit()

    return jsonify({'result': True})       
