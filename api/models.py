from . import db
from _datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    PENDING = 'PENDING'
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'

class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer(), primary_key=True)
    staff_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.Integer(), nullable=False)
    admin = db.Column(db.Boolean, default=0)
    password_hash = db.Column(db.String(500), nullable=False)

    staff_sales_orders = db.relationship('Order', backref=db.backref('staff'))


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Staff {self.staff_name}>'

class Customer(db.Model):
    __tablename__ = 'customers'

    cust_id = db.Column(db.Integer(), primary_key=True)
    customer_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.Integer(), nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)

    customer_orders = db.relationship('Order', backref=db.backref('customer'))


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Customer {self.customer_name}>'

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(50), nullable=False, unique=True)
    size = db.Column(db.Integer(), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    prev_price = db.Column(db.Float(), nullable=False)
    supplier = db.Column(db.String(50), nullable=False, unique=True)
    picture = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)

    product_ordered = db.relationship('Order', backref=db.backref('product'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Product {self.product_name} selling at Ksh{self.price}>'

# you have to create a cart table

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default='PENDING') # default='PENDING'

    customer_link = db.Column(db.Integer(), db.ForeignKey('customers.cust_id'))
    staff_link = db.Column(db.Integer(), db.ForeignKey('staff.staff_id'))
    product_link = db.Column(db.Integer(), db.ForeignKey('products.product_id'))

    time_order_taken = db.Column(db.DateTime(), default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Order {self.order_id}>'