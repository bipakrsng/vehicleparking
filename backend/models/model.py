from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
from datetime import datetime

db = SQLAlchemy()

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    

class RolesUsers(db.Model):
    id = db.Column( db.Integer(), primary_key=True )
    user_id = db.Column( db.Integer(), db.ForeignKey('user.id') )
    role_id = db.Column( db.Integer(), db.ForeignKey('role.id') )

class User(db.Model,UserMixin,RoleMixin,TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    address_line1= db.Column(db.String(255))
    address_line2= db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    pincode = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    gender = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(50))
    fs_uniquifier = db.Column(db.String(255), unique=True,nullable=False)
    last_login_at = db.Column(db.DateTime())
    roles = db.relationship('Role',secondary='roles_users',backref=db.backref('users',lazy='dynamic'))

class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255),unique=True)
    description = db.Column(db.String(255))

# ParkingLot model
class ParkingLot(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(255))
    price = db.Column(db.Float)
    address_line1 = db.Column(db.String(255))
    address_lin2 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    pincode = db.Column(db.String(255))
    number_of_spot = db.Column(db.Integer, default=0)

    # Relationship to ParkingSpot (one-to-many)
    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True) #lazy = true means that the related objects are loaded on demand. This is the default behavior. If you want to load all related objects at once, you can set lazy to 'joined' or 'subquery'.

# ParkingSpot model
class ParkingSpot(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    status = db.Column(db.String(255), default='available')

    # Relationship to ReserveParkingSpot (one-to-many)
    reservations = db.relationship('ReserveParkingSpot', backref='parking_spot', lazy=True)


# ReserveParkingSpot model
class ReserveParkingSpot(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    parking_timestamp = db.Column(db.DateTime)
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost = db.Column(db.Float)

    # Relationship to User (one-to-many)
    user = db.relationship('User', backref='reservations')
