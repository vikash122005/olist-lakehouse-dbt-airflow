SELECT
    product_category_name,
    product_category_name_english AS category_name_english
FROM {{ source('bronze', 'raw_category_translation')}}