from datve import app, login
from flask import render_template, request, redirect, url_for, session, jsonify
import dao
from flask_login import login_user, current_user, logout_user, login_required
from datve.admin import *


@app.route("/")
def home():
    cates = dao.load_categories()

    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(cate_id=cate_id, kw=kw)

    return render_template('index.html', categories=cates, products=products)


@app.route("/products")
def product_list():
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    products = dao.load_products(cate_id=cate_id,
                                 kw=kw,
                                 from_price=from_price,
                                 to_price=to_price)

    return render_template('products.html', products=products)


@app.route("/products/<int:product_id>")
def detail(product_id):
    product = dao.get_product_by_id(product_id)

    return render_template('detail.html', product=product)


# @app.route("/login", methods='post')
# def login():
#     un = request.form['username']
#     pa = request.form['password']
#
#     if un == 'admin' and pa == '123':
#         return "Đăng nhập thành công"
#
#     return "Đăng nhập thất bại

@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.check_login(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        number_phone = request.form.get('number_phone')
        email = request.form.get('email')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                dao.add_user(name=name, username=username, password=password, number_phone=number_phone, email=email)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mật khẩu không khớp!'
        except Exception as ex:
            err_msg = 'Hệ thống gặp lỗi' + str(ex)

    cates = dao.load_categories()
    return render_template('register.html', err_msg=err_msg, categories=cates)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = 'Username Hoặc mật khẩu không chính xác!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route('/cart')
def cart():
    return render_template('cart.html', stats=dao.count_cart(session.get('cart')))


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    place = data.get('place')
    to = data.get('to')
    price = data.get('price')
    category = data.get('category')

    # import pdb
    # pdb.set_trace()

    cart = session.get('cart')
    if not cart:
        cart = {}

    # key = app.config['CART_KEY']  # 'cart'
    # cart = session[key] if key in session else {}
    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        place = data['place']
        to = data['to']
        price = data['price']

        cart[id] = {
            "id": id,
            "place": place,
            "to": to,
            "price": price,
            "category": category,
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(dao.count_cart(cart))


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        dao.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart

    return jsonify(dao.count_cart(cart))


@app.route('/api/delete-cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        del cart[product_id]
        session['cart'] = cart

    return jsonify(dao.count_cart(cart))


@app.context_processor
def common_response():
    return {
        'categories': dao.load_categories(),
        'cart_stats': dao.count_cart(session.get('cart'))
    }


if __name__ == '__main__':
    app.run(debug=True)
