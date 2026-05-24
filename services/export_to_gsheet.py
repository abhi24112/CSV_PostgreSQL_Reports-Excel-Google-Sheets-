import os
import gspread
import pandas as pd
from pathlib import Path
from google.oauth2.service_account import Credentials
import logging

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def _get_client():
    creds_path = Path.cwd() / "credentials" / "google_service_account.json"
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return gspread.authorize(creds)


def _push_to_worksheet(sh, worksheet_title: str, df: pd.DataFrame):
    try:
        ws = sh.worksheet(worksheet_title)
    except gspread.WorksheetNotFound:
        rows = max(1, len(df) + 1)
        cols = max(1, len(df.columns))
        ws = sh.add_worksheet(title=worksheet_title, rows=str(rows), cols=str(cols))

    ws.clear()
    ws.update([df.columns.tolist()] + df.astype(str).values.tolist())


def _create_spreadsheet(gc, title: str, share_email: str):
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

    # Create directly in target Drive folder via Drive API (not gspread.create)
    file_metadata = {
        "name": title,
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "parents": [folder_id]
    }

    drive_service = gc.http_client  # reuse same auth
    response = gc.http_client.request(
        "post",
        "https://www.googleapis.com/drive/v3/files",
        json=file_metadata
    )

    file_id = response.json()["id"]
    sh = gc.open_by_key(file_id)
    sh.share(share_email, perm_type="user", role="writer")
    return sh


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value


def export_to_gsheets(yearly_df, monthly_df, quarterly_df):
    gc = _get_client()

    sh1 = gc.open_by_key(_require_env("YEARLY_SHEET_ID"))
    sh2 = gc.open_by_key(_require_env("MONTHLY_SHEET_ID"))
    sh3 = gc.open_by_key(_require_env("QUARTERLY_SHEET_ID"))

    _push_to_worksheet(sh1, "Yearly Sales", yearly_df)
    _push_to_worksheet(sh2, "Monthly Sales", monthly_df)
    _push_to_worksheet(sh3, "Quarterly Sales", quarterly_df)

    logger.info("Yearly sheet updated -> %s", sh1.url)
    logger.info("Monthly sheet updated -> %s", sh2.url)
    logger.info("Quarterly sheet updated -> %s", sh3.url)
    logger.info("Google Sheets exported successfully")