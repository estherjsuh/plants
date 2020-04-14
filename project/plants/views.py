from flask import render_template, Blueprint, request, redirect, url_for, flash, abort, jsonify
from project.models import Plants
from .forms import AddPlantForm
from project import db
###CONFIG###
plants_blueprint = Blueprint('plants', __name__, template_folder='templates')


##ROUTES##

@plants_blueprint.route('/')
def hello():
    return render_template('hello.html')

@plants_blueprint.route('/plants')
def all():
    all_plants = Plants.query.all()
    return render_template('plants.html', plants=all_plants)

@plants_blueprint.route('/new', methods=['GET','POST'])
def add_plant():
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = AddPlantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #filename = images.save(request.files['plant_photo'])
            #url = images.url(filename)
            new_plant = Plants(form.plant_name.data, form.plant_description.data, form.watering_frequency.data
            #, filename, url,
            )
            db.session.add(new_plant)
            db.session.commit()
            return redirect(url_for('plants.all'))
        # else:
        #     flash_errors(form)
        #     flash('ERROR! Plant could not be added.', 'error')
    return render_template('add_plant.html', form=form)
