from flask import request, jsonify
from http import HTTPStatus
from flask_restx import Resource, Namespace, fields
from .models import Product, Order, Customer

customer = Namespace('Customer', description='Customer Namespace')


@customer.route('/order/products')
class CustomerOrderProducts(Resource):

    def get(self):
        """Customer get all products"""

        products