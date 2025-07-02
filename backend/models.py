from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
from app import app
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# User model
class User(db.Model):
    
    __tablename__ = 'users'
    
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passhash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)

# Parking lot model
class ParkingLot(db.Model):
    
    __tablename__ = 'parking_lots'
    
    
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete-orphan", lazy=True)

# Parking spot model
class ParkingSpot(db.Model):
    
    __tablename__ = 'parking_spots'
    
    
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    is_avail = db.Column(db.Boolean, default=True, nullable=False)
    spot_number = db.Column(db.String(10), nullable=False)
    reservations = db.relationship('Reservation', backref='spot', lazy=True)

# Reservation model
class Reservation(db.Model):
    
    __tablename__ = 'reservations'



    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at= db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
