import pandas as pd

def clean_data(df):
    df['price'].fillna(df['price'].median(), inplace=True)
    df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)

    df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))

    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    return df
