from flask import Flask
from project.plants.views import plants_blueprint
from project.users.views import users_blueprint
from .models import User
from .extensions import db, login_manager, bcrypt
from .commands import create_tables
#from flask_sqlalchemy import SQLAlchemy
#from flask_uploads import UploadSet, configure_uploads
#from os.path import join, isfile
#from flask_login import LoginManager
#from flask_bcrypt import Bcrypt
#If we set instance_relative_config=True when we create our app with the Flask() call, app.config.from_pyfile() will load the specified file from the instance/ directory.

def create_app(config_file='settings.py'):
    app=Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = "users.login"
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.user_id==int(user_id)).first()

    app.register_blueprint(plants_blueprint)
    app.register_blueprint(users_blueprint)

    app.cli.add_command(create_tables)



    return app

##CONFIG - LOADS CONFIGURATION FROM CONFIG FILE##
# app = Flask(__name__, instance_relative_config=True)
# app.config.from_pyfile('flask.cfg')
#
# db = SQLAlchemy(app) #db instance
# bcrypt = Bcrypt(app)
#
# login_manager=LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "users.login"
#
# from project.models import User
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.filter(User.user_id==int(user_id)).first()

#Configure image uploading
#images = UploadSet('images', IMAGES)
#configure_uploads(app, images)


##BLUEPRINTS##


#register the blueprints
# app.register_blueprint(plants_blueprint)
# app.register_blueprint(users_blueprint)
