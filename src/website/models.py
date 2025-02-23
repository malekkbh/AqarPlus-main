from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from website import app
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    price_for = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    area_classification = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    more = db.Column(db.Text, nullable=True)
    
    email = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    seller_city = db.Column(db.String(50), nullable=False)

    publish_status = db.Column(db.String(50), default='waiting_for_approval' ) # published, unpublished, sold, rented, waiting_for_approval or rejected
    images = db.relationship('PropertyImage', backref='property', lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'category': self.category,
            'type': self.type,
            'area': self.area,
            'unit': self.unit,
            'price': self.price,
            'price_for': self.price_for,
            'currency': self.currency,
            'city': self.city,
            'region': self.region,
            'area_classification': self.area_classification,
            'address': self.address,
            'more': self.more,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'whatsapp': self.whatsapp,
            'seller_city': self.seller_city,
            'publish_status': self.publish_status,
            'images': [{'id': img.id, 'img_url': img.img} for img in self.images]
        }

class PropertyImage(db.Model):
    __tablename__ = 'property_images'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    # link to the image
    img = db.Column(db.String(255), nullable=False)

class DataReq(db.Model):
    __tablename__ = 'data_reqs'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    number_of_individuals = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    is_sale = db.Column(db.Boolean, nullable=False, default=True)

    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    property = db.relationship('Property', backref=db.backref('data_reqs', lazy=True))

    def to_json(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'phone': self.phone,
            'number_of_individuals': self.number_of_individuals,
            'city': self.city,
            'is_sale': self.is_sale,
            'property_id': self.property_id,
        }

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(50), nullable=False, primary_key=True)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        # Use pbkdf2:sha256 as the hashing method
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_json(self):
        return {
            'username': self.username,
        }
        
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    property = db.relationship('Property', backref=db.backref('notifications', lazy=True))
    
    def to_json(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'timestamp': self.timestamp.isoformat()
        }