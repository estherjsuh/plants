from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired
#from flask_wtf.file import FileField, FileAllowed, FileRequired
#from app import images


class AddPlantForm(FlaskForm):
    plant_name = StringField('Plant Name', validators=[DataRequired()])
    plant_description = StringField('Plant Description', validators=[DataRequired()])
    watering_frequency = IntegerField('Watering Frequency', validators=[DataRequired()])
    #created_at = DateFrield('Created At', validators=[DataRequired()])
    #plant_photo = FileField('Plant Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
