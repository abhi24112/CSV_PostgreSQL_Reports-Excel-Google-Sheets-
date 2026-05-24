import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def export_to_excel(yearly_df: pd.DataFrame, monthly_df: pd.DataFrame, quarterly_df: pd.DataFrame):
    output_dir = Path.cwd() / "output"
    output_dir.mkdir(exist_ok=True)

    yearly_df.to_excel(output_dir / "yearly_sales.xlsx", index=False)
    monthly_df.to_excel(output_dir / "monthly_sales.xlsx", index=False)
    quarterly_df.to_excel(output_dir / "quarterly_sales.xlsx", index=False)

    logger.info("Excel files exported to %s", str(output_dir))