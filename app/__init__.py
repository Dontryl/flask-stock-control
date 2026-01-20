from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize the database
db = SQLAlchemy()

# Create the Flask application
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
# Initialize the database with the app
    db.init_app(app)
# Import and register routes
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app