import pandas as pd
from sqlalchemy import create_engine
import os

# 1. SETUP CREDENTIALS
# Replace with your actual filename. DO NOT put this on GitHub!
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/big_query_key.json"

# 2. CONNECT TO LOCAL POSTGRES (SILVER LAYER)
pg_engine = create_engine('postgresql://admin:password123@127.0.0.1:5433/supply_chain_db')

# 3. FETCH DATA
print("Reading cleaned data from Postgres...")
df = pd.read_sql('SELECT * FROM cleaned_orders', pg_engine)

# 4. DEFINE BIGQUERY SETTINGS (GOLD LAYER)
project_id = 'supplychainanalytics-486808'  # Your Project ID
table_id = 'scm_data.cleaned_orders' # DatasetID.TableName

# 5. UPLOAD TO CLOUD
print(f"Uploading {len(df)} rows to BigQuery...")
try:
    df.to_gbq(
        destination_table=table_id,
        project_id=project_id,
        if_exists='replace',
        progress_bar=True
    )
    print("Cloud Upload Successful! 🚀")
except Exception as e:
    print(f"Cloud Upload Failed: {e}")