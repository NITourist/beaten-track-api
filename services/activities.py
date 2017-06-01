from flask import Blueprint
from flask import jsonify
from flask import request

from models import Activities
from models import Locations
from models import Images
from models import Scores
from mysqldb import db
import json

activities = Blueprint('activities', __name__, template_folder='templates')

from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


@activities.route('/activity', methods=['POST'])
def create_activity():
    # fetch name and rate from the request
    name = request.get_json()["name"]
    rating = request.get_json()["rating"]
    # score = request.get_json()["score"]
    stars = request.get_json()["stars"]
    price = request.get_json()["price"]
    sale_price = request.get_json()["sale_price"]
    address = request.get_json()["address"]
    description = request.get_json()["description"]
    location_text = request.get_json()["location_text"]
    features = request.get_json()["features"]
    room_amenities = request.get_json()["room_amenities"]
    thumb = request.get_json()["thumb"]
    location = request.get_json()["location"]
    images = request.get_json()["images"]

    activity = Activities()
    activity.name = name
    activity.rating = rating
    # activity.score = score
    activity.stars = stars
    activity.price = price
    activity.sale_price = sale_price
    activity.address = address
    activity.description = description
    activity.location_text = location_text
    activity.features = features
    activity.room_amenities = room_amenities
    activity.thumb = thumb

    curr_session = db.session  # open database session

    if location:
        location = Locations(lat=location['lat'], lon=location['lon'], distance=location['distance'])
        curr_session.flush()
        activity.location = location.id
        curr_session.add(location)

    if images:
        image = Images(image_1=images[0])
        # TODO Add images 2-5
        curr_session.flush()
        activity.images = image.id
        curr_session.add(image)

    try:
        curr_session.add(activity)  # add prepared statment to opened session
        curr_session.commit()  # commit changes
    except Exception as e:
        curr_session.rollback()
        curr_session.flush()  # for resetting non-commited .add()

    activity_id = activity.id  # fetch last inserted id
    data = Activities.query.filter_by(id=activity_id).first()  # fetch our inserted activity

    return jsonify(data._asdict())
