import os
import os.path as op
from app import db, image_path
from flask import render_template, Blueprint, redirect, url_for, abort, request, flash
from app.models import User, Article, Order
from app.core.forms import OrderForm, RemoveForm, CheckoutForm
from flask import session


controla = Blueprint('controla', __name__)


@controla.route('/')
def index():

    return render_template('index.html')

@controla.route('/shop')
def shop():

    stolovi = db.session.query(Article).all()

    return render_template('shop.html', stolovi=stolovi )

@controla.route('/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    """Creating flask session 'cart' to add the each product a customer picks from shop, its pretty simple condition block
    if there is no cart its simply creates one and appends the first item clicked if there is one with the same name, it just
    adds +1 on the quantity and finally if customer order totally different product it appends it to session."""

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
    """Check out function that does all the calculations and prepares the order to be inserted in db table, i guess this
    could have been a little bit prettier , i will have to improve this . But the imporant thing for me is that it works !"""

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

    if 'cart' not in session:
        return '<h1> Korpa je prazna </h1>'
    else:
        items = session['cart']

    form = RemoveForm()

    #Jquery / ajax work to remove the item from the cart if user clicks the remove button.
    session['layout'] = request.args.get('layout')

    id_remove = session['layout']

    if id_remove:
        id_remove = int(id_remove)
        for d in items:
            if id_remove == d['id']:
                items.remove(d)


    return render_template('cart.html', items=items, form=form)