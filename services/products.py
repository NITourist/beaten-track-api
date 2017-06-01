from flask import jsonify
from flask import request
from flask.blueprints import Blueprint

from mysqldb import db
from models import Products

products = Blueprint('products', __name__, template_folder='templates', static_folder='static')


@products.route('/product', methods=['POST'])
def create_product():
    # fetch name and rate from the request
    rate = request.get_json()["rate"]
    name = request.get_json()["name"]

    product = Products(rate=rate, name=name)  # prepare query statement

    curr_session = db.session  # open database session
    try:
        curr_session.add(product)  # add prepared statment to opened session
        curr_session.commit()  # commit changes
    except:
        curr_session.rollback()
        curr_session.flush()  # for resetting non-commited .add()

    product_id = product.id  # fetch last inserted id
    data = Products.query.filter_by(id=product_id).first()  # fetch our inserted product

    result = [data.name, data.rate]  # prepare visual data

    return jsonify(session=result)


@products.route('/products', methods=['GET'])
def get_product():
    data = Products.query.all()  # fetch all products on the table

    data_all = []

    for product in data:
        data_all.append([product.id, product.name, product.rate])  # prepare visual data

    return jsonify(products=data_all)


@products.route('/<int:product_id>/product', methods=['PATCH'])
def update_product(product_id):
    rate = request.get_json()["rate"]  # fetch rate
    curr_session = db.session

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


@products.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    curr_session = db.session  # initiate database session

    Products.query.filter_by(id=product_id).delete()  # find the product by product_id and deletes it
    curr_session.commit()  # commit changes to the database

    return get_product()  # return all create products
