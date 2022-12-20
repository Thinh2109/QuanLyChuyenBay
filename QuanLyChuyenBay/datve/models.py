from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datve import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    number_phone = Column(String(20), nullable=False)
    email = Column(String(100))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'

    place = Column(String(50))
    to = Column(String(50))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_time = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_detail = relationship('ReceiptDetail', backref='product', lazy=True)

    def __str__(self):
        return self.to


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #
        # c1 = Category(name='Hạng 1')
        # c2 = Category(name='Hạng 2')
        #
        # db.session.add(c1)
        # db.session.add(c2)
        #
        # db.session.commit()
        #
        # products = [{
        #     "id": 1,
        #     "place": "Đà Lạt",
        #     "to": "Hồ Chí Minh",
        #     "price": 350000,
        #     "image": "images/hcm.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 2,
        #     "place": "Đà Nẵng",
        #     "to": "Nha Trang",
        #     "price": 570000,
        #     "image": "images/nhatrang.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 3,
        #     "place": "Bà Rịa-Vũng Tàu",
        #     "to": "Hà Nội",
        #     "price": 570000,
        #     "image": "images/hanoi.jpg",
        #     "category_id": 2
        # }, {
        #     "id": 4,
        #     "place": "Hà Nội",
        #     "to": "Phú Quốc",
        #     "price": 800000,
        #     "image": "images/phuquoc.jpg",
        #     "category_id": 1
        # }]
        #
        # for p in products:
        #     pro = Product(place=p['place'], to=p['to'], price=p['price'], image=p['image'],
        #                   category_id=p['category_id'])
        #     db.session.add(pro)
        #
        # db.session.commit()
