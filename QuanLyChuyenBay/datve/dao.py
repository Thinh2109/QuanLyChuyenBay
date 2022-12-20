import hashlib
import json
from flask_login import current_user
from datve import db
from datve.models import Category, Product, User, Receipt, ReceiptDetail
from sqlalchemy.sql import extract
from sqlalchemy import func


# Dấu thăng dùng để định nghĩa dấu tiếng việt
def read_json(path):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


def load_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, 'data/categories.json'))


def load_products(cate_id=None, kw=None, from_price=None, to_price=None):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if kw:
        products = products.filter(Product.to.contains(kw))

    if from_price:
        products = products.filter(Product.price.__eq__(from_price))

    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    return products.all()
    # products = read_json(os.path.join(app.root_path, 'data/products.json'))
    #
    # if cate_id:
    #     products = [p for p in products if p['category_id'] == int(cate_id)]
    #
    # if kw:
    #     products = [p for p in products if p['to'].lower().find(kw.lower()) >= 0]
    #
    # if from_price:
    #     products = [p for p in products if p['price'] >= float(from_price)]
    #
    # if to_price:
    #     products = [p for p in products if p['price'] <= float(to_price)]
    #
    # return products


def get_product_by_id(product_id):
    return Product.query.get(product_id)
    # products = read_json(os.path.join(app.root_path, 'data/products.json'))
    #
    # for p in products:
    #     if p['id'] == product_id:
    #         return p


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def add_user(name, username, password, number_phone, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                number_phone=number_phone.strip(),
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(receipt=receipt,
                              product_id=c['id'],
                              quantity=c['quantity'],
                              unit_price=c['price'])
            db.session.add(d)

        db.session.commit()


# def product_stats(kw=None, from_date=None, to_date=None):
#     p = db.session.query(Product.id, Product.to,
#                          func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price)) \
#         .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id), isouter=True) \
#         .group_by()
#     return p.all()

def product_month_stats(year):
    return db.session.query(extract('month', Receipt.created_date),
                            func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price)) \
        .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id)) \
        .filter(extract('year', Receipt.created_date) == year) \
        .group_by(extract('month', Receipt.created_date))\
        .order_by(extract('month', Receipt.created_date)).all()
