import logging
import csv
from google import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from helpers.helpers import load_sheet, load_excel_sheet, split_grade_and_gender

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
            if town in row[3].lower() and 'bye' not in row[5].lower() and \
                'bye' not in row[3].lower() and 'no game' not in row[5].lower():
                home_games.append(row)

        return home_games

    def write_schedule(self, file_name, town, assignor) -> str:
        town = town.lower()

        with open(file_name, 'w', newline='') as csv_file:
            field_names = ['Date', 'Start Time', 'Venue', 'Sub-Venue', 'Home Team',
                          'Away Team', 'League', 'Age Group', 'Gender', 'Type',
                          'Pattern', 'Assignor Name', 'Notes (Visible to All)']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            writer.writeheader()
            for row in self.get_home_games(town):
                grade, gender = split_grade_and_gender(row[0])
                writer.writerow({
                    'Date': row[2],
                    'Start Time': '',
                    'Venue': '',
                    'Sub-Venue': '',
                    'Age Group': grade,
                    'Gender': gender,
                    'Home Team': f'{row[3].strip()}-{row[4].strip()}',
                    'Away Team': f'{row[5].strip()}-{row[6].strip()}',
                    'League': town.title(),
                    'Type': 'Coastal',
                    'Pattern': 'Three Officials',
                    'Assignor Name': assignor,
                    'Notes (Visible to All)': row[1]
                })
        return file_name
