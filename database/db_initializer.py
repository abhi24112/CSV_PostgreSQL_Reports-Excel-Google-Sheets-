import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from helper.utils import load_config

# Importing yaml data
database_config = load_config()


load_dotenv()


def create_database_if_not_exists(target_db: str) -> None:

    """
    Create the Postgres database if it does not exist.
    """

    host = os.getenv("DB_HOST")
    maintenance_db = os.getenv("MAINTENENCE_DB")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT")

    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            database=maintenance_db,
            user=user,
            password=password,
            port=port,
        )
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (target_db,))
            exists = cur.fetchone() is not None

            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(target_db)))
                print(f"Created database: {target_db}")
            else:
                print(f"Database already exists: {target_db}")
    finally:
        if conn is not None:
            conn.close()


def initialize_schema(target_db: str) -> None:

	"""Create required tables inside target_db (idempotent).

	This schema matches the columns in data/data.csv.
	"""

	host = os.getenv("DB_HOST")
	user = os.getenv("DB_USER")
	password = os.getenv("DB_PASSWORD")
	port = int(os.getenv("DB_PORT", "5432"))

	conn = None
	try:
		conn = psycopg2.connect(
			host=host,
			database=target_db,
			user=user,
			password=password,
			port=port
		)

		with conn:
			with conn.cursor() as cur:
				cur.execute(
					f"""
					CREATE TABLE IF NOT EXISTS {database_config["table_name"]} (
						row_id INTEGER PRIMARY KEY,
						order_id TEXT NOT NULL,
						order_date DATE NOT NULL,
						ship_date DATE NOT NULL,
						ship_mode TEXT,
						customer_id TEXT,
						customer_name TEXT,
						segment TEXT,
						country TEXT,
						city TEXT,
						state TEXT,
						postal_code TEXT,
						region TEXT,
						product_id TEXT,
						category TEXT,
						sub_category TEXT,
						product_name TEXT,
						sales NUMERIC(12, 4)
					)
					"""
				)

		print("Schema initialized (superstore_orders table ready)")
	finally:
		if conn is not None:
			conn.close()


def main() -> None:
    target_db = os.getenv("DB_DATABASE", "retail")
    create_database_if_not_exists(target_db)
    initialize_schema(target_db)


if __name__ == "__main__":
	main()
