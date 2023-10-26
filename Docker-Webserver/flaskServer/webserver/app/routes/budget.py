from flask import jsonify, request
from app import db
from app.routes import budget_bp

@budget_bp.route('/get_presupuestos_email', methods=['POST'], endpoint='get_presupuestos_email')
def get_presupuestos_email():
    info = request.get_json()
    # Extract the email from the request data
    email = info["email"]

    # Query to retrieve the budget information
    sql_query = """
        SELECT c.name, cpc.fecha, cli.email, cli.telephone, cli.name, p.finalizado, p.resultado
        FROM usuarios u, users_to_entities ue, entities e, entidades_calculadoras ec, calculators c, calculadoras_presupuestos_clientes cpc, presupuestos p, clientes cli
        WHERE u.mail="%s" AND u.mail=ue.user_email AND ue.entity_id=e.ID AND ue.entity_id=ec.id_entidad AND ec.token=cpc.token AND cpc.token=c.token AND cpc.presupuestos_id=p.id AND cpc.email_cliente=cli.email
        ORDER BY cpc.fecha DESC
    """ % email

    # Execute the query and fetch the results
    results = db.session.execute(sql_query)

    # Build the result dictionary
    result = []
    for row in results:
        result.append({
            'name': row[0],
            'fecha': row[1],
            'email': row[2],
            'telephone': row[3],
            'client_name': row[4],
            'finalizado': row[5],
            'resultado': row[6]
        })

    # Return the result as JSON
    return jsonify({'result': result})


@budget_bp.route('/get_presupuestos_entidad', methods=['POST'], endpoint='get_presupuestos_entidad')
def get_presupuestos_entidad():
    info = request.get_json() 
    # Extract the email from the request data 
    entidad_id = info["entidad_id"] 
 
    # Query to retrieve the budget information 
    sql_query = """ 
        SELECT p.id, e.nombre, c.name,  p.resultado, p.formula, p.finalizado, cli.email, cli.telephone, cli.name, cpc.fecha 
        FROM entities e, entidades_calculadoras ec, calculators c, calculadoras_presupuestos_clientes cpc, presupuestos p, clientes cli 
        WHERE e.ID = "%s" AND ec.id_entidad=e.ID AND ec.token=cpc.token AND cpc.presupuestos_id=p.id AND cpc.email_cliente=cli.email; 
    """ % entidad_id 
 
    # Execute the query and fetch the results 
    results = db.session.execute(sql_query) 
 
    # Build the result dictionary 
    result = [] 
    for row in results: 
        result.append({ 
            'id': row[0], 
            'nombre': row[1], 
            'name': row[2], 
            'resultado': row[3], 
            'formula': row[4], 
            'finalizado': row[5], 
            'email': row[6], 
            'telephone': row[7], 
            'client_name': row[8],
            'fecha': row[9]             
        }) 
 
    # Return the result as JSON 
    return jsonify({'result': result})