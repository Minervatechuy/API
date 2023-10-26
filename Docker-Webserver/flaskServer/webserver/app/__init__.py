from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    ma.init_app(app)

    from app.routes import user_bp
    app.register_blueprint(user_bp)

    from app.routes import calculators_bp
    app.register_blueprint(calculators_bp)

    from app.routes import stage_bp
    app.register_blueprint(stage_bp)

    from app.routes import stage_opcion_bp
    app.register_blueprint(stage_opcion_bp)

    from app.routes import entitie_bp
    app.register_blueprint(entitie_bp)

    from app.routes import budget_bp
    app.register_blueprint(budget_bp)     

    from app.routes import token_bp
    app.register_blueprint(token_bp)       

    return app

