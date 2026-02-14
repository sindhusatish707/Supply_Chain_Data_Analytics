import pandas as pd 
from sqlalchemy import create_engine

#load raw data
df = pd.read_csv('./data/DataCoSupplyChainDataset.csv', encoding='ISO-8859-1')

#connecting to docker instance
engine = create_engine('postgresql://admin:password123@localhost:5433/supply_chain_db')

#create raw_orders table in sql and push data
df.to_sql('raw_orders', engine, if_exists='replace', index=False)

print('Data successfully loaded into POstgreSQL!')