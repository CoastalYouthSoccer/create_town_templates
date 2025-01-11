from unittest import (TestCase, main as test_main)
from unittest.mock import (patch, MagicMock)
import pytest
from classes.master_schedule import MasterSchedule

GRADE34 = "Grade 3/4"
BOYS = "Boys"
GIRLS = "Girls"
DIVISION1= "Division1"
APRIL06 = "04/06/2024"
APRIL13 = "04/13/2024"
APRIL20 = "04/20/2024"
CARVER1 = "Carver-1"
CARVER2 = "Carver-2"
CARVER3 = "Carver-3"
COHASSET1 = "Cohasset-1"
COHASSET2 = "Cohasset-2"
HANOVER1 = "Hanover-1"
HINGHAM1 = "Hingham-1"
LOCATION = "Location"
TIME = "10:00 PM"
SCORE = "Pending"
GIRLS_SCHEDULE = "Girls 7/8 D1"
BOYS_SCHEDULE = "Boys 7/8 D1"

MOCK_SHEET_VALUES = [
    ["Event ID", "Date", "Time", "Location", "Visitor", "V Score",
     "Home", "H Score", "Schedule"],
    [123456, APRIL06, TIME, LOCATION, HANOVER1, SCORE, COHASSET1,
     SCORE, GIRLS_SCHEDULE],
    [123457, APRIL06, TIME, LOCATION, 'Hanover-2', SCORE, HINGHAM1,
     SCORE, GIRLS_SCHEDULE],
    [123458, APRIL13, TIME, LOCATION, CARVER3, SCORE, COHASSET2,
     SCORE, GIRLS_SCHEDULE],
    [123459, APRIL13, TIME, LOCATION, HINGHAM1, SCORE, CARVER1,
     SCORE, GIRLS_SCHEDULE],
    [123450, APRIL20, TIME, LOCATION, CARVER2, SCORE, COHASSET1,
     SCORE, BOYS_SCHEDULE],
    [123451, APRIL20, TIME, LOCATION, CARVER1, SCORE, CARVER3,
     SCORE, BOYS_SCHEDULE],
    [123452, APRIL06, TIME, LOCATION, CARVER1, SCORE, COHASSET1,
     SCORE, BOYS_SCHEDULE],
    [123453, APRIL06, TIME, LOCATION, CARVER2, SCORE, HINGHAM1,
     SCORE, BOYS_SCHEDULE],
    [123454, APRIL13, TIME, LOCATION, CARVER3, SCORE, COHASSET2,
     SCORE, BOYS_SCHEDULE],
    [123455, APRIL13, TIME, LOCATION, HINGHAM1, SCORE, CARVER1,
     SCORE, BOYS_SCHEDULE]
]


@patch('helpers.helpers.auth.default')
class TestMasterSchedule(TestCase):
    def test_init(self, mock_auth_default):
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        result = MasterSchedule('invalidid', 'A1:A1')
        self.assertEqual(result.id, 'invalidid')
        self.assertEqual(result.sheet_range, 'A1:A1')
        self.assertEqual(result.schedule, [])
        self.assertEqual(result.value_input_option, 'RAW')

    @patch('helpers.helpers.build')
    def test_read_schedule(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_execute_result = {'values': MOCK_SHEET_VALUES}
        mock_sheet_service = MagicMock()
        mock_sheet_service.values().get().execute.return_value = mock_execute_result
        mock_build.return_value.spreadsheets.return_value = mock_sheet_service

        schedule = MasterSchedule('validid', 'A:I')
        schedule.read_schedule()
        self.assertEqual(MOCK_SHEET_VALUES, schedule.schedule)

    @patch('helpers.helpers.build')
    def test_get_home_games(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_execute_result = {'values': MOCK_SHEET_VALUES}
        mock_sheet_service = MagicMock()
        mock_sheet_service.values().get().execute.return_value = mock_execute_result
        mock_build.return_value.spreadsheets.return_value = mock_sheet_service

        expected_results = [
            [123459, APRIL13, TIME, LOCATION, HINGHAM1, SCORE, CARVER1,
             SCORE, GIRLS_SCHEDULE],
            [123451, APRIL20, TIME, LOCATION, CARVER1, SCORE, CARVER3,
             SCORE, BOYS_SCHEDULE],
            [123455, APRIL13, TIME, LOCATION, HINGHAM1, SCORE, CARVER1,
             SCORE, BOYS_SCHEDULE]
        ]

        schedule = MasterSchedule('validid', 'A:I')
        schedule.read_schedule()
        results = schedule.get_home_games('Carver')
        self.assertEqual(expected_results, results)

    @patch('helpers.helpers.build')
    def test_write_schedule(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_sheet_values = MOCK_SHEET_VALUES
        mock_execute_result = {'values': mock_sheet_values}
        mock_sheet_service = MagicMock()
        mock_sheet_service.values().get().execute.return_value = mock_execute_result
        mock_build.return_value.spreadsheets.return_value = mock_sheet_service

        schedule = MasterSchedule('validid', 'A:I')
        schedule.read_schedule()
        file_name = schedule.write_schedule('carver.csv', 'Carver', 'Homer')
        self.assertEqual(file_name, 'carver.csv')

if __name__ == '__main__':
    test_main()
