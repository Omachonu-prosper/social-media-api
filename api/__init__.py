from flask import Flask
from flask_cors import CORS
from api.user_auth import auth

import api.error_handler as error

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register app blueprints
    app.register_blueprint(auth)

    # Register error handlers
    app.register_error_handler(400, error.bad_request)
    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.unauthorised)
    app.register_error_handler(405, error.method_not_allowed)
    app.register_error_handler(500, error.server_error)

    return app
