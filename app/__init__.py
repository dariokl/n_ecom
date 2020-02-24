
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

from  config import *
from werkzeug.routing import BaseConverter





#  General app set up
app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY']= SECRET_KEY


#Setting up RegexConverter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).init(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter


# Setting up psotgresql from config.py
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TRACK_MODIFICATIONS

#DataBase
db = SQLAlchemy(app)


#Admin
admin = Admin(app)
#Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

#Blueprints
from app.core.views import controla
from app.users.views import users
from app.viewadmin.views import admin_core

app.register_blueprint(controla)
app.register_blueprint(users)
app.register_blueprint(admin_core)
###

