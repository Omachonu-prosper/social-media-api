from flask import Flask
from flask_cors import CORS
from api.user_auth import auth

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register app blueprints 
    app.register_blueprint(auth)

    return app
