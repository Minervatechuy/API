from flask import jsonify, request
from app import db
from app.routes import token_bp
from app.models import Tokens

@token_bp.route('/comprar_token', methods=['POST'], endpoint='comprar_token')
def comprar_token():
    # Se trae la información que viene de la vista en json
    info = request.get_json()

    # Find the first unsold token
    token = Tokens.query.filter_by(vendido=False).first()

    if token:
        # Update the token as sold
        token.vendido = True
        db.session.commit()

        # Return the token value
        return jsonify({'result': token.token})
    else:
        return jsonify({'result': None})