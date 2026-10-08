SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp AS purchased_at,
    order_approved_at AS approved_at,
    order_delivered_carrier_date AS delivered_to_carrier_at,
    order_delivered_customer_date AS delivered_to_customer_at,
    order_estimated_delivery_date AS estimated_delivery_at
FROM {{ source('bronze', 'raw_orders') }}