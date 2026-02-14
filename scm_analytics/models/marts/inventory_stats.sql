SELECT 
    category_name,
    AVG(days_for_shipping_real) as avg_actual_lead_time,
    STDDEV(days_for_shipping_real) as lead_time_volatility
FROM {{ source('main', 'cleaned_orders') }}
GROUP BY 1;