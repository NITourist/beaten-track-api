from flask.blueprints import Blueprint

from mysqldb import db

arts = Blueprint('arts', __name__, template_folder='templates', static_folder='static')
