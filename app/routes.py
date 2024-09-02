from flask import request, jsonify
from . import app, db
from .models import User
import bcrypt, jwt
from datetime import datetime, timedelta
from .models import Product
import pandas as pd

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, 
            app.config['SECRET_KEY'], 
            algorithm="HS256"
        )
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
@app.route('/summary', methods=['GET'])
def summary():
    products = db.session.query(Product.category, 
                                (Product.price * Product.quantity_sold).label('total_revenue'),
                                Product.product_name,
                                Product.quantity_sold).all()
    
    df = pd.DataFrame(products, columns=['category', 'total_revenue', 'product_name', 'quantity_sold'])
    
    df['top_product'] = df.groupby('category')['quantity_sold'].idxmax().apply(lambda x: df['product_name'][x])
    df['top_product_quantity_sold'] = df.groupby('category')['quantity_sold'].transform('max')

    summary_report = df.groupby('category').agg({
        'total_revenue': 'sum',
        'top_product': 'first',
        'top_product_quantity_sold': 'first'
    })

    summary_report.to_csv('static/summary_report.csv', index=False)
    
    return jsonify({"message": "Summary report generated", "file": "/static/summary_report.csv"})
