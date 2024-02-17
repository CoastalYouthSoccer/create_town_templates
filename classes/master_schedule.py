import logging
import csv
from google import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from helpers.helpers import load_sheet

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
    def read_schedule(self) -> None:
        self.schedule = load_sheet(self.id, self.sheet_range)

    def get_home_games(self, town) -> list:
        home_games = []

        for row in self.schedule:
            if town in row['home_team'].lower():
                home_games.append(row)

        return home_games

    def write_schedule(self, file_name, town, assignor) -> str:
        town = town.lower()
        town_title = town.title()

        with open(file_name, 'w', newline='') as csv_file:
            field_names = ['date', 'start_time', 'venue', 'sub_venue', 'home_team',
                          'away_team', 'league', 'age_group', 'gender', 'type',
                          'pattern', 'assignor', 'notes']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            writer.writeheader()
            for row in self.get_home_games(town):
                writer.writerow({
                    'date': row['date'],
                    'start_time': '',
                    'venue': '',
                    'sub_venue': '',
                    'home_team': row['home_team'],
                    'away_team': row['away_team'],
                    'league': town_title,
                    'age_group': row['grade'],
                    'gender': row['gender'],
                    'type': 'Coastal',
                    'pattern': 'Three Officials',
                    'assignor': assignor,
                    'notes': row['division']
                })
        return file_name
