from flask import jsonify, request
from app import db
from app.routes import stage_opcion_bp
from app.models import EtapaOpcion

@stage_opcion_bp.route('/insertOpcion', methods=['POST'], endpoint='insertOpcion')
def insertOpcion():
    try:
        # Parse the JSON data from the request
        info = request.json

        # Convierto las claves del JSON en una lista
        keys_arr = list(info.keys())

        # Extract the user and etapa_id from the JSON
        usuario = info['usuario']
        etapa_id = info['etapa_id']

        # Iterate over the options to insert into the database
        for k in range(5, len(info)):
            clave = keys_arr[k]
            valor = info[keys_arr[k]]

            # If the option is an image, handle it separately
            if clave == 'imagen' and valor != '':
                imagen = valor
                option = EtapaOpcion(etapa_id=etapa_id, meta_key=clave, meta_value='imagen', imagen=imagen)
            else:
                option = EtapaOpcion(etapa_id=etapa_id, meta_key=clave, meta_value=valor)

            db.session.add(option)

        db.session.commit()

        return jsonify({'result': True, 'id_etapa': etapa_id})

    except Exception as e:
        return jsonify({'result': False, 'error': str(e)})
    
@stage_opcion_bp.route('/getOpciones', methods=['POST'], endpoint='getOpciones')
def getOpciones():
    # Parse the JSON data from the request
    info = request.json

    # Extract the 'identificador' from the JSON
    identificador = info.get('identificador')

    # Use SQLAlchemy to fetch EtapaOpcion records
    opciones = EtapaOpcion.query.filter_by(etapa_id=identificador).order_by(EtapaOpcion.id).all()

    # Prepare the result
    result = []
    for opcion in opciones:
        result.append({
            'id': opcion.id,
            'etapa_id': opcion.etapa_id,
            'meta_key': opcion.meta_key,
            'meta_value': opcion.meta_value,
            'imagen': opcion.imagen
        })

    # Split the results into chunks of three
    chunk_size = 3
    chunked_result = [result[i:i + chunk_size] for i in range(0, len(result), chunk_size)]

    # Return the chunked result
    return jsonify({'result': chunked_result})

@stage_opcion_bp.route('/editOpcion', methods=['POST'], endpoint='editOpcion')
def editOpcion():
    try:
        # Parse the JSON data from the request
        info = request.json

        # Extract the 'data_id' from the JSON
        data_id = info.get('data_id')

        # Iterate over the keys in the JSON to update options
        for key in info.keys():
            if key not in ('usuario_context', 'url_context', 'debug_context', 'data_id'):
                value = info[key]

                # Handle 'imagen' separately
                if key == 'imagen' and value != '':
                    option = EtapaOpcion.query.get(data_id)
                    option.meta_key = key
                    option.meta_value = 'imagen'
                    option.imagen = value
                else:
                    option = EtapaOpcion.query.get(data_id)
                    option.meta_key = key
                    option.meta_value = value
                    option.imagen = None

                db.session.commit()

        return jsonify({'result': True, 'id_etapa': data_id})
    except Exception as e:
        return jsonify({'result': False, 'error': str(e)})

@stage_opcion_bp.route('/getOpcion', methods=['POST'], endpoint='getOpcion')
def getOpcion():
    try:
        # Parse the JSON data from the request
        info = request.json

        # Extract the identifier from the JSON
        identificador = info['identificador']

        # Query the EtapaOpcion model for the options
        options = EtapaOpcion.query.filter(
            (EtapaOpcion.id == identificador) |
            (EtapaOpcion.id == identificador + 1) |
            (EtapaOpcion.id == identificador + 2)
        ).all()

        result = [{key: getattr(option, key) for key in option.__table__.columns.keys()} for option in options]

        # Return the result
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'result': False, 'error': str(e)})     

@stage_opcion_bp.route('/deleteOpcion', methods=['POST'], endpoint='deleteOpcion')
def deleteOpcion():
    info = request.get_json()

    etapa_id = info["opcion_id"]
    
    # Delete the option
    option = EtapaOpcion.query.get(etapa_id)
    if option:
        db.session.delete(option)
        db.session.commit()

        # Optionally, you may want to do the additional deletions here
        for i in range(1, 3):
            next_etapa_id = etapa_id + i
            next_option = EtapaOpcion.query.get(next_etapa_id)
            if next_option:
                db.session.delete(next_option)
                db.session.commit()

    return jsonify({'result': True})