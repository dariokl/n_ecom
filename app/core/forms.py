from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Email, EqualTo, DataRequired
from wtforms import ValidationError
from app.models import Order


class OrderForm(FlaskForm):
    submit = SubmitField("Naruci")

class RemoveForm(FlaskForm):
    name = StringField()
    submit = SubmitField('Remove')


class CheckoutForm(FlaskForm):
    name = StringField("Ime i Prezime", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    text = TextAreaField('Vise informacija o vasoj narudžbi')
    number = StringField('Broj telefona', validators=[DataRequired()])
    submit = SubmitField('Izvrši narudžbu')
