import pandas as pd

from database.db import DatabaseManager
import logging

logger = logging.getLogger(__name__)

def aggregate_sales() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    db = DatabaseManager()

    try:
        db.connect()

        # Yearly, Montly, Quaterly Sales Query
        yearly_query = """
            SELECT 
                EXTRACT(YEAR FROM order_date) AS year,
                SUM(sales) AS total_sales
            FROM superstore_orders
            GROUP BY year
            ORDER BY year
        """
        monthly_query = """
            SELECT 
                EXTRACT(YEAR FROM order_date) AS year,
                EXTRACT(MONTH FROM order_date) AS month_number,
                TO_CHAR(order_date, 'Month') AS month_name,
                SUM(sales) AS total_sales
            FROM superstore_orders
            GROUP BY year, month_number, month_name
            ORDER BY year, month_number;
        """
        quaterly_query = """
            SELECT 
                EXTRACT(YEAR FROM order_date) AS year,
                CASE EXTRACT(QUARTER FROM order_date)
                    WHEN 1 THEN '1st'
                    WHEN 2 THEN '2nd'
                    WHEN 3 THEN '3rd'
                    WHEN 4 THEN '4th'
                END AS quarter_name,
                SUM(sales) AS total_sales
            FROM superstore_orders
            GROUP BY year, quarter_name
            ORDER BY year, quarter_name;
        """

        # Get dataframes
        db.execute_query(yearly_query)
        yearly_sales_df = pd.DataFrame(
            db.fetch_all(),
            columns=["year", "total_sales"], 
        )
        
        db.execute_query(monthly_query)
        monthly_sales_df = pd.DataFrame(
            db.fetch_all(),
            columns=["year", "month", "month_name", "total_sales"],
        )

        db.execute_query(quaterly_query)
        quaterly_sales_df = pd.DataFrame(
            db.fetch_all(),
            columns=["year", "quarter", "total_sales"],
        )

        return yearly_sales_df, monthly_sales_df, quaterly_sales_df

    except Exception as e:
        logger.exception("Aggregation failed: %s", e)
        raise
    finally:
        db.close()