from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import images


class AddPlantForm(Form):
    plant_name = StringField('Plant Name', validators=[DataRequired()])
    plant_description = StringField('Plant Description', validators=[DataRequired()])
    watering_frequency = IntegerField('Watering Frequency', validators=[DataRequired()])
    created_at = DateFrield('Created At', validators=[DataRequired()])
    plant_photo = FileField('Plant Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
