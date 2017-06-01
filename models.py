from mysqldb import db
from collections import OrderedDict


class Activities(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    stars = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.00)
    sale_price = db.Column(db.Float, nullable=False, default=0.00)
    location = db.Column('location', db.Integer, db.ForeignKey("locations.id"), nullable=True)
    address = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    location_text = db.Column(db.String(512), nullable=False)
    features = db.Column(db.String(512), nullable=False)
    room_amenities = db.Column(db.String(512), nullable=False)
    thumb = db.Column(db.String(128), nullable=False)
    images = db.Column('images', db.Integer, db.ForeignKey("images.id"), nullable=True)

    # scores = db.relationship('Scores', backref='activities')

    def __repr__(self):
        return '<Activities (%s, %s) >' % (self.rate, self.name)

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


class Locations(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Integer, nullable=False, default=0)
    lon = db.Column(db.Integer, nullable=False, default=0)
    distance = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Locations (%s, %s, %s) >' % (self.id, self.lat, self.lon)


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_1 = db.Column(db.String(128), nullable=False, default=0)
    image_2 = db.Column(db.String(128), nullable=True)
    image_3 = db.Column(db.String(128), nullable=True)
    image_4 = db.Column(db.String(128), nullable=True)
    image_5 = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return '<Images (%s, %s) >' % (self.id, self.image_1)


class Scores(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, default=0)
    score = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Scores (%s, %s, %s) >' % (self.id, self.name, self.score)


# class LocationScores(db.Model):
#     __tablename__ = 'location_scores_table'
#
#     activities_id = db.Column(db.Integer, db.ForeignKey('activities.id'), primary_key=True)
#     activities = db.relationship(Activities, primaryjoin=activities_id == Activities.id, backref='subscriptions')
#     scores_id = db.Column(db.Integer, db.ForeignKey('scores.id'), primary_key=True)
#     scores = db.relationship(Scores, primaryjoin=scores_id == Scores.id, backref='subscriptions')


class Arts(db.Model):
    __tablename__ = 'arts'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Arts (%s, %s) >' % (self.rate, self.name)


class Bars(db.Model):
    __tablename__ = 'bars'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Bars (%s, %s) >' % (self.rate, self.name)


class Culture(db.Model):
    __tablename__ = 'culture'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Culture (%s, %s) >' % (self.rate, self.name)


class Landmarks(db.Model):
    __tablename__ = 'landmarks'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Landmarks (%s, %s) >' % (self.rate, self.name)


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Products (%s, %s) >' % (self.rate, self.name)


class Restaurants(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Restaurants (%s, %s) >' % (self.rate, self.name)
