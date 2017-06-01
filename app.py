import configparser

import os

from flask import Flask

from mysqldb import db
from services.activities import activities
from services.products import products


def create_app():
    app = Flask(__name__)

    # Read config file
    config = configparser.ConfigParser()
    config.read('app_db.conf')

    # MySQL configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + config.get('DB', 'user') + \
                                            ':' + config.get('DB', 'password') + '@' + \
                                            config.get('DB', 'host') + '/' + config.get('DB', 'db')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['DEBUG'] = True

    app.register_blueprint(activities)
    app.register_blueprint(products)

    db.init_app(app)

    return app


def setup_database(app):
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()


if __name__ == "__main__":
    app = create_app()
    # Because this is just a demostration we set up the database like this.
    if not os.path.isfile('/tmp/test.db'):
        setup_database(app)
    app.run()
