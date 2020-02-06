import os
import os.path as op
from theapp import db, image_path
from flask import render_template, Blueprint, redirect, url_for, abort, request, flash
from theapp.models import User, Article, Order
from theapp import admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import Markup
from flask_admin import form
from sqlalchemy import event
from theapp.adminview.forms import OrderForm, RemoveForm, CheckoutForm
from flask import session


controla = Blueprint('controla', __name__)


@controla.route('/')
def index():

    stolovi = db.session.query(Article).all()

    return render_template('index.html', stolovi=stolovi, sum=sum)


@controla.route('/shop')
def shop():

    stolovi = db.session.query(Article).all()



    return render_template('shop.html', stolovi=stolovi)




@controla.route('/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):

    form = OrderForm()

    product = Article.query.get_or_404(product_id)

    total = 1
    if form.validate_on_submit():
        if "cart" not in session:
            session["cart"] = []
            session["cart"].append({'name': product.name, 'price': product.price,
                                    'q': total, 'img': product.filename, 'id': product.id})

        elif product.name in [d['name'] for d in session['cart']]:
            for d in session['cart']:
                if d['name'] == product.name:
                    d['q'] += 1
                    d['price'] = d['q'] * d['price']

        else:
            session["cart"].append({'name': product.name, 'price': product.price,
                                    'q': total, 'img': product.filename, 'id': product.id})

        flash("Successfully added to cart!")


    return render_template('one.html', product=product, form=form)



@controla.route('/checkout', methods=["GET", "POST"])
def check_out():

    items = session['cart']
    form = CheckoutForm()

    product=[d['name'] for d in items]
    ammount=[str(d['q']) for d in items]
    total = [d['price'] for d in items]

    print(''.join(product))

    sum=0
    for i in range(len(total)):
        sum += total[i]

    print(sum)


    if form.validate_on_submit():

        order = Order(
        name=form.name.data,
        user_mail=form.email.data,
        text=form.text.data,
        number=form.number.data,
        product=' '.join(product),
        ammount='-'.join(ammount),
        total=sum
        )

        db.session.add(order)
        db.session.commit()
        session.clear()

        return redirect(url_for('controla.index'))




    return render_template('checkout.html',items=items, form=form)


@controla.route('/cart', methods=['GET', 'POST'])
def cart():

    form = RemoveForm()
    items = session['cart']

    session['layout'] = request.args.get('layout')

    id_remove = session['layout']

    if id_remove:
        id_remove = int(id_remove)
        for d in items:
            if id_remove == d['id']:
                items.remove(d)






    return render_template('cart.html', items=items, form=form)
# ADMIN VIEWS

class MyViewAdmin(ModelView):
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




class MultiImage(MyViewAdmin):

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
            url_relative_path = 'theapp/static/images',
            ),

            'filename_two': form.ImageUploadField(
            'image_two',
            base_path = image_path,
            url_relative_path = 'theapp/static/images',
            ),

            'filename_tree': form.ImageUploadField(
            'image_tree',
            base_path = image_path,
            url_relative_path = 'theapp/static/images',
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


admin.add_view(MyViewAdmin(User, db.session))
admin.add_view(MultiImage(Article, db.session))
admin.add_view(MyViewAdmin(Order, db.session))
