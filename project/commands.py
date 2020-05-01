import click
from flask.cli import with_appcontext

from .extensions import db
from .models import Plants, User

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    db.session.commit()
