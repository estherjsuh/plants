from project import db, bcrypt
import datetime
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

class Plants(db.Model):

    __tablename__ = 'plants'

    plant_id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String, nullable=False)
    plant_description = db.Column(db.String, nullable=False)
    watering_frequency = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    def __init__(self, user_id,name, description, frequency, image_filename=None, image_url=None):
        self.user_id = user_id
        self.plant_name = name
        self.plant_description = description
        self.watering_frequency = frequency
        self.image_filename = image_filename
        self.image_url = image_url
        self.user_id = user_id

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    plants = db.relationship('Plants', backref='user', lazy='dynamic')

    def __init__(self, name, email, plaintext_password):
        self.name = name
        self.email = email
        self.password = plaintext_password
        self.authenticated = False

    @hybrid_property
    def password(self):
        return self._password_hash

    #For consistency with Python properties, SQLAlchemy decided to disallow the use of functions called something other than the name of the hybrid proprerty that they affect. So the above now needs to be:
    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)
