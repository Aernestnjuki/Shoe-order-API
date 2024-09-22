from flask import request
from http import HTTPStatus
from flask_restx import Resource, Namespace, fields
from .models import Product, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db

admin = Namespace('Admin', description='Staff admin Namespace')

all_users_model = admin.model(
    'Admin get all customers',
    {
        'user_id': fields.Integer(description='An ID'),
        'user_name': fields.String(required=True, description='A customer name'),
        'email': fields.String(required=True, description='An email'),
        'admin': fields.Integer(requires=True, description='If user is admin'),
        'phone': fields.Integer(required=True, description='A phone number')
    }
)

product_model = admin.model(
    'Products model',
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




@admin.route('/all-customers')
class GetAllCustomers(Resource):

    @admin.marshal_with(all_users_model)
    @jwt_required()
    def get(self):
        """Admin staff get all customers"""

        logged_user = get_jwt_identity()

        is_admin = User.query.filter_by(user_id=logged_user, admin=1).first()

        if is_admin.admin:
            customer = User.query.all()

            return customer, HTTPStatus.OK

        return {"error": "Not Allowed"}, HTTPStatus.BAD_REQUEST


@admin.route('/products')
class GetCreateProducts(Resource):

    @admin.marshal_with(product_model)
    @jwt_required()
    def get(self):
        """Admin staff get all products"""


        products = Product.query.all()

        return products, HTTPStatus.OK


    @admin.expect(product_model)
    @admin.marshal_with(product_model)
    @jwt_required()
    def post(self):
        """Admin staff Post a product"""

        data = request.get_json()

        new_product = Product(
            product_name = data.get('product_name'),
            size = data.get('size'),
            color = data.get('color'),
            price = data.get('price'),
            prev_price = data.get('prev_price'),
            supplier = data.get('supplier'),
            picture = data.get('picture'),
            description = data.get('description')
        )

        new_product.save()

        return new_product, HTTPStatus.CREATED

@admin.route('/update/product/<int:product_id>')
class GetUpdateDelete(Resource):

    @admin.marshal_with(product_model)
    @jwt_required()
    def get(self, product_id):
        """Admin get a product by ID"""
        p_id = Product.query.get_or_404(product_id)

        return p_id, HTTPStatus.OK


    @admin.expect(product_model)
    @admin.marshal_with(product_model)
    @jwt_required()
    def put(self, product_id):
        """Admin Update product by ID"""

        data = request.get_json()

        product_to_update = Product.query.get_or_404(product_id)

        product_to_update.product_name = data.get('product_name')
        product_to_update.size = data.get('size')
        product_to_update.color = data.get('color')
        product_to_update.price = data.get('price')
        product_to_update.prev_price = data.get('prev_price')
        product_to_update.supplier = data.get('supplier')
        product_to_update.picture = data.get('picture')
        product_to_update.description = data.get('description')

        db.session.commit()

        return product_to_update, HTTPStatus.OK


    @admin.marshal_with(product_model)
    @jwt_required()
    def delete(self, product_id):
        """Admin Delete product by ID"""

        product_to_delete = Product.query.get_or_404(product_id)

        product_to_delete.delete()

        return product_to_delete, HTTPStatus.NO_CONTENT