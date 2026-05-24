from services.load_data_to_psql import load_data_to_psql
from services.preprocessing import preprocess
from services.read_csv import read_csv
from services.aggregation import aggregate_sales
from services.export_to_excel import export_to_excel
from services.export_to_gsheet import export_to_gsheets
from helper.utils import setup_logging

import logging

logger = logging.getLogger(__name__)

def main():

    setup_logging()
    logger.info("Pipeline started")

    # Loading csv file
    df = read_csv()

    # Processing
    df = preprocess(df=df)

    # Load csv to database
    status = load_data_to_psql(df)
    if not status:
        raise ValueError("CSV Data is not Imported to Postgres SQL")
    else:
        logger.info("CSV Imported Successfully")

    # Aggregate via psql
    yearly_df, monthly_df, quarterly_df = aggregate_sales()

    # Export to excel
    export_to_excel(
        yearly_df=yearly_df,
        monthly_df=monthly_df,
        quarterly_df=quarterly_df
    )

    # Export to google sheet
    export_to_gsheets(
        yearly_df=yearly_df,
        monthly_df=monthly_df,
        quarterly_df=quarterly_df
    )

    logger.info("Pipeline finished successfully")


if __name__ == "__main__":
    main()