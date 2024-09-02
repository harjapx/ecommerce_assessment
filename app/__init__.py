from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URL, SECRET_KEY

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes after initializing app and db
from . import routes
