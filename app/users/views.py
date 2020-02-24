from app import db
from flask import render_template,  request, redirect, url_for, Blueprint, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.users.forms import RegistrationForm, LoginForm
from app.models import User

users = Blueprint('users', __name__)


@users.route('/register', methods=["GET", "POST"])
def register():

    form_r = RegistrationForm()
    form_l = LoginForm()

    if form_r.validate_on_submit():
        user = User(username=form_r.username.data,
                    email=form_r.email.data,
                    password=form_r.password.data)

        db.session.add(user)
        db.session.commit()


        return redirect(url_for('controla.index'))

    if form_l.validate_on_submit():
                user = User.query.filter_by(email=form_l.email_l.data).first()

                if user.check_password(password=form_l.password_l.data) and user is not None:

                    login_user(user)
                    flash('Log in success!')

                    next = request.args.get('next')

                    if next == None or not next[0] == '/':
                        next = url_for('controla.index')

                    return redirect(next)

    return render_template('register.html', form_r=form_r, form_l=form_l)




@users.route('/logout',methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('controla.index'))
