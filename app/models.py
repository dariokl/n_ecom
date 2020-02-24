from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login_manager
from datetime import datetime





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#Users and review
class User(db.Model , UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=True)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.username}"

class Article(db.Model):

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    price = db.Column(db.Integer)
    filename = db.Column(db.String(128), unique=True)
    filename_two = db.Column(db.String(128), unique=True)
    filename_tree = db.Column(db.String(128), unique=True)


    def __repr__(self):
        return f"{self.name}"

    @property

    def url(self):

        return f'/static/images/{self.filename}'

    @property

    def filepath(self):
        if self.filename is None:
            return
        return f'static/images/{self.filename}'
    @property

    def url_two(self):

        return f'/static/images/{self.filename_two}'

    @property

    def filepath_two(self):
        if self.filename_two is None:
            return
        return f'static/images/{self.filename_two}'
    @property

    def url_tree(self):

        return f'/static/images/{self.filename_tree}'

    @property

    def filepath_tree(self):
        if self.filename_tree is None:
            return
        return f'static/images/{self.filename_tree}'


class Order(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_mail = db.Column(db.String)
    text = db.Column(db.Text)
    number = db.Column(db.String, nullable=False)
    product = db.Column(db.String)
    ammount = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, name, user_mail, product, ammount, text, number, total):
        self.name = name
        self.user_mail = user_mail
        self.product = product
        self.ammount = ammount
        self.text = text
        self.number = number
        self.total = total

    def __repr__(self):

        return f"{self.product}"

