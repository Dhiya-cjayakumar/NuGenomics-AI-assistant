from flask import Flask
from .routes import routes  
from dotenv import load_dotenv
import os
load_dotenv()
def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'default_dev_secret_key')
    app.register_blueprint(routes)  
    return app
