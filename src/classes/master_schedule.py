import logging
import csv
from google import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from helpers.helpers import (load_sheet, load_excel_sheet, extract_team_name,
                            split_grade_gender_division)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

logger = logging.getLogger(__name__)


class MasterSchedule():
    def __init__(self, id, sheet_range) -> None:
        self.id = id
        self.sheet_range = sheet_range
        self.credentials, _ = auth.default()
        self.value_input_option = "RAW"
        self.schedule = []

# Read the sheet row-by-row.
#   Ignore the header 
    def read_schedule(self, excel_format=False) -> None:
        if excel_format:
            self.schedule = load_excel_sheet(self.id, self.sheet_range)
        else:
            self.schedule = load_sheet(self.id, self.sheet_range)

    def get_home_games(self, town) -> list:
        home_games = []
        town = town.lower()
        for row in self.schedule:
            if town in row[6].lower():
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
                game_info = split_grade_gender_division(row[8])
                writer.writerow({
                    "Game ID": row[0],
                    "Date": row[1],
                    "Start Time": "",
                    "Venue": "",
                    "Sub-Venue": "",
                    "Age Group": game_info["grade"],
                    "Gender": game_info["gender"],
                    "Home Team": extract_team_name(row[6]),
                    "Away Team": extract_team_name(row[4]),
                    "League": town.title(),
                    "Type": "Coastal",
                    "Pattern": "Three Officials",
                    "Assignor Name": assignor,
                    "Assignor Notes": game_info["division"]
                })
        return file_name
