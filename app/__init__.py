import os
import json
import logging
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    
    app = Flask(__name__)
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'settings.json'))
    
    with open(config_path) as config_file:
        config = json.load(config_file)
        app.config['SECRET_KEY'] = config.get('SECRET_KEY')
        app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
        app.config['JWT_SECRET_KEY'] = config.get('JWT_SECRET_KEY')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
        
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.referral import referral_bp
    app.register_blueprint(referral_bp)
    
    swagger_ui = get_swaggerui_blueprint('/swagger', '/static/swagger.json')
    app.register_blueprint(swagger_ui)
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not Found'}), 404
    
    return app
