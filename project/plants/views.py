from flask import render_template, Blueprint, request, redirect, url_for, flash, abort, jsonify
from project.models import Plants
from .forms import AddPlantForm
from project import db, images
###CONFIG###
plants_blueprint = Blueprint('plants', __name__, template_folder='templates')

##FUNCTION##
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')


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
            filename = images.save(request.files['plant_photo'])
            url = images.url(filename)
            new_plant = Plants(form.plant_name.data, form.plant_description.data, form.watering_frequency.data, filename, url
            )
            db.session.add(new_plant)
            db.session.commit()
            flash('Yay! {} joined the crew'.format(new_plant.plant_name.title()), 'success')
            return redirect(url_for('plants.all'))
        else:
            flash_errors(form)
            flash('Error: Plant could not be added.', 'error')
    return render_template('add_plant.html', form=form)


@plants_blueprint.route('/gallery')
def gallery():
    all_plants = Plants.query.all()
    return render_template('gallery.html',plants=all_plants)

@plants_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    data = Plants.query.filter(Plants.plant_id == id)
    plant = data.first()
    if plant:
        form = AddPlantForm(formdata=request.form, obj=plant)
        if request.method == 'POST' and form.validate():
            save_changes(plant, form)
            flash('Plant updated successfully!')
            return reditect(url_for('plants.all'))
        return render_template('edit.html', form=form)
    else:
        flash_errors(form)
        flash('Error: Plant could not update')
