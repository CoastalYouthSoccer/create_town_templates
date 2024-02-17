from unittest import (TestCase, mock)
from unittest.mock import (patch, MagicMock)
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

class TestMasterSchedule(TestCase):
    def test_init(self):
        result = MasterSchedule('invalidid', 'A1:A1')
        self.assertEqual(result.id, 'invalidid')
        self.assertEqual(result.sheet_range, 'A1:A1')
        self.assertEqual(result.schedule, [])
        self.assertEqual(result.value_input_option, 'RAW')

    @patch('helpers.utils.auth.default')
    @patch('helpers.utils.build')
    def test_read_schedule(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_sheet_values = [
            ['Division', 'Grade', 'Gender', 'Date', 'Home Team', 'Away Team'],
            [DIVISION1, GRADE34, BOYS, APRIL06, HANOVER1, COHASSET1],
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

        expected_results = [
            {'division': DIVISION1, 'grade': GRADE34, 'gender': BOYS,
             'date': APRIL06, 'home_team': HANOVER1, 'away_team': COHASSET1},
            {'division': DIVISION1, 'grade': GRADE34, 'gender': BOYS,
             'date': APRIL06, 'home_team': 'Hanover-2', 'away_team': HINGHAM1},
            {'division': DIVISION1, 'grade': GRADE34, 'gender': BOYS,
             'date': APRIL13, 'home_team': CARVER3, 'away_team': COHASSET2},
            {'division': DIVISION1, 'grade': GRADE34, 'gender': BOYS,
             'date': APRIL13, 'home_team': HINGHAM1, 'away_team': CARVER1},
                {'division': DIVISION1, 'grade': GRADE34, 'gender': BOYS,
             'date': APRIL20, 'home_team': CARVER2, 'away_team': COHASSET1},
            {'division': DIVISION1, 'grade': GRADE34, 'gender': BOYS,
             'date': APRIL20, 'home_team': CARVER1, 'away_team': CARVER3},
            {'division': DIVISION1, 'grade': GRADE34, 'gender': GIRLS,
             'date': APRIL06, 'home_team': CARVER1, 'away_team': COHASSET1},
            {'division': DIVISION1, 'grade': GRADE34, 'gender': GIRLS,
             'date': APRIL06, 'home_team': CARVER2, 'away_team': HINGHAM1},
            {'division': DIVISION1, 'grade': GRADE34, 'gender': GIRLS,
             'date': APRIL13, 'home_team': CARVER3, 'away_team': COHASSET2},
            {'division': DIVISION1, 'grade': GRADE34, 'gender': GIRLS,
             'date': APRIL13, 'home_team': HINGHAM1, 'away_team': CARVER1}
        ]

        schedule = MasterSchedule('validid', 'A:G')
        self.assertEqual(expected_results, schedule.read_schedule())

    @patch('helpers.utils.auth.default')
    @patch('helpers.utils.build')
    def test_get_home_games(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_sheet_values = [
            ['Division', 'Grade', 'Gender', 'Date', 'Home Team', 'Away Team'],
            [DIVISION1, GRADE34, BOYS, APRIL06, HANOVER1, COHASSET1],
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

        expected_results = {
            GRADE34: {
                BOYS: {
                    'games': [
                        {'date': APRIL13, 'home_team': CARVER3, 'away_team': COHASSET2},
                        {'date': APRIL20, 'home_team': CARVER2, 'away_team': COHASSET1},
                        {'date': APRIL20, 'home_team': CARVER1, 'away_team': CARVER3}
                    ]
                },
                GIRLS: {
                    'games': [
                        {'date': APRIL06, 'home_team': CARVER1, 'away_team': COHASSET1},
                        {'date': APRIL06, 'home_team': CARVER2, 'away_team': HINGHAM1},
                        {'date': APRIL13, 'home_team': CARVER3, 'away_team': COHASSET2}
                    ]
                }
            }
        }

        schedule = MasterSchedule('validid', 'A:G')
        results = schedule.get_home_games('Carver')
        self.assertEqual(expected_results, results)

#    @patch('helpers.utils.auth.default')
#    @patch('helpers.utils.build')
#    def test_write_schedule(self, mock_build, mock_auth_default):
#        # Mock the necessary objects
#        mock_credentials = MagicMock()
#        mock_auth_default.return_value = (mock_credentials, None)
#        mock_execute_result = {
#            'spreadsheetId': 'sheetid',
#            'updateRange': 'testrange',
#            'updatedRows': 11,
#            'updatedColumns': 6,
#            'updatedCells': 66
#        }
#
#        mock_sheet_service = MagicMock()
#        mock_sheet_service.values().update().execute.return_value = mock_execute_result
#        mock_build.return_value.spreadsheets.return_value = mock_sheet_service
#
#        mock_schedule = {
#            'division1': {
#                'Grade 5/6': {
#                    'Boys': [
#                        ['04/06/2024', 'Carver-1', 'Cohasset-1'],
#                        ['04/06/2024', 'Carver-2', 'Hingham-1'],
#                        ['04/13/2024', 'Carver-3', 'Cohasset-2'],
#                        ['04/13/2024', 'Hingham-1', 'Carver-1'],
#                        ['04/20/2024', 'Carver-2', 'Cohasset-1']
#                    ],
#                    'Girls': [
#                        ['05/11/2024', 'Cohasset-1', 'Carver-1'],
#                        ['05/11/2024', 'Carver-2', 'Hingham-1'],
#                        ['05/18/2024', 'Cohasset-2', 'Cohasset-1'],
#                        ['05/18/2024', 'Carver-3', 'Carver-2'],
#                        ['05/25/2024', 'No Games', 'No Games'],
#                        ['06/01/2024', 'Cohasset-1', 'Hingham-1']
#                    ]
#                }
#            }
#        }
#
#        schedule = MasterSchedule('validid', 'A:G')
#        results = schedule.write_schedule(mock_schedule)
#        self.assertEqual(expected_results, results)


if __name__ == '__main__':
    unittest.main()
