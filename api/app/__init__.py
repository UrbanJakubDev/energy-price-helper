"""
This contains the application factory for creating flask application instances.
Using the application factory allows for the creation of flask applications configured 
for different environments based on the value of the CONFIG_TYPE environment variable
"""

import os
from flask import Flask
from flask_cors import CORS

from app.utils import mkdir_if_not
# from flask_mail import Mail

# ### Flask extension objects instantiation ###
# mail = Mail()


### Application Factory ###
def create_app(config_type=None):

    app = Flask(__name__)
    # CORS(app)

    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    # Inintialize DB
    initialize_db(app)

    # Register blueprints
    register_blueprints(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    # Check if api/UPLOADS folder exists, if not create it
    mkdir_if_not(app.config['TMP_FOLDER'])
    

    return app


### Initialize Database ###
def initialize_db(app):
    pass


### Helper Functions ###
def register_blueprints(app):

    # Import blueprints
    from app.main import main_blueprint
    from app.filehandle import file_blueprint

    # Register blueprints
    app.register_blueprint(main_blueprint, url_prefix="/api")
    app.register_blueprint(file_blueprint, url_prefix="/api")


def initialize_extensions(app):

    # Enable CORS for JS app
    CORS(app)


def register_error_handlers(app):
    from flask import make_response, jsonify

    def response(e):
        return jsonify({
            'message': e.description
        }), e.code


    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return response(e)

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return response(e)

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return response(e)

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return response(e)

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return response(e)


def configure_logging(app):
    import logging
    from flask.logging import default_handler
    from logging.handlers import RotatingFileHandler

    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler(
        'flaskapp.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)
