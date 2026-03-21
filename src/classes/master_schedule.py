import logging
import csv
import gspread
from google.auth import default

from helpers.helpers import (load_excel_sheet,
                            split_grade_gender_division)

creds, _ = default(scopes=[
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    ])

logger = logging.getLogger(__name__)

client = gspread.authorize(creds)


class MasterSchedule():
    def __init__(self, sheet_id) -> None:
        self.work_book = client.open_by_key(sheet_id)
        self.schedule = []

# Read the sheet row-by-row.
#   Ignore the header 
    def read_schedule(self, excel_format=False) -> None:
        if excel_format:
            self.schedule = load_excel_sheet(self.id, self.sheet_range)
        else:
            sheet = self.work_book.worksheet("Schedule")

            self.schedule = sheet.get_all_records()

    def get_home_games(self, town) -> list:
        home_games = []
        town = town.lower()
        for row in self.schedule:
            if town in row['Home Team'].lower():
                home_games.append(row)

        return home_games

    def write_schedule(self, file_name, town, assignor) -> str:
        town = town.lower()

        with open(file_name, "w", newline="") as csv_file:
            field_names = [
                "Game ID", "Date", "Start Time", "Venue", "Sub-Venue",
                "Home Team", "Away Team", "League", "Age Group",
                "Gender", "Type", "Pattern", "Assignor Name",
                "Assignor Notes"
            ]
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            writer.writeheader()
            for row in self.get_home_games(town):
                writer.writerow({
                    "Game ID": row["Game Id"],
                    "Date": row["Date"],
                    "Start Time": "",
                    "Venue": row["Venue"],
                    "Sub-Venue": row["Sub Venue"],
                    "Age Group": row["Grade"],
                    "Gender": row["Gender"],
                    "Home Team": row["Home Team"],
                    "Away Team": row["Away Team"],
                    "League": town.title(),
                    "Type": "Coastal",
                    "Pattern": "Three Officials",
                    "Assignor Name": assignor,
                    "Assignor Notes": row["Division"]
                })
        return file_name
