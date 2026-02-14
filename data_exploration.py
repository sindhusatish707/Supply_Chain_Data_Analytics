import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://admin:password123@localhost:5433/supply_chain_db')

print("DESCRIPTIVE ANALYSIS")


# DESCRIPTIVE ANALYSIS-------------------------------------------------------------------------------------------------------------
#check which products are being delivered late and the avg lead time
late_delivery_query = """
SELECT 
    "Category Name",
    COUNT(*) as order_count,
    AVG("Days for shipping (real)") as avg_lead_time,
    AVG("Days for shipment (scheduled)") as avg_shipping_time
FROM raw_orders
WHERE "Delivery Status" = 'Late delivery'
GROUP BY 1
ORDER BY avg_lead_time DESC;
"""

df_late_deliveries = pd.read_sql(late_delivery_query, engine)
print("Assessing avg shipping days for late deliveries")
print(df_late_deliveries.head())
print("*" *30)


#check which products give maximum profit ordered by country
avg_profit_query = """
SELECT
    "Category Name",
    COUNT(*) as order_count,
    "Customer Country",
    AVG("Benefit per order") as avg_profit_per_order
FROM raw_orders
GROUP BY "Customer Country", "Category Name"
ORDER BY avg_profit_per_order DESC;
"""

df_avg_profit_by_country = pd.read_sql(avg_profit_query, engine)
print("Average profit made per customer country")
print(df_avg_profit_by_country.head())
print("*" *30)


#check which country makes most profit
best_profit_by_country_query = """
SELECT
    "Customer Country",
    AVG("Benefit per order") as avg_profit_per_order
FROM raw_orders
GROUP BY "Customer Country"
ORDER BY avg_profit_per_order DESC;
"""

df_best_profit_by_country = pd.read_sql(best_profit_by_country_query, engine)
print("Most profit made per customer country")
print(df_best_profit_by_country.head())
print("*" *30)


#check which product is sold the most
max_product_sale_query = """
SELECT
    "Category Name",
    COUNT(*) as order_number
FROM raw_orders
GROUP BY 1
ORDER BY order_number DESC;
"""

df_max_product_sale = pd.read_sql(max_product_sale_query, engine)

print("Most popular or in demand product category")
print(df_max_product_sale.head())
print("*" *30)

#check which state has most of the customers
max_customers_by_state_query = """
SELECT
    "Customer Country",
    "Customer City",
    COUNT(*) as orders_count_from_city
FROM raw_orders
GROUP BY 1, 2
ORDER BY orders_count_from_city DESC;
"""

df_max_customers_by_state = pd.read_sql(max_customers_by_state_query, engine)
print("Maximum number of orders grouped by customer country and city")
print(df_max_customers_by_state.head())
print("*" *30)

#order placed with respect to mode of payment
payment_modes_per_product_query = """
SELECT
    "Category Name",
    "Type",
    COUNT(*) as payment_mode_count
FROM raw_orders
GROUP BY "Category Name", "Type"
ORDER BY payment_mode_count DESC;
"""

df_payment_modes_per_product = pd.read_sql(payment_modes_per_product_query, engine)
print("Product category and corresponding payment method comparision")
print(df_payment_modes_per_product.head())
print("*" *30)

#order placed by customer segment
product_popularity_by_cust_segment_query = """
SELECT
    "Customer Segment",
    COUNT(*) as customers_per_segment_count,
    "Category Name"
FROM raw_orders
GROUP BY "Customer Segment", "Category Name"
ORDER BY customers_per_segment_count DESC;
"""

df_product_popularity_by_cust_segment = pd.read_sql(product_popularity_by_cust_segment_query, engine)
print("Which product does each customer segment order the most")
print(df_product_popularity_by_cust_segment.head())
print("*" *30)


print("STATISTICAL ANALYSIS")


#STATISTICAL ANALYSIS ----------------------------------------------------------------------------------------------------
#should give better comparision and whole picture than just counts and averages

#lead time variance
#high volatility indicates we need more safety stock as it takes longer to deliver and usually faces late delivery case
lead_time_var_query = """
SELECT
    "Category Name",
    AVG("Days for shipping (real)") as avg_actual,
    STDDEV("Days for shipping (real)") as lead_time_volatility,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY "Days for shipping (real)") as p95_lead_time
FROM raw_orders
GROUP BY 1
ORDER BY lead_time_volatility DESC;
"""

df_lead_time_var = pd.read_sql(lead_time_var_query, engine)
print("Lead time volatility grouped by product category")
print(df_lead_time_var.head())
print("*" *30)


#profitability
#a more significant indicator than average profit is to assess where the company is losing money
profitability_query = """
SELECT
    "Customer Country",
    COUNT(CASE WHEN "Benefit per order" < 0 THEN 1 END) as loss_making_orders,
    COUNT(*) as total_orders,
    (COUNT(CASE WHEN "Benefit per order" < 0 THEN 1 END):: float / COUNT(*)) * 100 as loss_rate_pct
FROM raw_orders
GROUP BY 1
HAVING COUNT(*) > 100
ORDER BY loss_rate_pct DESC;
"""

df_profitability = pd.read_sql(profitability_query, engine)
print("Which locations are costing the company the most loss")
print(df_profitability.head())
print("*" *30)


#most volume by product
most_volume_product_query = """
SELECT
    "Category Name",
    "Product Name",
    COUNT(CASE WHEN "Benefit per order" > 0 THEN 1 END) as profit_making_orders,
    COUNT(*) as product_order_count,
    (COUNT(CASE WHEN "Benefit per order" > 0 THEN 1 END):: float / COUNT(*)) * 100 as profit_rate_pct
FROM raw_orders
GROUP BY 1, 2
ORDER BY profit_rate_pct DESC;
"""

df_most_volume_product = pd.read_sql(most_volume_product_query, engine)
print("Profit creating products grouped by category")
print(df_most_volume_product.head())
print("*" *30)


#see which product drives the most value to indentify "Class A" items
#Pareto Principle (80/20 Rule) - 20% of products drive 80% of revenue
pareto_query = """
WITH product_sales AS (
    SELECT
        "Product Name",
        SUM("Sales") as total_product_sales
    FROM raw_orders
    GROUP BY 1
),
cumulative_sales AS (
    SELECT
        "Product Name",
        total_product_sales,
        SUM(total_product_sales) OVER (ORDER BY total_product_sales DESC) as running_total,
        SUM(total_product_sales) OVER () as grand_total
    FROM product_sales
)
SELECT
    "Product Name",
    total_product_sales,
    (running_total / grand_total) * 100 as cumulative_pct
FROM cumulative_sales
ORDER BY total_product_sales DESC;
"""

df_pareto = pd.read_sql(pareto_query, engine)
print("Pareto Principle")
# print(df_pareto[df_pareto["cumulative_pct"] > 80])
print(df_pareto.head())

