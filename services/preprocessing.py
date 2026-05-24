import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    if df is not None:
        # rename columsns
        df = df.rename(columns={
            "Row ID": "row_id",
            "Order ID": "order_id",
            "Order Date": "order_date",
            "Ship Date": "ship_date",
            "Ship Mode": "ship_mode",
            "Customer ID": "customer_id",
            "Customer Name": "customer_name",
            "Segment": "segment",
            "Country": "country",
            "City": "city",
            "State": "state",
            "Postal Code": "postal_code",
            "Region": "region",
            "Product ID": "product_id",
            "Category": "category",
            "Sub-Category": "sub_category",
            "Product Name": "product_name",
            "Sales": "sales",
        })

        # Fixing Date datatype issues if any
        df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True).dt.date
        df["ship_date"] = pd.to_datetime(df["ship_date"], dayfirst=True).dt.date
        
        # making postal code string
        df['postal_code'] = df['postal_code'].astype("string")

        # replaceing nan values with None for psycopg
        df = df.astype(object)
        df = df.where(pd.notnull(df), None)


        return df



