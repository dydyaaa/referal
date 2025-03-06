import os
import json
import redis
from celery import Celery
from logging_config import setup_logging
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['REDIS_URL_BROKER'],
        broker=app.config['REDIS_URL_BROKER']
    )

    celery.conf.update(app.config)
    return celery

def create_app(test_mode=False):
    
    app = Flask(__name__)
    settings = 'settings_test' if test_mode else 'settings'
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{settings}.json'))
    
    with open(config_path) as config_file:
        config = json.load(config_file)
        app.config.update(config)
        
    setup_logging(test_mode)
    app.logger.info("Application starting up")
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    
    app.redis = redis.Redis.from_url(app.config['REDIS_URL_CACHE'], decode_responses=True)
    app.celery = make_celery(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.routes.referral import referral_bp
    app.register_blueprint(referral_bp, url_prefix='/referral')
    
    swagger_ui = get_swaggerui_blueprint('/swagger', '/static/swagger.json')
    app.register_blueprint(swagger_ui)
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not Found'}), 404
    
    return app

app = create_app()
celery = app.celery