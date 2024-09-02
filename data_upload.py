import pandas as pd
from app.models import Product
from app import db
from app.utils import clean_data

# Load the CSV data
df = pd.read_csv('data/products.csv')

# Clean the data
df = clean_data(df)

# Upload to the database
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

db.session.commit()

print("Data uploaded successfully!")
