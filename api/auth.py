from flask_restx import Namespace, fields, Resource
from flask import request, jsonify
from .models import User
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import make_response
from email_validator import validate_email, EmailNotValidError

auth = Namespace('Auth', description='Auth Namespace')

user_signup_model = auth.model(
    'User Signup Model',
    {
        'user_name': fields.String(required=True, description='Enter username'),
        'email': fields.String(required=True, description='Enter email'),
        'phone': fields.Integer(required=True, description='Enter phone number'),
        'admin': fields.Integer(required=True),
        'password': fields.String(required=True, description='Enter password')
    }
)


user_login_model = auth.model(
    'User Login Model',
    {
        "email": fields.String(required=True, description='Enter Email'),
        "password": fields.String(required=True, description='Enter password')
    }
)



@auth.route('/user/signup')
class UserSignUp(Resource):

    @auth.expect(user_signup_model)
    def post(self):
        """User SignUp"""
        data = request.get_json()

        user_name = User.query.filter_by(user_name=data.get('user_name')).first()
        email = User.query.filter_by(email=data.get('email')).first()

        if user_name:
            return make_response(jsonify({'error': f'User name: {data.get("user_name")} already exists!'}), HTTPStatus.NOT_FOUND)

        if email:
            return make_response(jsonify({'error': f'Email: {data.get("email")} already exists!'}), HTTPStatus.NOT_FOUND)

        try:
            validate_email(data.get('email'))

        except EmailNotValidError as e:
            return make_response(jsonify({'error': str(e)}), HTTPStatus.UNPROCESSABLE_ENTITY)

        if len(data.get('password')) < 6:
            return make_response(jsonify({'error': 'Your password is too short!'}), HTTPStatus.PRECONDITION_FAILED)

        user = User(
            user_name=data.get('user_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            admin=data.get('admin'),
            password_hash=generate_password_hash(data.get('password'))
        )

        user.save()

        return make_response(jsonify({'message': 'User registered successfully'}), HTTPStatus.CREATED)


@auth.route('/user/login')
class UserLogin(Resource):

    @auth.expect(user_login_model)
    def post(self):
        """User Login"""
        email = request.json['email']
        password = request.json['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "email": user.email,
                "staff_name": user.user_name
            }

            return response, HTTPStatus.OK
        return make_response(jsonify({'error': 'Invalid email or Password'}), HTTPStatus.BAD_REQUEST)


@auth.route('/refresh-token')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        """Updating the access-token with the refresh-token"""

        user_id = get_jwt_identity()

        new_access_token = create_access_token(identity=user_id)

        return jsonify({'access-token': new_access_token}), HTTPStatus.OK
