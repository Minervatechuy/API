from flask import Blueprint

user_bp = Blueprint('user', __name__)
from . import user  # Import user route here

calculators_bp = Blueprint('calculators', __name__)  # Update the name to 'calculators'
from . import calculator  # Import calculator route here

stage_bp = Blueprint('stage', __name__)  # Update the name to 'stage'
from . import stage  # Import phase route here

stage_opcion_bp = Blueprint('stage_opcion', __name__)  # Update the name to 'stage_opcion'
from . import stage_opcion  # Import stage_opcion route here

entitie_bp = Blueprint('entitie', __name__)  # Update the name to 'entitie'
from . import entitie  # Import entitie route here

budget_bp = Blueprint('budget', __name__)  # Update the name to 'budget'
from . import budget  # Import budget route here

token_bp = Blueprint('token', __name__)  # Update the name to 'budget'
from . import token  # Import budget route here
