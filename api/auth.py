from flask_restx import Namespace, fields, Resource
from flask import request, jsonify
from .models import User
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import make_response
from email_validator import validate_email, EmailNotValidError

auth = Namespace('Auth', description='Auth Namespace')

staff_signup_model = auth.model(
    'Staff Signup Model',
    {
        'staff_name': fields.String(required=True, description='Enter staff name'),
        'email': fields.String(required=True, description='Enter email'),
        'phone': fields.Integer(required=True, description='Enter phone number'),
        'password': fields.String(required=True, description='Enter password')
    }
)


staff_login_model = auth.model(
    'Staff Login Model',
    {
        "email": fields.String(required=True, description='Enter Email'),
        "password": fields.String(required=True, description='Enter password')
    }
)

customer_signup_model = auth.model(
    'Customer Signup Model',
    {
        'customer_name': fields.String(required=True, description='Enter customer name'),
        'email': fields.String(required=True, description='Enter email'),
        'phone': fields.Integer(required=True, description='Enter phone number'),
        'password': fields.String(required=True, description='Enter password')
    }
)

customer_login_model = auth.model(
    "Customer Login Model",
    {
        'email': fields.String(required=True, description='Enter email'),
        'password': fields.String(required=True, description='Enter password')
    }
)

@auth.route('/staff/signup')
class StaffSignUp(Resource):

    @auth.expect(staff_signup_model)
    def post(self):
        """Staff SignUp"""
        data = request.get_json()

        staff_name = User.query.filter_by(staff_name=data.get('staff_name')).first()
        email = User.query.filter_by(email=data.get('email')).first()

        if staff_name:
            return make_response(jsonify({'error': f'Staff name: {data.get("staff_name")} already exists!'}), HTTPStatus.NOT_FOUND)

        if email:
            return make_response(jsonify({'error': f'Email: {data.get("email")} already exists!'}), HTTPStatus.NOT_FOUND)

        try:
            validate_email(data.get('email'))

        except EmailNotValidError as e:
            return make_response(jsonify({'error': str(e)}), HTTPStatus.UNPROCESSABLE_ENTITY)

        if len(data.get('password')) < 6:
            return make_response(jsonify({'error': 'Your password is too short!'}), HTTPStatus.PRECONDITION_FAILED)

        staff = User(
            staff_name=data.get('staff_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            password_hash=generate_password_hash(data.get('password'))
        )

        staff.save()

        return make_response(jsonify({'message': 'Staff registered successfully'}), HTTPStatus.CREATED)


@auth.route('/staff/login')
class StaffLogin(Resource):

    @auth.expect(staff_login_model)
    def post(self):
        """Staff Login"""
        email = request.json['email']
        password = request.json['password']

        staff = User.query.filter_by(email=email).first()

        if staff and check_password_hash(staff.password_hash, password):
            access_token = create_access_token(identity=staff.staff_id)
            refresh_token = create_refresh_token(identity=staff.staff_id)

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "email": staff.email,
                "staff_name": staff.staff_name
            }

            return response, HTTPStatus.OK
        return make_response(jsonify({'error': 'Invalid email or Password'}), HTTPStatus.BAD_REQUEST)


@auth.route('/customer/signup')
class CustomerSignUp(Resource):

    @auth.expect(customer_signup_model)
    def post(self):
        """Customer Signup"""

        data = request.get_json()

        customer_name = User.query.filter_by(customer_name=data.get('customer_name')).first()
        email = User.query.filter_by(email=data.get('email')).first()

        if customer_name:
            return make_response(jsonify({'error': f'Customer name {data.get("customer_name")} already exists!'}), HTTPStatus.BAD_REQUEST)

        if email:
            return make_response(jsonify({'error': f'email: {data.get("email")} already exists!'}), HTTPStatus.BAD_REQUEST)

        try:
            email_is_valid = validate_email(data.get('email'))

        except EmailNotValidError as e:
            return make_response(jsonify({'error': str(e)}), HTTPStatus.UNPROCESSABLE_ENTITY)

        customer = User(
            customer_name = data.get('customer_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            password_hash=generate_password_hash(data.get('password'))
        )

        customer.save()

        return make_response(jsonify({'message': 'You have been registered successfully!'}), HTTPStatus.CREATED)


@auth.route('/customer/login')
class CustomerLogin(Resource):

    @auth.expect(customer_login_model)
    def post(self):
        """Customer Login"""

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        customer = User.query.filter_by(email=email).first()

        if customer and check_password_hash(customer.password_hash, password):
            access_token = create_access_token(identity=customer.cust_id)
            refresh_token = create_refresh_token(identity=customer.cust_id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'email': customer.email,
                'customer_name': customer.customer_name
            }

            return make_response(jsonify({'message': response}), HTTPStatus.OK)

        return make_response(jsonify({'error': 'Incorrect email or password! Try again!'}), HTTPStatus.BAD_REQUEST)

