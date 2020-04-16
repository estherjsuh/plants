from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

#If we set instance_relative_config=True when we create our app with the Flask() call, app.config.from_pyfile() will load the specified file from the instance/ directory.

##CONFIG - LOADS CONFIGURATION FROM CONFIG FILE##
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

db = SQLAlchemy(app) #db instance

#Configure image uploading
images = UploadSet('images', IMAGES)
configure_uploads(app, images)


##BLUEPRINTS##
from project.plants.views import plants_blueprint

#register the blueprints
app.register_blueprint(plants_blueprint)
