import pandas as pd
from app import app, db
from app.models import Product

# Load the data from CSV into a DataFrame
df = pd.read_csv('static/products.csv')

# Data cleaning and processing
df['price'].fillna(df['price'].median(), inplace=True)
df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Create the application context
with app.app_context():
    # Iterate over DataFrame rows and add to the database
    for _, row in df.iterrows():
        product = Product(
            product_id=row['product_id'],
            product_name=row['product_name'],
            category=row['category'],
            price=row['price'],
            quantity_sold=row['quantity_sold'],
            rating=row['rating'],
            review_count=row['review_count']
        )
        db.session.add(product)

    # Commit the changes to the database
    db.session.commit()

print("Data uploaded successfully.")
