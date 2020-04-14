from project import db
import datetime

class Plants(db.Model):

    __tablename__ = 'plants'

    plant_id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String, nullable=False)
    plant_description = db.Column(db.String, nullable=False)
    watering_frequency = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # image_filename = db.Column(db.String, default=None, nullable=True)
    # image_url = db.Column(db.String, default=None, nullable=True)


    def __init__(self, name, description, frequency):
        self.plant_name = name
        self.plant_description = description
        self.watering_frequency = frequency
        #self.created_at = created_at
        # self.image_filename = image_filename
        # self.image_url = image_url
