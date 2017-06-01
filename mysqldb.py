from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

db = SQLAlchemy()

Base = declarative_base()
