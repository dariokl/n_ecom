from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired
from wtforms import ValidationError
from app.models import User



class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired() ])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo(
        'pass_confirm', message="Password must match")])
    pass_confirm = PasswordField(
        "Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class LoginForm(FlaskForm):

    email_l = StringField("Email", validators=[DataRequired(), Email()])
    password_l = PasswordField('Password', validators=[DataRequired()])
    submit_l = SubmitField('Log In')
