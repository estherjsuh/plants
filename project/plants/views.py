from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from project.models import Plants, User
from .forms import AddPlantForm, EditPlantForm
from project import db, app
from werkzeug.utils import secure_filename
import os
###CONFIG###
plants_blueprint = Blueprint('plants', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

##FUNCTION##
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


##ROUTES##

@plants_blueprint.route('/')
def hello():
    return render_template('hello.html')

@plants_blueprint.route('/plants')
@login_required
def all():
    all_plants = Plants.query.filter_by(user_id=current_user.user_id).order_by(Plants.created_at.desc())
    return render_template('plants.html', plants=all_plants)

@plants_blueprint.route('/new', methods=['GET','POST'])
@login_required
def add_plant():
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = AddPlantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if 'plant_photo' not in request.files:
                flash('No plant photo added')
                return redirect(request.url)

            file = request.files['plant_photo']

            if file.filename=='':
                flash('No plant photo selected ')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                url = os.path.join(app.config['IMAGE_URL'], filename)
            else:
                filename = ''
                url = ''

            # filename = images.save(request.files['plant_photo'])
            # url = images.url(filename)
            new_plant = Plants(current_user.user_id, form.plant_name.data, form.plant_description.data, form.watering_frequency.data, filename, url)        
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
    all_plants = Plants.query.order_by(Plants.created_at.desc()).all()
    #all_plants.order_by(desc(Plants.created_at))
    return render_template('gallery.html',plants=all_plants)

@plants_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    plant = Plants.query.filter_by(plant_id=id).first_or_404()
    form = EditPlantForm()
    if request.method=='POST':
        if form.validate_on_submit():
            plant.plant_name = form.plant_name.data
            plant.plant_description = form.plant_description.data
            plant.watering_frequency = form.watering_frequency.data
            if form.plant_photo.has_file():
                file = request.files['plant_photo']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                url = os.path.join(app.config['IMAGE_URL'], filename)
                plant.image_filename = filename
                plant.image_url = url
            db.session.add(plant)
            db.session.commit()
            flash('{} has been updated'.format(plant.plant_name), 'success')
            return redirect(url_for('plants.all'))
        else:
            flash_errors(form)
            flash('Could not udpate {}'.format(plant.plant_name), 'error')
    return render_template('edit.html', form=form, plant=plant)

@plants_blueprint.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    plant = Plants.query.filter_by(plant_id=id).first_or_404()
    if request.method=='POST':
        db.session.delete(plant)
        db.session.commit()
        flash('{} Deleted'.format(plant.plant_name), 'success')
        return redirect(url_for('plants.all'))
    else:
        flask('Could not delete {}'.format(plant.plant_name), 'error')
