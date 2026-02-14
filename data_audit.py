import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
from sqlalchemy import create_engine


engine = create_engine('postgresql://admin:password123@localhost:5433/supply_chain_db')

df = pd.read_sql("select * from raw_orders", engine)

print(f"Total Rows: {len(df)}")
print(f"Duplicate Rows: {df.duplicated().sum()}")
print("\nMissing values per column")
print(df.isnull().sum()[df.isnull().sum() > 0])  #only columns where null values are present

cols_to_check = ['Customer Country', 'Customer City', 'Type', 'Delivery Status', 'Shipping Mode']

for col in cols_to_check:
    print(f"Unique values in {col}")
    print(df[col].value_counts().head(10))

    if df[col].dtype == 'object':
        unique_lower = df[col].str.lower().str.strip().nunique()
        unique_actual = df[col].nunique()
        if unique_lower != unique_actual:
            print(f"Warning!! {col} has case or spacing mismatch")

sns.set_theme(style='whitegrid')

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.histplot(df['Days for shipping (real)'], bins=20, kde=True, ax=axes[0], color='skyblue')
axes[0].set_title('Distribution of Actual Shipping Days')

sns.histplot(df['Benefit per order'], bins=50, kde=True, ax=axes[1], color='salmon')
axes[1].set_title('Distribution of Profit (Identify Loss Making Outliers)')

plt.savefig('product_shipping_and_profit_distribution.png')
plt.tight_layout()
plt.show()


'''
Histogram Breakdown
1.Distribution of Actual Shipping Days (Blue):

    The Multi-Modal Peak: Notice how the data isn't a smooth curve but has distinct spikes at days 2, 3, 4, 5, and 6. 
    This suggests that the logistics system operates on discrete daily cycles.

    The 2-Day Surge: The massive spike at 2 days indicates that the majority of your supply chain is optimized for a 48-hour turnaround, 
    but there is significant "tail" (orders taking 4-6 days) that likely causes your high Late Delivery count (98,977 orders!).

2.Distribution of Profit (Red):

    The "Long Tail" of Loss: Most orders hover around the $0 to $200 profit mark (the central peak).

    Negative Outliers: You have orders plummeting toward -$4,000. These are your "Revenue Bleeders." 
    In a supply chain context, these are usually caused by 
        heavy item returns, 
        expedited shipping costs on low-margin items, or 
        massive discounts.
'''

plt.figure(figsize=(10, 6))
sns.histplot(df['Benefit per order'], bins=100, kde=True, color='salmon')
plt.xlim(-1000, 500)
plt.title('Zoomed-in Profit Distribution (Focusing on Loss-Making Orders)')
plt.xlabel('Benefit per order ($)')

plt.savefig('zoomed_profit_distribution.png')
plt.show()
