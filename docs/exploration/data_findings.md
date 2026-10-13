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

----------------------------------------------------------------------------------------------------------------------------------------------------------
--The observations raw_sellers

--Toatal row counts
con.sql("SELECT COUNT(*) FROM bronze.raw_sellers")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│         3095 │
└──────────────┘

--Total Distinct seller_id
con.sql("SELECT COUNT(DISTINCT seller_id) FROM bronze.raw_sellers")

┌───────────────────────────┐
│ count(DISTINCT seller_id) │
│           int64           │
├───────────────────────────┤
│                      3095 │
└───────────────────────────┘

--Casing and whitespace test

con.sql("SELECT COUNT(DISTINCT seller_city),COUNT(DISTINCT lower(trim(seller_city))) FROM bronze.raw_sellers")

┌─────────────────────────────┬─────────────────────────────────────────────────┐
│ count(DISTINCT seller_city) │ count(DISTINCT lower(main."trim"(seller_city))) │
│            int64            │                      int64                      │
├─────────────────────────────┼─────────────────────────────────────────────────┤
│                         611 │                                             611 │
└─────────────────────────────┴─────────────────────────────────────────────────┘

con.sql("SELECT COUNT(DISTINCT seller_state),COUNT(DISTINCT lower(trim(seller_state))) FROM bronze.raw_sellers")

┌──────────────────────────────┬──────────────────────────────────────────────────┐
│ count(DISTINCT seller_state) │ count(DISTINCT lower(main."trim"(seller_state))) │
│            int64             │                      int64                       │
├──────────────────────────────┼──────────────────────────────────────────────────┤
│                           23 │                                               23 │
└──────────────────────────────┴──────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------------------------------------------------------------
--The observations raw_category_translation

--Toatal row counts
con.sql("SELECT COUNT(*) FROM bronze.raw_category_translation")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│           71 │
└──────────────┘

--Total Distinct product_category_name
con.sql("SELECT COUNT(DISTINCT product_category_name) FROM bronze.raw_category_translation")

┌───────────────────────────────────────┐
│ count(DISTINCT product_category_name) │
│                 int64                 │
├───────────────────────────────────────┤
│                                    71 │
└───────────────────────────────────────┘

--Whitespace and casing
con.sql("SELECT COUNT(DISTINCT product_category_name),COUNT(DISTINCT lower(trim(product_category_name))) FROM bronze.raw_category_translation")

┌───────────────────────────────────────┬───────────────────────────────────────────────────────────┐
│ count(DISTINCT product_category_name) │ count(DISTINCT lower(main."trim"(product_category_name))) │
│                 int64                 │                           int64                           │
├───────────────────────────────────────┼───────────────────────────────────────────────────────────┤
│                                    71 │                                                        71 │
└───────────────────────────────────────┴───────────────────────────────────────────────────────────┘

con.sql("SELECT COUNT(DISTINCT product_category_name_english),COUNT(DISTINCT lower(trim(product_category_name_english))) FROM bronze.raw_category_translation")

┌───────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┐
│ count(DISTINCT product_category_name_english) │ count(DISTINCT lower(main."trim"(product_category_name_english))) │
│                     int64                     │                               int64                               │
├───────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│                                            71 │                                                                71 │
└───────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────┘


--Total NUll values in product_category_name

con.sql("SELECT COUNT(*) FROM bronze.raw_category_translation WHERE product_category_name IS NULL")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            0 │
└──────────────┘

--Total NUll values in product_category_name_english

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            0 │
└──────────────┘

--Total NullS in bronze.raw_products from product_category_name column

con.sql("SELECT COUNT(*) FROM bronze.raw_products WHERE product_category_name IS NULL")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│          610 │
└──────────────┘

--Unmatched rows in bronze.raw_category_translation table comapring with bronze.raw_products
--con.sql("""

...     SELECT COUNT(*)
...     FROM bronze.raw_products p
...     LEFT JOIN bronze.raw_category_translation t
...         ON p.product_category_name = t.product_category_name
...     WHERE t.product_category_name IS NULL
...       AND p.product_category_name IS NOT NULL
... """)

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│           13 │
└──────────────┘

--product_category_name that are not available in raw_category_translation but available in bronze.raw_products

--con.sql("""

...     SELECT DISTINCT p.product_category_name
...     FROM bronze.raw_products p
...     LEFT JOIN bronze.raw_category_translation t
...         ON p.product_category_name = t.product_category_name
...     WHERE t.product_category_name IS NULL
...       AND p.product_category_name IS NOT NULL
... """)
┌───────────────────────────────────────────────┐
│             product_category_name             │
│                    varchar                    │
├───────────────────────────────────────────────┤
│ portateis_cozinha_e_preparadores_de_alimentos │
│ pc_gamer                                      │
└───────────────────────────────────────────────┘

## Category translation findings

**What I checked:** whether every product category in `products` has an English name in the translation table.

**What I found:**
- The translation table has 71 rows, all unique, with no nulls and no casing or whitespace problems.
- 610 products have no category at all (NULL).
- 13 products have a category, but it is missing from the translation table. The two missing categories are `pc_gamer` and `portateis_cozinha_e_preparadores_de_alimentos`.
- 610 + 13 = 623 products had no English name in the first join.

**What I decided:**
- Keep `category_translation` in Silver as a clean copy of the 71 rows, with no changes to the data.
- Handle the gaps later in Gold (`dim_products`):
  - NULL category: label it `unknown`.
  - Category exists but has no translation: use the Portuguese name.
  - Always use a left join so no products are dropped.

**Why:** Dropping or leaving these products blank would hide them from reports, so every product still gets a readable category name.

----------------------------------------------------------------------------------------------------------------------------------------------------------
--The observations raw_products

--Rows and uniqueness:
con.sql("SELECT COUNT(*),COUNT(DISTINCT product_id) FROM bronze.raw_products")

┌──────────────┬────────────────────────────┐
│ count_star() │ count(DISTINCT product_id) │
│    int64     │           int64            │
├──────────────┼────────────────────────────┤
│        32951 │                      32951 │
└──────────────┴────────────────────────────┘

--Nulls per column:
con.sql("SELECT COUNT(*) - COUNT(product_category_name) AS Null_category_name,
                COUNT(*) - COUNT(product_name_lenght) AS Null_name_lenght,
                COUNT(*) - COUNT(product_description_lenght) AS Null_description_lenght,
                COUNT(*) - COUNT(product_photos_qty) AS Null_photos_qty,
                COUNT(*) - COUNT(product_weight_g) AS Null_weight_g,
                COUNT(*) - COUNT(product_length_cm) AS length_cm,
                COUNT(*) - COUNT(product_height_cm) AS Null_height_cm,
                COUNT(*) - COUNT(product_width_cm) AS Null_width_cm  FROM bronze.raw_products").show(max_width = 1000)

┌────────────────────┬──────────────────┬─────────────────────────┬─────────────────┬───────────────┬───────────┬────────────────┬───────────────┐
│ Null_category_name │ Null_name_lenght │ Null_description_lenght │ Null_photos_qty │ Null_weight_g │ length_cm │ Null_height_cm │ Null_width_cm │
│       int64        │      int64       │          int64          │      int64      │     int64     │   int64   │     int64      │     int64     │
├────────────────────┼──────────────────┼─────────────────────────┼─────────────────┼───────────────┼───────────┼────────────────┼───────────────┤
│                610 │              610 │                     610 │             610 │             2 │         2 │              2 │             2 │
└────────────────────┴──────────────────┴─────────────────────────┴─────────────────┴───────────────┴───────────┴────────────────┴───────────────┘

--Impossible values:
con.sql("SELECT COUNT(*) FROM bronze.raw_products WHERE  product_weight_g = 0")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            4 │
└──────────────┘

con.sql("""
...     SELECT
...         MIN(product_weight_g)  AS min_weight,  MAX(product_weight_g)  AS max_weight,
...         MIN(product_length_cm) AS min_length,  MAX(product_length_cm) AS max_length,
...         MIN(product_height_cm) AS min_height,  MAX(product_height_cm) AS max_height,
...         MIN(product_width_cm)  AS min_width,   MAX(product_width_cm)  AS max_width
...     FROM bronze.raw_products
... """).show(max_width=1000)

┌────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬───────────┬───────────┐
│ min_weight │ max_weight │ min_length │ max_length │ min_height │ max_height │ min_width │ max_width │
│   int64    │   int64    │   int64    │   int64    │   int64    │   int64    │   int64   │   int64   │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┼───────────┤
│          0 │      40425 │          7 │        105 │          2 │        105 │         6 │       118 │
└────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴───────────┴───────────┘

--Overlap check(Whether they’re empty on the same rows)
con.sql("SELECT COUNT(*) FROM bronze.raw_products WHERE product_category_name IS NULL AND product_name_lenght IS NULL AND product_description_lenght IS NULL AND product_photos_qty IS NULL")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│          610 │
└──────────────┘

--Where do the 2 null-weight products sit?
con.sql("SELECT COUNT(*) FROM bronze.raw_products WHERE product_category_name IS NULL AND product_name_lenght IS NULL AND product_description_lenght IS NULL AND product_photos_qty IS NULL AND product_weight_g IS NULL AND product_length_cm IS NULL AND product_height_cm IS NULL AND product_width_cm IS NULL")

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            1 │
└──────────────┘

--Where do the 2 null-weight products sit?(only for weight column)

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            1 │
└──────────────┘


## Products findings

**What I checked:** row count, uniqueness, nulls, and value ranges in products.

**What I found:**
- 32,951 products, all unique `product_id`.
- 610 products have no category, name length, description length or photo quantity, always on the same rows.
- 2 products have no weight or dimensions: one is inside the 610 group, and one (category `bebes`) has listing details but no measurements.
- 4 products have weight 0. All are in `cama_mesa_banho` with identical dimensions, so likely a missing weight recorded as 0.
- Length, height and width have no zeros or extreme values. Max weight is 40,425 g, which is plausible.

**What I decided:** keep all rows in Silver and only fix the two column spellings (`lenght` to `length`). Add a dbt test on Day 4 that weight must be greater than 0.

**Why:** changing or deleting these silently would hide a source problem. Gold decides how to treat them, for example excluding zero weights from shipping analysis.

-------------------------------------------------------------------------------------------------------------------------------------------------------

