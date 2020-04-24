from project import db
import datetime
from sqlalchemy.ext.hybrid import hybrid_method

class Plants(db.Model):

    __tablename__ = 'plants'

    plant_id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String, nullable=False)
    plant_description = db.Column(db.String, nullable=False)
    watering_frequency = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)


    def __init__(self, name, description, frequency, image_filename=None, image_url=None):
        self.plant_name = name
        self.plant_description = description
        self.watering_frequency = frequency
        #self.created_at = created_at
        self.image_filename = image_filename
        self.image_url = image_url

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_plaintext = db.Column(db.String, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password_plaintext):
        self.name = name
        self.email = email
        self.password_plaintext = password_plaintext
        self.authenticated = False

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return self.password_plaintext == plaintext_password

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
