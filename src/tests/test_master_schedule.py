from unittest import (TestCase, main as test_main)
from unittest.mock import (patch, MagicMock)
from classes.master_schedule import MasterSchedule

GRADE34_BOYS = "Grade 3/4 Boys"
GRADE34 = "Grade 3/4"
BOYS = "Boys"
GIRLS = "Girls"
GRADE34_GIRLS = "Grade 3/4 Girls"
DIVISION1= "Division1"
APRIL06 = "04/06/2024"
APRIL13 = "04/13/2024"
APRIL20 = "04/20/2024"
CARVER = "Carver"
CARVER1 = "Carver-1"
CARVER2 = "Carver-2"
CARVER3 = "Carver-3"
COHASSET = "Cohasset"
COHASSET1 = "Cohasset-1"
COHASSET2 = "Cohasset-2"
HANOVER = "Hanover"
HINGHAM = "Hingham"
HINGHAM1 = "Hingham-1"
HOME_TEAM = "Home Team"
AWAY_TEAM = "Away Team"


class TestMasterSchedule(TestCase):
    def test_init(self):
        result = MasterSchedule('invalidid', 'A1:A1')
        self.assertEqual(result.id, 'invalidid')
        self.assertEqual(result.sheet_range, 'A1:A1')
        self.assertEqual(result.schedule, [])
        self.assertEqual(result.value_input_option, 'RAW')

    @patch('helpers.helpers.auth.default')
    @patch('helpers.helpers.build')
    def test_read_schedule(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_sheet_values = [
            ['Grade', 'Division', 'Date', HOME_TEAM, 'Home #', AWAY_TEAM, 'Away #'],
            [GRADE34_BOYS, DIVISION1, APRIL06, HANOVER, 1, COHASSET, 1],
            [GRADE34_BOYS, DIVISION1, APRIL06, HANOVER, 2, HINGHAM, 1],
            [GRADE34_BOYS, DIVISION1, APRIL13, CARVER, 3, COHASSET, 2],
            [GRADE34_BOYS, DIVISION1, APRIL13, HINGHAM, 1, CARVER, 1],
            [GRADE34_BOYS, DIVISION1, APRIL20, CARVER, 2, COHASSET, 1],
            [GRADE34_BOYS, DIVISION1, APRIL20, CARVER, 1, CARVER, 3],
            [GRADE34_GIRLS, DIVISION1, APRIL06, CARVER, 1, COHASSET, 1],
            [GRADE34_GIRLS, DIVISION1, APRIL06, CARVER, 2, HINGHAM, 1],
            [GRADE34_GIRLS, DIVISION1, APRIL13, CARVER, 3, COHASSET, 2],
            [GRADE34_GIRLS, DIVISION1, APRIL13, HINGHAM, 1, CARVER, 1],
        ]
        mock_execute_result = {'values': mock_sheet_values}
        mock_sheet_service = MagicMock()
        mock_sheet_service.values().get().execute.return_value = mock_execute_result
        mock_build.return_value.spreadsheets.return_value = mock_sheet_service

        schedule = MasterSchedule('validid', 'A:G')
        schedule.read_schedule()
        self.assertEqual(mock_sheet_values, schedule.schedule)

    @patch('helpers.helpers.auth.default')
    @patch('helpers.helpers.build')
    def test_get_home_games(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_sheet_values = [
            ['Grade', 'Division', 'Date', HOME_TEAM, 'Home #', AWAY_TEAM, 'Away #'],
            [GRADE34_BOYS, DIVISION1, APRIL06, HANOVER, 1, COHASSET, 1],
            [GRADE34_BOYS, DIVISION1, APRIL06, HANOVER, 2, HINGHAM, 1],
            [GRADE34_BOYS, DIVISION1, APRIL13, CARVER, 3, COHASSET, 1],
            [GRADE34_BOYS, DIVISION1, APRIL13, HINGHAM, 1, CARVER, 1],
            [GRADE34_BOYS, DIVISION1, APRIL20, CARVER, 2, COHASSET, 1],
            [GRADE34_BOYS, DIVISION1, APRIL20, CARVER, 1, CARVER, 3],
            [GRADE34_GIRLS, DIVISION1, APRIL06, CARVER, 1, COHASSET, 1],
            [GRADE34_GIRLS, DIVISION1, APRIL06, CARVER, 2, HINGHAM, 1],
            [GRADE34_GIRLS, DIVISION1, APRIL13, CARVER, 3, COHASSET, 2],
            [GRADE34_GIRLS, DIVISION1, APRIL13, HINGHAM, 1, CARVER, 1]
        ]
        mock_execute_result = {'values': mock_sheet_values}
        mock_sheet_service = MagicMock()
        mock_sheet_service.values().get().execute.return_value = mock_execute_result
        mock_build.return_value.spreadsheets.return_value = mock_sheet_service

        expected_results = [
            [GRADE34_BOYS, DIVISION1, APRIL13, CARVER, 3, COHASSET, 1],
            [GRADE34_BOYS, DIVISION1, APRIL20, CARVER, 2, COHASSET, 1],
            [GRADE34_BOYS, DIVISION1, APRIL20, CARVER, 1, CARVER, 3],
            [GRADE34_GIRLS, DIVISION1, APRIL06, CARVER, 1, COHASSET, 1],
            [GRADE34_GIRLS, DIVISION1, APRIL06, CARVER, 2, HINGHAM, 1],
            [GRADE34_GIRLS, DIVISION1, APRIL13, CARVER, 3, COHASSET, 2]
        ]

        schedule = MasterSchedule('validid', 'A:G')
        schedule.read_schedule()
        results = schedule.get_home_games('Carver')
        self.assertEqual(expected_results, results)

    @patch('helpers.helpers.auth.default')
    @patch('helpers.helpers.build')
    def test_write_schedule(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_sheet_values = [
            ['Division', 'Grade', 'Gender', 'Date', 'Home Team', 'Away Team'],
            [DIVISION1, GRADE34, BOYS, APRIL06, 'Hanover-1', COHASSET1],
            [DIVISION1, GRADE34, BOYS, APRIL06, 'Hanover-2', HINGHAM1],
            [DIVISION1, GRADE34, BOYS, APRIL13, CARVER3, COHASSET2],
            [DIVISION1, GRADE34, BOYS, APRIL13, HINGHAM1, CARVER1],
            [DIVISION1, GRADE34, BOYS, APRIL20, CARVER2, COHASSET1],
            [DIVISION1, GRADE34, BOYS, APRIL20, CARVER1, CARVER3],
            [DIVISION1, GRADE34, GIRLS, APRIL06, CARVER1, COHASSET1],
            [DIVISION1, GRADE34, GIRLS, APRIL06, CARVER2, HINGHAM1],
            [DIVISION1, GRADE34, GIRLS, APRIL13, CARVER3, COHASSET2],
            [DIVISION1, GRADE34, GIRLS, APRIL13, HINGHAM1, CARVER1],
        ]
        mock_execute_result = {'values': mock_sheet_values}
        mock_sheet_service = MagicMock()
        mock_sheet_service.values().get().execute.return_value = mock_execute_result
        mock_build.return_value.spreadsheets.return_value = mock_sheet_service

        schedule = MasterSchedule('validid', 'A:G')
        schedule.read_schedule()
        file_name = schedule.write_schedule('carver.csv', 'Carver', 'Homer')
        self.assertEqual(file_name, 'carver.csv')

if __name__ == '__main__':
    test_main()
