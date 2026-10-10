SELECT
    seller_id,
    seller_zip_code_prefix AS seller_zip_prefix,
    seller_city,
    seller_state
FROM {{ source('bronze', 'raw_sellers') }}