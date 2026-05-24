import pandas as pd
from psycopg2.extras import execute_values
from database.db import DatabaseManager
from helper.utils import load_config
import logging

database_config = load_config()

logger = logging.getLogger(__name__)

def _get_existing_row_ids(db) -> set:
    db.execute_query(f"SELECT row_id FROM {database_config['table_name']}")
    return {row[0] for row in db.fetch_all()}

def load_data_to_psql(df: pd.DataFrame) -> bool:
    db = DatabaseManager()
    try:
        db.connect()

        existing_ids = _get_existing_row_ids(db)
        new_df = df[~df["row_id"].isin(existing_ids)]

        if new_df.empty:
            logger.info("No new rows to insert; database is already up to date")
            return True

        cols = [
            "row_id", "order_id", "order_date", "ship_date", "ship_mode",
            "customer_id", "customer_name", "segment", "country", "city",
            "state", "postal_code", "region", "product_id", "category",
            "sub_category", "product_name", "sales"
        ]

        query = f"""
            INSERT INTO {database_config["table_name"]}(
                row_id, order_id, order_date, ship_date, ship_mode,
                customer_id, customer_name, segment, country, city,
                state, postal_code, region, product_id, category,
                sub_category, product_name, sales
            ) VALUES %s
        """

        params = [tuple(row) for row in new_df[cols].to_numpy()]
        execute_values(db.cur, query, params, page_size=database_config["page_size"])
        db.commit()

        logger.info("Inserted %s new rows into %s", len(params), database_config["table_name"])
        return True

    except Exception as e:
        logger.exception("Failed to load data into Postgres: %s", e)
        db.rollback()
        logger.info("Changes were rolled back")
        return False
    finally:
        db.close()