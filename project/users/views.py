from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from project.models import User
from .forms import RegisterForm, LoginForm
from project.extensions import db
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
                return redirect(url_for('users.login'))
            except IntegrityError:
                db.session.rollback()
                flash('Email {} already exists'.format(form.email.data), 'error')
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for logging in {}'.format(user.name.title()),'info')
                return redirect(url_for('plants.all'))
            else:
                flash('Invalid login credentials', 'error')
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated=False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('users.login'))
