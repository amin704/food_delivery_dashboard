import pandas as pd


df = pd.read_csv('Food Delivery Dataset.csv')

df = df.dropna(subset=['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude'])

df['Restaurant_latitude'] = pd.to_numeric(df['Restaurant_latitude'], errors='coerce')
df['Restaurant_longitude'] = pd.to_numeric(df['Restaurant_longitude'], errors='coerce')
df['Delivery_location_latitude'] = pd.to_numeric(df['Delivery_location_latitude'], errors='coerce')
df['Delivery_location_longitude'] = pd.to_numeric(df['Delivery_location_longitude'], errors='coerce')

df = df[
    (df['Restaurant_latitude'].between(0, 90)) &
    (df['Restaurant_longitude'].between(0, 180)) &
    (df['Delivery_location_latitude'].between(0, 90)) &
    (df['Delivery_location_longitude'].between(0, 180)) &
    (df['Restaurant_latitude'] != 0) &
    (df['Restaurant_longitude'] != 0) &
    (df['Delivery_location_latitude'] != 0) &
    (df['Delivery_location_longitude'] != 0)
]


df.to_csv('Cleaned_Food_Delivery_Dataset.csv', index=False)