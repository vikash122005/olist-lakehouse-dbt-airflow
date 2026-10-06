###Define paths (raw folder, warehouse file)
from pathlib import Path
import duckdb

ROOT = Path(__file__).parent.parent.resolve()

RAW_DIR = ROOT / "data" / "raw"

DB_PATH = ROOT / "data" / "warehouse" / "olist.duckdb"


###Define the file-to-table mapping

MAPPING = {
    "olist_customers_dataset.csv":"raw_customers",
    "olist_geolocation_dataset.csv":"raw_geolocation",
    "olist_order_items_dataset.csv":"raw_order_items",
    "olist_order_payments_dataset.csv":"raw_order_payments",
    "olist_order_reviews_dataset.csv":"raw_order_reviews",
    "olist_orders_dataset.csv":"raw_orders",
    "olist_products_dataset.csv":"raw_products",
    "olist_sellers_dataset.csv":"raw_sellers",
    "product_category_name_translation.csv":"raw_category_translation"
}


###Connect to the DuckDB file and create the bronze schema

def main():
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS bronze")
        ###Loop over the mapping and load each table
        for file_name,table_name in MAPPING.items():
            file_path = RAW_DIR / file_name
            sql = f"""

            CREATE OR REPLACE TABLE bronze.{table_name} AS
            SELECT *,
                current_timestamp AS _loaded_at,
                '{file_name}' AS _source_file
            FROM read_csv_auto('{file_path.as_posix()}')
            """
            con.execute(sql)

            row_count = con.execute(f"SELECT COUNT(*) FROM bronze.{table_name}").fetchone()[0]
            print(f"Loaded {row_count} rows into bronze.{table_name} from {file_name}")
    finally:
    
        con.close()



###Print the row count for each table


###Close the connection

if __name__ == "__main__": main()