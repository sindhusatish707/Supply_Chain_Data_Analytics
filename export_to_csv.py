import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://admin:password123@127.0.0.1:5433/supply_chain_db')

print("Fetching data from cleaned_orders table...")
df_cleaned = pd.read_sql('SELECT * FROM cleaned_orders', engine)

output_path = 'data/cleaned_supply_chain.csv'
df_cleaned.to_csv(output_path, index=False)

print(f"Success! Data exported to {output_path}")
print(f"Total rows exported: {len(df_cleaned)}")