import pandas as pd
from pathlib import Path


def _csv_path(file_name: str) -> Path:
    try:
        # current directory
        current_file = Path(__file__)
        root_directory = current_file.parent.parent
        file_path = root_directory / "data" / file_name

        return file_path
    
    except Exception as e:
        raise FileNotFoundError("Data Folder or Csv File not found.")

def read_csv() -> pd.DataFrame:

    try:
        file_path = _csv_path("data.csv")

        if not file_path:
            raise FileNotFoundError("CSV file path is invalid.")

        df = pd.read_csv(file_path)
        if df is None:
            raise ValueError("DataFrame is not read properly.")

        return df
    except Exception as e:
        raise ValueError("Data Frame is not imported")


    


    