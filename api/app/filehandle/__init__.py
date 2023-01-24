from flask.blueprints import Blueprint

file_blueprint = Blueprint('file', __name__, template_folder='templates')

from . import views
from . import models
from . import services