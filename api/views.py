from flask import request, jsonify, make_response
from http import HTTPStatus
from flask_restx import Resource, Namespace, fields
from .models import Product, Order
from flask_jwt_extended import jwt_required, get_jwt_identity

customer = Namespace('Customer', description='Customer Namespace')


customer_view_products = customer.model(
    'Admin get all products',
    {
        'product_id': fields.Integer(description='A product ID'),
        'product_name': fields.String(required=True, description='Product name'),
        'size': fields.Integer(required=True, dscription='Product size'),
        'color': fields.String(required=True, dscription='Product color'),
        'price': fields.Float(required=True, dscription='Product price'),
        'prev_price': fields.Float(required=True, dscription='Product previous price'),
        'supplier': fields.String(required=True, dscription='Product supplier name'),
        'picture': fields.String(required=True, dscription='Product picture'),
        'description': fields.String(required=True, dscription='Product description')
    }
)

order_model = customer.model(
    'Order_model',
    {
        'quantity': fields.Integer(required=True, dscription='Order quantity')
    }
)

all_order_model = customer.model(
    'All order model',
    {
        'id': fields.Integer(description='Order ID'),
        'quantity': fields.Integer(required=True, dscription='Order quantity'),
        'customer_link': fields.Integer(description='Customer ID'),
        'product_link': fields.Integer(description='Product ID')
    }
)

@customer.route('/products')
class CustomerOrderProducts(Resource):

    @customer.marshal_with(customer_view_products)
    @jwt_required()
    def get(self):
        """Customer get all products"""

        products = Product.query.all()

        return make_response(products, HTTPStatus.OK)




@customer.route('/order/<int:order_id>')
class GetCreateDeleteOrders(Resource):

    def get(self, order_id):
        """Get all ordered products"""
        pass

    @customer.expect(order_model)
    @customer.marshal_with(all_order_model)
    @jwt_required()
    def post(self, order_id):
        """Create an order"""
        current_user = get_jwt_identity()

        data = request.get_json()

        prod_id = Product.query.get(order_id)

        new_order = Order.query.filter_by(product_link=prod_id, customer_link=current_user).first()

        if new_order:
            return make_response(jsonify({'error': 'Order already exits!'}), HTTPStatus.BAD_REQUEST)

        else:
            new_order.quantity = data.get('quantity')


    def put(self, order_id):
        """Update one customer order by product ID"""
        pass

    def delete(self, order_id):
        """Delete an order"""


@customer.route('/order/<int:order_id>/customer/<int:cust_id>')
class SpecificCustomerOrders(Resource):

    def get(self, order_id, cust_id):
        """Get customer specific orders"""
        pass

@customer.route('/order/customer/<int:cust_id>')
class AllOrdersByCustomer(Resource):
    """Get all orders by a customer"""
    pass








