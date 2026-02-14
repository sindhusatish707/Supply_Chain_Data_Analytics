import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://admin:password123@localhost:5433/supply_chain_db')

df = pd.read_sql("select * from raw_orders", engine)

#remove spaces, parantheses and convert to lower case
df.columns = [col.lower().replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]

#handle null values and redundant columns
#from audit, delete columns that are >50% empty
cols_to_drop = ['order_zipcode', 'product_description']
df.drop(columns=cols_to_drop, inplace=True)


#some columnswith null values can be handled where
#Customer Lname can be filled with 'Unknown'
#Zipcode can be filled with 0
df['customer_lname'] = df['customer_lname'].fillna('Unknown')
df['customer_zipcode'] = df['customer_zipcode'].fillna(0)


#ensuring standard text patterns
text_cols = ['customer_country', 'customer_city', 'type', 'delivery_status', 'shipping_mode']
for col in text_cols:
    df[col] = df[col].str.strip().str.title()

#type casting
#errors='coerce' makes the empty row values NaT - Not a Time
date_cols = ['order_date_dateorders', 'shipping_date_dateorders']
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

numeric_cols = ['benefit_per_order', 'sales', 'order_item_discount', 'product_price']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

#converting days to integers to round off values like 2.5 shipping days
int_cols = ['days_for_shipping_real', 'days_for_shipment_scheduled']
df[int_cols] = df[int_cols].fillna(0).astype(int)

print("Cleaning Complete. New Columns: ", df.columns[:5].tolist())
print(df.dtypes)

# Save to a new table called 'cleaned_orders'
df.to_sql('cleaned_orders', engine, if_exists='replace', index=False)
print("Cleaned data successfully uploaded to 'cleaned_orders' table.")