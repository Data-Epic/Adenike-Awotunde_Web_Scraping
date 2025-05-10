import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import logging
from io import StringIO
from datetime import datetime
from dotenv import load_dotenv
import os

class PremierLeagueStatsScraper:
    """
    Scrapes Premier League stats for 2024-2025 season from fbref.com and exports them to Google Sheets
    it initializes the class, set up and load  the environment and also set up logging for easy debugging.
    """

    def __init__(self):
        self._load_environment()
        self._setup_logging()

        self.url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        self.sheet_title = "2024-2025 Premier League Data"
        self.creds_file = os.getenv("CREDENTIALS_FILE")
        self.sheet = None
        self.soup = None

    def _load_environment(self):
        load_dotenv()
        print(f"SHEET_ID: {os.getenv('SHEET_ID')}, CREDENTIALS_FILE: {os.getenv('CREDENTIALS_FILE')}")
        self.sheet_id = os.getenv("SHEET_ID")

    def _setup_logging(self):
        logging.basicConfig(
            filename='history.log',
            level=logging.INFO,
            format='%(asctime)s: %(levelname)s: %(message)s'
        )

    # Authenticating the sheet
    def authenticate(self):
        try:
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file(self.creds_file, scopes=scopes)
            client = gspread.authorize(creds)
            self.sheet = client.open_by_key(self.sheet_id)
            self.sheet.update_title(self.sheet_title)
            logging.info("Authenticated with Google Sheets.")
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            raise Exception("Failed to authenticate with Google Sheets.")
    
    # Sheet reset to clear initial data in the sheet
    def reset_sheet(self):
        try:
            worksheets = self.sheet.worksheets()
            for i, ws in enumerate(worksheets):
                if i != 0:
                    self.sheet.del_worksheet(ws)
            self.sheet.get_worksheet(0).clear()
            logging.info("Google Sheet reset complete.")
        except Exception as e:
            logging.error(f"Reset sheet error: {e}")
            raise

    # Scrape function
    def scrape_page(self):
        try:
            page = urlopen(self.url)
            html = page.read().decode("utf-8")
            self.soup = BeautifulSoup(html, "html.parser")
            logging.info("Page scraped successfully.")
        except Exception as e:
            logging.error(f"Scrape failed: {e}")
            raise Exception("Check if the URL is accessible or if your internet is working.")

    # Exporting the tables to the sheet
    def export_tables(self):
        try:
            tables = self.soup.find_all("table")

            for table in tables:
                try:
                    caption = table.find("caption").get_text(strip=True)
                    table_id = table["id"]
                    worksheet_title = f"{caption}_{table_id}"

                    df = pd.read_html(StringIO(str(table)))[0]

                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = [' '.join(col).strip() for col in df.columns.values]

                    df["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    print(f"\nPreview of '{worksheet_title}':")
                    print(df.head())

                    try:
                        worksheet = self.sheet.worksheet(worksheet_title)
                        worksheet.clear()
                    except gspread.exceptions.WorksheetNotFound:
                        worksheet = self.sheet.add_worksheet(title=worksheet_title, rows="100", cols="20")

                    set_with_dataframe(worksheet, df)
                    logging.info(f"Exported: {worksheet_title}")

                except Exception as e:
                    logging.error(f"Error in table '{worksheet_title}': {e}")
                    continue

        except Exception as e:
            logging.error(f"Export failed: {e}")
            raise

    def run(self):
        print("Starting Premier League stats export process...")
        self.authenticate()
        self.reset_sheet()
        self.scrape_page()
        self.export_tables()
        print("Premier League data successfully exported to Google Sheets!")

# run the script
if __name__ == "__main__":
    scraper = PremierLeagueStatsScraper()
    scraper.run()
