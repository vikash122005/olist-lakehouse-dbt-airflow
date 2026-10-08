--The three observations

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

