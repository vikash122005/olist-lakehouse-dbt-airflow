--The observations raw_orders

--Status counts as per Order status
con.sql("SELECT order_status,COUNT(*) FROM silver.orders GROUP BY order_status")

┌──────────────┬──────────────┐
│ order_status │ count_star() │
│   varchar    │    int64     │
├──────────────┼──────────────┤
│ delivered    │        96478 │
│ unavailable  │          609 │
│ invoiced     │          314 │
│ processing   │          301 │
│ approved     │            2 │
│ canceled     │          625 │
│ created      │            5 │
│ shipped      │         1107 │
└──────────────┴──────────────┘

--Nulls count in delivered_to_customer_at as per Order status
con.sql("SELECT order_status,COUNT(*) FROM silver.orders WHERE delivered_to_customer_at IS NULL GROUP BY order_status")

┌──────────────┬──────────────┐
│ order_status │ count_star() │
│   varchar    │    int64     │
├──────────────┼──────────────┤
│ created      │            5 │
│ delivered    │            8 │
│ invoiced     │          314 │
│ processing   │          301 │
│ shipped      │         1107 │
│ approved     │            2 │
│ unavailable  │          609 │
│ canceled     │          619 │
└──────────────┴──────────────┘

--Impossible dates: count rows where delivered_to_customer_at < purchased_at
con.sql("SELECT COUNT(*) FROM silver.orders WHERE delivered_to_customer_at < purchased_at")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            0 │
└──────────────┘

I found 8 delivered orders with no delivery date. I kept them in Silver so no data is lost, documented them, and added a test so it’s caught on every run

----------------------------------------------------------------------------------------------------------------------------------------------------------
--The observations raw_customers

--Toatal row counts
con.sql("SELECT COUNT(*) FROM bronze.raw_customers")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        99441 │
└──────────────┘

--Total Distinct customer_id(customer_id is generated for each orders) counts:
con.sql("SELECT COUNT(DISTINCT customer_id) FROM bronze.raw_customers")

┌─────────────────────────────┐
│ count(DISTINCT customer_id) │
│            int64            │
├─────────────────────────────┤
│                       99441 │
└─────────────────────────────┘

--Total Distinct customer_unique_id counts:
con.sql("SELECT COUNT(DISTINCT customer_unique_id) FROM bronze.raw_customers")

┌────────────────────────────────────┐
│ count(DISTINCT customer_unique_id) │
│               int64                │
├────────────────────────────────────┤
│                              96096 │
└────────────────────────────────────┘

--Total Repeated customer orders counts:
con.sql("SELECT COUNT(DISTINCT customer_id) - COUNT(DISTINCT customer_unique_id) FROM bronze.raw_customers")

┌────────────────────────────────────────────────────────────────────┐
│ (count(DISTINCT customer_id) - count(DISTINCT customer_unique_id)) │
│                               int64                                │
├────────────────────────────────────────────────────────────────────┤
│                                                               3345 │
└────────────────────────────────────────────────────────────────────┘

--Casing and whitespace test
con.sql("SELECT COUNT(DISTINCT customer_city),COUNT(DISTINCT lower(trim(customer_city))) FROM bronze.raw_customers")

┌───────────────────────────────┬───────────────────────────────────────────────────┐
│ count(DISTINCT customer_city) │ count(DISTINCT lower(main."trim"(customer_city))) │
│             int64             │                       int64                       │
├───────────────────────────────┼───────────────────────────────────────────────────┤
│                          4119 │                                              4119 │
└───────────────────────────────┴───────────────────────────────────────────────────┘

con.sql("SELECT COUNT(DISTINCT customer_state),COUNT(DISTINCT lower(trim(customer_state))) FROM bronze.raw_customers")
┌────────────────────────────────┬────────────────────────────────────────────────────┐
│ count(DISTINCT customer_state) │ count(DISTINCT lower(main."trim"(customer_state))) │
│             int64              │                       int64                        │
├────────────────────────────────┼────────────────────────────────────────────────────┤
│                             27 │                                                 27 │
└────────────────────────────────┴────────────────────────────────────────────────────┘