import os
import json
import redis
import boto3
import flask_profiler as fp
from botocore.client import Config
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
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

def make_s3(app):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=app.config['S3_SECRET_KEY'],
        endpoint_url=app.config['S3_URL'],
        region_name=app.config['S3_REGION'],
        config = Config(s3={'payload_signing_enabled': False}, 
                        signature_version="s3")
    )
    
    return s3_client

def make_redis(app):
    rds = redis.Redis.from_url(
        app.config['REDIS_URL_CACHE'], 
        decode_responses=True)
    
    return rds


def create_app(test_mode=False):
    
    app = Flask(__name__)
    settings = 'settings_test' if test_mode else 'settings'
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{settings}.json'))
    
    with open(config_path) as config_file:
        config = json.load(config_file)
        app.config.update(config)
        
    setup_logging(test_mode)
    app.logger.info("Application starting up")
    
    fp.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    app.redis = make_redis(app)
    app.celery = make_celery(app)
    app.s3_client = make_s3(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.routes.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    from app.routes.referral import referral_bp
    app.register_blueprint(referral_bp, url_prefix='/referral')
    from app.routes.workout import workout_bp
    app.register_blueprint(workout_bp, url_prefix='/workout')
    
    swagger_ui = get_swaggerui_blueprint('/swagger', '/static/swagger.json')
    app.register_blueprint(swagger_ui)
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not Found'}), 404
    
    @app.errorhandler(Exception)
    def internal_server_error(error):
        app.logger.error(f'{error}')
        return jsonify({'message': f'Internal Server Error'}), 500
    
    return app
