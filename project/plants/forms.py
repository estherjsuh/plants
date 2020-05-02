from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class AddPlantForm(FlaskForm):
    plant_name = StringField('Plant Name', validators=[DataRequired()])
    plant_description = StringField('Plant Description', validators=[DataRequired()])
    watering_frequency = IntegerField('Watering Frequency', validators=[DataRequired()])
    plant_photo = FileField('Plant Photo', validators=[FileRequired()])

class EditPlantForm(FlaskForm):
    plant_name  = StringField('Plant Name', validators=[])
    plant_description = StringField('Plant Description', validators=[])
    watering_frequency = IntegerField('Watering Frequency', validators=[])
    plant_photo = FileField('Plant Photo')
