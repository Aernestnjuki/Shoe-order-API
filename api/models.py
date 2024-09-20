from . import db
from _datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    PENDING = 'PENDING'
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.Integer(), nullable=False)
    admin = db.Column(db.Boolean, default=0)
    password_hash = db.Column(db.String(500), nullable=False)

    carts = db.relationship('Cart', backref=db.backref('user'))
    orders = db.relationship('Order', backref=db.backref('user'))

    created_at = db.Column(db.DateTime(), default=datetime.now())


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Staff {self.staff_name}>'


class Product(db.Model):
    __tablename__ = 'products'

    prod_id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(50), nullable=False, unique=True)
    size = db.Column(db.Integer(), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    prev_price = db.Column(db.Float(), nullable=False)
    supplier = db.Column(db.String(50), nullable=False, unique=True)
    picture = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)

    carts = db.relationship('Cart', backref=db.backref('product'))
    orders = db.relationship('Order', backref=db.backref('product'))

    created_at = db.Column(db.DateTime(), default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Product {self.product_name} selling at Ksh{self.price}>'


class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)

    user_link = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    product_link = db.Column(db.Integer(), db.ForeignKey('products.prod_id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Cart {self.cart_id}>'

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default='PENDING')

    user_link = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    product_link = db.Column(db.Integer(), db.ForeignKey('products.prod_id'))

    time_order_taken = db.Column(db.DateTime(), default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Order {self.order_id}>'