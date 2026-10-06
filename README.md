# Olist E-commerce Data Platform (Medallion Architecture)

An end-to-end ELT data platform built on the Olist Brazilian e-commerce dataset, using a Bronze → Silver → Gold medallion architecture with Python, DuckDB, dbt, and Airflow.

> **Status: In progress.** The Bronze layer is complete. Silver, Gold, testing, orchestration, and CI are being built.

## Project Goal

Olist is a real marketplace where sellers sell to customers across Brazil. Its data comes as 9 separate CSV files that are hard to analyze directly. This project turns them into clean, tested, analytics-ready tables so questions like these can be answered reliably:

- Which product categories generate the most revenue?
- Do late deliveries hurt review scores?
- Which sellers and regions perform worst?
- Are customers coming back?

## Architecture

```
Raw CSVs (Olist, 9 files)
        ↓
Bronze  - raw data loaded as-is, with load metadata
        ↓
Silver  - cleaned and typed data (dbt)          [planned]
        ↓
Gold    - star schema: facts and dimensions     [planned]
        ↓
Dashboard and insights                          [planned]
```

## Tech Stack

| Purpose | Tool |
|---|---|
| Ingestion | Python 3.10, pathlib |
| Warehouse | DuckDB |
| Transformation | dbt Core (dbt-duckdb) - planned |
| Orchestration | Apache Airflow - planned |
| Containerization | Docker - planned |
| CI | GitHub Actions - planned |
| Dashboard | Streamlit - planned |

## Repository Structure

```
olist-lakehouse-dbt-airflow/
├── ingestion/
│   └── load_bronze.py      # Loads raw CSVs into DuckDB (bronze schema)
├── dbt_project/            # Silver and Gold models (planned)
├── airflow/                # Orchestration DAGs (planned)
├── docs/                   # Diagrams and notes
├── data/
│   ├── raw/                # Olist CSVs (not committed)
│   └── warehouse/          # DuckDB file (not committed)
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vikash122005/olist-lakehouse-dbt-airflow.git
cd olist-lakehouse-dbt-airflow
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows PowerShell
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

### 3. Download the dataset

Download the **Brazilian E-Commerce Public Dataset by Olist** from Kaggle and place all 9 CSV files in `data/raw/`.

### 4. Load the Bronze layer

```bash
python ingestion/load_bronze.py
```

This creates `data/warehouse/olist.duckdb` with a `bronze` schema containing 9 tables.

## Bronze Layer

Bronze stores the data exactly as it arrived, with no cleaning, so there is always an untouched copy to rebuild from.

| Table | Rows |
|---|---|
| bronze.raw_customers | 99,441 |
| bronze.raw_geolocation | 1,000,163 |
| bronze.raw_order_items | 112,650 |
| bronze.raw_order_payments | 103,886 |
| bronze.raw_order_reviews | 99,224 |
| bronze.raw_orders | 99,441 |
| bronze.raw_products | 32,951 |
| bronze.raw_sellers | 3,095 |
| bronze.raw_category_translation | 71 |

Each table includes two metadata columns for lineage:

- `_loaded_at`: timestamp of the load
- `_source_file`: name of the CSV the row came from

## Design Decisions

- **Idempotent loads:** the loader uses `CREATE OR REPLACE TABLE`, so re-running it never duplicates rows.
- **Config-driven ingestion:** a file-to-table mapping dictionary and a single loop replace nine copy-pasted blocks.
- **Path handling with pathlib:** paths are derived from the script location, so it runs from any directory.
- **Safe connection handling:** `try/finally` guarantees the DuckDB connection closes even if a load fails.
- **Generated files stay out of Git:** raw data, the `.duckdb` file, and the virtual environment are git-ignored and rebuilt from code.
- **Why DuckDB:** free, serverless, fast for analytics, and reads CSVs directly, which suits a local, reproducible project.

## Data Model Notes

`orders` is the central table. Relationships are logical (the CSVs have no enforced foreign keys), so they will be validated with dbt tests:

| From | To | Join key |
|---|---|---|
| orders | customers | customer_id |
| order_items | orders | order_id |
| order_items | products | product_id |
| order_items | sellers | seller_id |
| order_payments | orders | order_id |
| order_reviews | orders | order_id |
| products | category_translation | product_category_name |

Known gotchas to handle in Silver: `customer_id` is per order while `customer_unique_id` identifies the real customer, `order_items` is identified by `order_id` plus `order_item_id`, and geolocation zip prefixes are not unique.

## Roadmap

- [x] Day 1: Repo setup and Bronze ingestion
- [ ] Day 2: Silver layer (cleaning and typing in dbt)
- [ ] Day 3: Gold layer (star schema: fact and dimension tables)
- [ ] Day 4: dbt tests and documentation
- [ ] Day 5: Airflow DAG and Docker
- [ ] Day 6: Dashboard and business insights
- [ ] Day 7: Architecture diagram, CI, and demo

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) on Kaggle.
