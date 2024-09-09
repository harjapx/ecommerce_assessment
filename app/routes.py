from flask import request, jsonify
from app import db, app
from app.models import User, Product
import bcrypt
import jwt
from datetime import datetime, timedelta
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
    
    if user:
        print("Stored hashed password:", user.password)
        print("Provided password:", password)
    
    if user and bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()):
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
    # Query the database for products and their revenue
    products = db.session.query(
        Product.category, 
        (Product.price * Product.quantity_sold).label('total_revenue'),
        Product.product_name,
        Product.quantity_sold
    ).all()
    
    # Create a DataFrame from the retrieved data
    df = pd.DataFrame(products, columns=['category', 'total_revenue', 'product_name', 'quantity_sold'])

    # Handle the case where no products are found
    if df.empty:
        return jsonify({"message": "No products found in the database"}), 404

    # Calculate top product and quantity sold for each category
    top_products = df.loc[df.groupby('category')['quantity_sold'].idxmax()]
    summary_report = df.groupby('category').agg({
        'total_revenue': 'sum'
    }).reset_index().merge(top_products[['category', 'product_name', 'quantity_sold']], on='category')
    
    summary_report.rename(columns={
        'product_name': 'top_product',
        'quantity_sold': 'top_product_quantity_sold'
    }, inplace=True)
    
    # Save the summary report to CSV
    summary_report.to_csv('static/summary_report.csv', index=False)
    
    return jsonify({"message": "Summary report generated", "file": "/static/summary_report.csv"})

