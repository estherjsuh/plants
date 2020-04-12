from flask import Flask, jsonify, request, render_template
from flask_uploads import UploadSet, IMAGES, configure_uploads
#from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
#from forms import AddPlantForm
#from flask_sqlalchemy import SQLAlchemy
from .forms import AddPlantForm
#from resources.plant import Plant
app = Flask(__name__)
#app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
#db = SQLAlchemy(app)
#db = SQLAlchemy(app)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

# @app.route('/new', methods=['POST', 'GET'])
# def create_plant():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         description = request.form['description']
#         frequency = request.form['frequency']
#         created_at = request.form['created_at']
#         plant_photo = photos.save(request.files['plant_photo'])
#         return '<h2>Plant {} has been added</h2>'.format(name.title())
#
#     # request_data = request.get_json()
#     #
#     # new_plant = {
#     #     'name': request_data['name'],
#     #     'description': request_data['description'],
#     #     'frequency' : request_data['frequency'],
#     #     'created_at': request_data['created_at']
#     # }
#     # plants.append(new_plant)
#
#     #the name in the form method below is what is being fed to above
#     return ''' <form method="POST" enctype=multipart/form-data action="{{url_for('upload')}}">
#         Name <input type ="text" name="name"><br>
#         Description <input type="text" name="description"><br>
#         Frequency <input type="number" name="frequency"><br>
#         Created At <input type="date" name="created_at"><br>
#         Plant Photo <input type="file" name="plant_photo"><br>
#         <input type = "submit">
#         </form>'''
@app.route('/')
def homepage():
    return render_template('hello.html')


@app.route('/new', methods=['POST', 'GET'])
def add_plant():
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = AddPlantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = images.save(request.files['plant_photo'])
            url = images.url(filename)
            new_plant = Plant(form.plant_name.data, form.plant_description.data, form.watering_frequency.data, form.created_at.data, filename, url)
            db.session.add(new_plant)
            db.session.commit()
            flash('New Plant {}, added!'.format(new_plant.plant_name), 'success')
            return redirect(url_for(homepage))
        else:
            flash_errors(form)
            flash('ERROR! Plant could not be added.', 'error')

    return render_template('add_plant.html', form=form)

    #jsonify(new_plant)
if __name__ == '__main__':
    app.run(port=5000, debug=True)
