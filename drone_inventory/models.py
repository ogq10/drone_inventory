from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid # stands for unique user identifier - WIll use for Primary Keys

# Adding Flask Security for password protection - comes built in with flask
from werkzeug.security import generate_password_hash, check_password_hash

#import secrets module (provided by python)
import secrets

#import for Flask-Login classes
from flask_login import UserMixin, LoginManager

# Install our Marshaller
from flask_marshmallow import Marshmallow



db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Drone', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User: {self.email} has been created and added to the database!"


class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision = 10, scale = 2))
    camera_quality = db.Column(db.String(120), nullable = True)
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_prod = db.Column(db.Numeric(precision = 10, scale = 2))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_prod, series, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.series = series
        self.user_token = user_token

    def __repr__(self):
        return f'The following drone has been created: {self.name}'
    
    def set_id(self):
        return str(uuid.uuid4())


# API Schema via Marshmallow
class DroneSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'desciription', 'camera_quality', 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'series']

# Singular data point return
drone_schema = DroneSchema()

# List of multiple onjects returned
drone_schemas = DroneSchema(many = True)