SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix AS customer_zip_prefix,
    customer_city,
    customer_state
FROM {{ source('bronze', 'raw_customers') }}
