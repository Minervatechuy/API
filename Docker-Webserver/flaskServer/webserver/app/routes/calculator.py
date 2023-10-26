from flask import jsonify, request
from app import db
from app.routes import calculators_bp
from app.models import Calculators, Tokens, UsersToCalculators, EntidadesCalculadoras, Usuarios, Etapa, EtapaData, EtapaOpcion

@calculators_bp.route('/createCalculator', methods=['POST'], endpoint='createCalculator')
def create_calculator():
    # Parse JSON data from the request
    info = request.json

    token = info['token']
    url = info['url']
    ip = info['ip']
    entidad = info['entidad']
    nombre = info['nombre']
    email = info['email']

    # Check if the token is available
    token_available = Tokens.query.filter_by(token=token, vendido=1, canjeado=0).count()
    if token_available == 0:
        return jsonify({'tipo': 'error', 'mensaje': 'Token inválido'})

    # Check if a calculator already exists for the given URL
    calculator_exists = Calculators.query.filter_by(url=url).count()
    if calculator_exists > 0:
        return jsonify({'tipo': 'error', 'mensaje': 'Ya existe una calculadora para esa página. Por favor, inténtelo con otra dirección'})

    # Find the user by email
    user = Usuarios.query.filter_by(mail=email).first()

    if user:
        # Create a new calculator
        new_calculator = Calculators(token=token, url=url, ip=ip, entity_ID=entidad, name=nombre, activo=1)
        # Add the calculator to the user's calculators (UsersToCalculators)
        user_to_calculator = UsersToCalculators(user_email=email, calculator_token=token)

        # Add and commit changes to the database
        db.session.add(new_calculator)
        db.session.add(user_to_calculator)
        db.session.commit()

        # Update the 'canjeado' status of the token
        token_record = Tokens.query.filter_by(token=token).first()
        token_record.canjeado = 1
        db.session.commit()

        return jsonify({'tipo': 'success', 'mensaje': 'Calculadora creada'})
    else:
        return jsonify({'tipo': 'error', 'mensaje': 'Usuario no encontrado'})


@calculators_bp.route('/getSpecificCalculatorInfo', methods=['POST'], endpoint='getSpecificCalculatorInfo')
def get_specific_calculator_info():
    # Parse the JSON data from the request
    info = request.json

    # Retrieve the 'token' from the JSON data
    token = info.get('token')

    # Check if 'token' is provided
    if token is None:
        return jsonify({'result': 'Token not provided'})

    # Perform a database query or execute a stored procedure to get calculator info
    try:
        # Modify this part to execute the stored procedure or query
        # Here's an example using SQLAlchemy assuming you have a Calculator model
        calculator = (
            db.session.query(Calculators)
            .join(UsersToCalculators, Calculators.token == UsersToCalculators.calculator_token)
            .join(Usuarios, Usuarios.mail == UsersToCalculators.user_email)
            .filter(Calculators.activo == 1, Calculators.token == token)
            .first()
        )
        if calculator:
            result = {
                'name': calculator.name,
                'url': calculator.url,
                'ip': calculator.ip,
                'formula': calculator.formula,
                'entity_ID': calculator.entity_ID,
                'activo': calculator.activo,
                'token': calculator.token
            }
        else:
            return jsonify({'result': 'Calculator not found'})
    except Exception as e:
        return jsonify({'result': 'Error retrieving calculator info'})

    return jsonify({'result': result})   

@calculators_bp.route('/updateFormula', methods=['POST'], endpoint='updateFormula')
def update_formula():
    # Parse the JSON data from the request
    info = request.json

    # Get the token and formula from the JSON data
    token = info.get("token")
    formula = info.get("formula")

    try:
        # Update the formula in the database
        calculator = Calculators.query.filter_by(token=token).first()
        if calculator:
            calculator.formula = formula
            db.session.commit()

            # Return the result
            return jsonify({'result': True})
        else:
            return jsonify({'result': False, 'error': 'Calculator not found'})
    except Exception as e:
        return jsonify({'result': False, 'error': str(e)})


@calculators_bp.route('/getCalcFormula', methods=['POST'], endpoint='getCalcFormula')
def getCalcFormula():
    try:
        # Parse the JSON data from the request
        info = request.json

        # Extract the 'token' from the JSON data
        token = info['token']

        # Query the database to get the formula for the specified calculator
        calculator = Calculators.query.filter_by(token=token).first()

        # Check if the calculator with the specified token exists
        if calculator:
            formula = calculator.formula
        else:
            formula = None

        # Return the result as JSON
        return jsonify({'result': formula})

    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})        

@calculators_bp.route('/deleteCalc', methods=['POST'], endpoint='deleteCalc')
def deleteCalc():
    try:
        # Parse the JSON data from the request
        info = request.json

        # Extract the token from the JSON
        token = info['token']

        # Query the database to retrieve the calculator
        calculator = Calculators.query.filter_by(token=token).first()

        if calculator is not None:
            # Retrieve all related stages
            stages = Etapa.query.filter_by(token=token).all()

            # Loop through each stage and delete its data and options
            for stage in stages:
                stage_id = stage.id

                # Delete stage data
                EtapaData.query.filter_by(etapa_id=stage_id).delete()

                # Delete stage options
                EtapaOpcion.query.filter_by(etapa_id=stage_id).delete()

            # Delete the stages themselves
            Etapa.query.filter_by(token=token).delete()

            # Delete the calculator
            Calculators.query.filter_by(token=token).delete()

            # Commit the changes to the database
            db.session.commit()
        else:
            return jsonify({'result': False, 'error': 'Calculator not found'})

        return jsonify({'result': True})

    except Exception as e:
        return jsonify({'result': False, 'error': str(e)})
    
@calculators_bp.route('/get_presupuestos_calculadora', methods=['POST'], endpoint='get_presupuestos_calculadora')
def get_presupuestos_calculadora():
    info = request.get_json()

    # Se toma el token y la formula del json anterior de cara a la búsqueda
    token = info["token"]

    # Raw SQL Query
    sql_query = """
        SELECT p.id, p.resultado, p.formula, p.finalizado, cli.email, cli.telephone, cli.name, cpc.fecha
        FROM calculators c, calculadoras_presupuestos_clientes cpc, presupuestos p, clientes cli
        WHERE c.token="%s" AND cpc.presupuestos_id=p.id AND cpc.email_cliente=cli.email;
    """ % token

    result = db.session.execute(sql_query)

    result_dict = [{'id': row[0], 'resultado': row[1], 'formula': row[2], 'finalizado': row[3], 'email': row[4], 'telephone': row[5], 'name': row[6], 'fecha': row[7]} for row in result]

    # Se devuelve el resultado
    return jsonify({'result': result_dict})


@calculators_bp.route('/get_presupuestos_calculadoras_nombre', methods=['POST'], endpoint='get_presupuestos_calculadoras_nombre')
def get_presupuestos_calculadoras_nombre():
    info = request.get_json()

    usuario = info["usuario"]

    sql_query = """
        SELECT DISTINCT c.name, c.token
        FROM usuarios u, users_to_entities ue, entities e, entidades_calculadoras ec, calculators c, calculadoras_presupuestos_clientes cpc, presupuestos p, clientes cli
        WHERE u.mail="%s" AND u.mail=ue.user_email AND ue.entity_id=e.ID AND ue.entity_id=ec.id_entidad AND ec.token=cpc.token AND cpc.token=c.token AND cpc.presupuestos_id=p.id AND cpc.email_cliente=cli.email;
    """ % usuario

    result = db.session.execute(sql_query)

    result_dict = [{'name': row[0], 'token': row[1]} for row in result]

    return jsonify({'result': result_dict}) 


@calculators_bp.route('/edit_calulator', methods=['POST'], endpoint='edit_calulator')
def edit_calulator():
    # Extract the request data
    data = request.get_json()
    token = data.get('token')
    nombre = data.get('nombre')
    url = data.get('url')
    entidad = data.get('entidad_id')

    # Check if the URL is already being used by another calculator
    n_url = Calculators.query.filter_by(url=url).count()
    if n_url != 0 and n_url != 1:
        return jsonify({'tipo': "error", "mensaje": "Este dominio ya está siendo utilizado en otra calculadora, por favor inténtelo de nuevo con otro dominio."})

    # Find the calculator by token
    calculator = Calculators.query.filter_by(token=token).first()

    if calculator:
        # Update the calculator properties
        calculator.url = url
        calculator.entity_ID = entidad
        calculator.name = nombre

        # Commit changes to the database
        db.session.commit()

        return jsonify({'tipo': "success", "mensaje": "La calculadora ha sido editada correctamente."})
    else:
        return jsonify({'tipo': "error", "mensaje": "La calculadora no se encontró."})