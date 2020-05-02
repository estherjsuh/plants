from flask import Flask
from project.plants.views import plants_blueprint
from project.users.views import users_blueprint
from .models import User
from .extensions import db, login_manager, bcrypt
from .commands import create_tables


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
