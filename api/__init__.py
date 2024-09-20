from flask import Flask
from flask_restx import Api
from .config import config_dict
from .utils import db
from .models import User, Product, Order, Cart
from flask_jwt_extended import JWTManager



def create_app(configuration=config_dict['Dev']):
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)

    JWTManager(app)

    api = Api(app, title='Shoe Order API', description='These Api handle shoe orders and deliveries')

    from .auth import auth
    from .admin import admin
    from .views import customer

    api.add_namespace(auth, path='/auth')
    api.add_namespace(admin, path='/admin')
    api.add_namespace(customer, path='/customer')


    @app.shell_context_processor
    def make_shell_processor():
        return {
            'db': db,
            'user': User,
            'product': Product,
            'cart': Cart,
            'order': Order
        }



    return app