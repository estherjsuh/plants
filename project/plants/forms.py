'''
2 Forms to handle plant data
'''

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class AddPlantForm(FlaskForm):
    '''Adds new plant'''
    plant_name = StringField('Plant Name', validators=[DataRequired()])
    plant_description = StringField('Plant Description', validators=[DataRequired()])
    watering_frequency = IntegerField('Watering Frequency', validators=[DataRequired()])
    plant_photo = FileField('Plant Photo', validators=[FileRequired()])

class EditPlantForm(FlaskForm):
    '''Edits exisitng plant'''
    plant_name  = StringField('Plant Name', validators=[])
    plant_description = StringField('Plant Description', validators=[])
    watering_frequency = IntegerField('Watering Frequency', validators=[])
    plant_photo = FileField('Plant Photo')
