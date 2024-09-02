from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URL, SECRET_KEY
from . import routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)