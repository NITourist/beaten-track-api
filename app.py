import configparser
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask import jsonify
from api_mock import hotels

application = Flask(__name__)

# Read config file
config = configparser.ConfigParser()
config.read('app__db.conf')

# MySQL configurations
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + config.get('DB', 'user') + \
                                                ':' + config.get('DB', 'password') + '@' + \
                                                config.get('DB', 'host') + '/' + config.get('DB', 'db')

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

mysql = SQLAlchemy()

app = Flask(__name__)


@application.route('/hotels', methods=['GET'])
def get_hotels():
    """ returns a list of events """
    return jsonify({'hotels': hotels})


# map models
class Products(mysql.Model):
    __tablename__ = 'products'
    id = mysql.Column(mysql.Integer, primary_key=True)
    rate = mysql.Column(mysql.Integer, nullable=False)
    name = mysql.Column(mysql.String(128), nullable=False)

    def __repr__(self):
        return '<Products (%s, %s) >' % (self.rate, self.name)


@application.route("/")
def hello():
    return "Hello World!"


@application.route('/product', methods=['POST'])
def create_product():
    # fetch name and rate from the request
    rate = request.get_json()["rate"]
    name = request.get_json()["name"]

    product = Products(rate=rate, name=name)  # prepare query statement

    curr_session = mysql.session  # open database session
    try:
        curr_session.add(product)  # add prepared statment to opened session
        curr_session.commit()  # commit changes
    except:
        curr_session.rollback()
        curr_session.flush()  # for resetting non-commited .add()

    product_id = product.id  # fetch last inserted id
    data = Products.query.filter_by(id=product_id).first()  # fetch our inserted product

    config.read('rating_db.conf')

    result = [data.name, data.rate]  # prepare visual data

    return jsonify(session=result)


@application.route('/product', methods=['GET'])
def get_product():
    data = Products.query.all()  # fetch all products on the table

    data_all = []

    for product in data:
        data_all.append([product.id, product.name, product.rate])  # prepare visual data

    return jsonify(products=data_all)


@application.route('/<int:product_id>/product', methods=['PATCH'])
def update_product(product_id):
    rate = request.get_json()["rate"]  # fetch rate
    curr_session = mysql.session

    try:
        product = Products.query.filter_by(id=product_id).first()  # fetch the product do be updated
        product.rate = rate  # update the column rate with the info fetched from the request
        curr_session.commit()  # commit changes
    except:
        curr_session.rollback()
        curr_session.flush()

    product_id = product.id
    data = Products.query.filter_by(id=product_id).first()  # fetch our updated product

    result = [data.name, data.rate]  # prepare visual data

    return jsonify(session=result)


@application.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    curr_session = mysql.session  # initiate database session

    Products.query.filter_by(id=product_id).delete()  # find the product by product_id and deletes it
    curr_session.commit()  # commit changes to the database

    return get_product()  # return all create products


if __name__ == "__main__":
    mysql.init_app(application)
    with application.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        mysql.create_all()
    application.run()
