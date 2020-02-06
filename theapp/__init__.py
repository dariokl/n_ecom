import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class


app = Flask(__name__)


app.config['SECRET_KEY'] = 'aje'


# Data base setup

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
admin = Admin(app)

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

#Uploads
image_path = op.join(op.dirname(__file__), "static/images")


#blueprints

from theapp.adminview.views import controla
from theapp.users.views import users

app.register_blueprint(controla)
app.register_blueprint(users)