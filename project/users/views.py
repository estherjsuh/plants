from flask import render_template, Blueprint, request, redirect, url_for, flash
from project.models import User
from .forms import RegisterForm
from project import db, app
from sqlalchemy.exc import IntegrityError

###CONFIG###
users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/register', methods= ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.name.data, form.email.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                flash('Registration Success!', 'success')
                return redirect(url_for('plants.all'))
            except IntegrityError:
                db.session.rollback()
                flash('Email {} already exists'.format(form.email.data), 'error')
    return render_template('register.html', form=form)
