from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from .views import healthcheck_blueprint, user_blueprint, category_blueprint, record_blueprint, currency_blueprint
from .db import db

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    api = Api(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(healthcheck_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(record_blueprint)
    app.register_blueprint(currency_blueprint)

    return app
