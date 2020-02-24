import os
import os.path as op
from app import admin, db
from config import image_path
from flask import render_template, Blueprint, redirect, url_for, abort, request, flash
from app.models import User, Article, Order
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import Markup
from flask_admin import form, BaseView, expose, AdminIndexView, Admin
from sqlalchemy import event

admin_core = Blueprint('admin_core', __name__)

# ADMIN VIEWS
class AdminView(ModelView):
    """ Defining an admin role for one single user ,
    this web app will be used by one person so i didnt see a point of making
    more roles beside the admin role that will have access to all models in DB."""
    def is_accessible(self):

        if current_user.is_anonymous:
            return abort(403)

        elif current_user.is_admin:
            return current_user.is_authenticated

        else:
            return abort(403)




class MultiImage(AdminView):
    """Overriding the custom view and adding file upload forms , since the admin would need an ability to add new
    products to his web site , i didnt find enough material on this topic so i created 3 individual fields , i guess
    this will require changes in future."""

    def _list_thumbnail(view, context, model, name):
        if not model.filename:
            return ''

        elif not model.filename_two:
            return ''

        elif not model.filename_tree:
            return ''

        return Markup(
            '<img src="{model.url}" style="width: 150px;"><img src="{model.url_two}" style="width: 150px;"><img src="{model.url_tree}" style="width: 150px;">'.format(model=model)

        )

    form_extra_fields = {
            'filename': form.ImageUploadField(
            'image',
            base_path = image_path,
            url_relative_path = 'app/static/images',
            ),

            'filename_two': form.ImageUploadField(
            'image_two',
            base_path = image_path,
            url_relative_path = 'app/static/images',
            ),

            'filename_tree': form.ImageUploadField(
            'image_tree',
            base_path = image_path,
            url_relative_path = 'app/static/images',
            ),

        }

    column_list = [
            'image', 'name', 'filename', 'price',
        ]

    column_formatters = {
            'image': _list_thumbnail
        }


    @event.listens_for(Article, 'after_delete')
    def del_image(mapper, connection, target):
        if target.filename is not None:
                try:
                    os.remove(op.join(image_path, target.filename))
                    os.remove(op.join(image_path, target.filename_two))
                    os.remove(op.join(image_path, target.filename_tree))
                except OSError or TypeError:
                    pass


admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Order, db.session))
admin.add_view(MultiImage(Article, db.session))
