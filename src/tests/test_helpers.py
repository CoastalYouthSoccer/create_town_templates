from unittest import TestCase, main as test_main
from unittest.mock import (patch, MagicMock)
from os import environ
from os.path import (join, dirname)
from googleapiclient.errors import HttpError
from helpers.helpers import (load_sheet, get_email_vars,
                             get_spreadsheet_vars, extract_team_name,
                             split_grade_gender_division)

CONST_EMAIL_EMAIL = "email_email"
CONST_EMAIL_USERNAME = "email_username"
CONST_EMAIL_PASSWORD = "email_password"
CONST_TEAM_NAME = "Team-1"
EMPTY_GENDER_GRADE_DIVISION = {
    "gender": None,
    "grade": None,
    "division": None
}

class TestGetEnvironment(TestCase):
    @patch.dict(environ,{
    "SPREADSHEET_ID": "season_id",
    "SPREADSHEET_RANGE": "season_range",
    "GOOGLE_APPLICATION_CREDENTIALS": "dontshare",
    }, clear=True)
    def test_all_variables_set(self):
        expected_result = {
            'SPREADSHEET_ID': 'season_id',
            'SPREADSHEET_RANGE': 'season_range',
            'GOOGLE_APPLICATION_CREDENTIALS': 'dontshare'
        }
        rc, result = get_spreadsheet_vars()
        self.assertEqual(rc, 0)
        self.assertEqual(result, expected_result)

    @patch.dict(environ,{
    "SPREADSHEET_RANGE": "season_range",
    "GOOGLE_APPLICATION_CREDENTIALS": "dontshare",
    }, clear=True)
    def test_missing_season_id(self):
        expected_result = {
            'SPREADSHEET_ID': None,
            'SPREADSHEET_RANGE': 'season_range',
            'GOOGLE_APPLICATION_CREDENTIALS': 'dontshare'
        }

        with self.assertLogs(level='INFO') as cm:
            rc, result = get_spreadsheet_vars()
        self.assertEqual(rc, 55)
        self.assertEqual(cm.output,
                         ['ERROR:root:SPREADSHEET_ID environment variable is missing'])
        self.assertEqual(result, expected_result)

    @patch.dict(environ,{}, clear=True)
    def test_missing_everything(self):
        expected_result = {
            'SPREADSHEET_ID': None,
            'SPREADSHEET_RANGE': None,
            'GOOGLE_APPLICATION_CREDENTIALS': None
        }
        with self.assertLogs(level='INFO') as cm:
            rc, result = get_spreadsheet_vars()
        self.assertEqual(rc, 55)
        self.assertEqual(cm.output,
                         ['ERROR:root:GOOGLE_APPLICATION_CREDENTIALS environment variable is missing',
                          'ERROR:root:SPREADSHEET_ID environment variable is missing',
                          'ERROR:root:SPREADSHEET_RANGE environment variable is missing'])
        self.assertEqual(result, expected_result)


class TestLoadSheet(TestCase):
    @patch('helpers.helpers.auth.default')
    @patch('helpers.helpers.build')
    def test_load_sheet_success(self, mock_build, mock_auth_default):
        # Mock the necessary objects
        mock_credentials = MagicMock()
        mock_auth_default.return_value = (mock_credentials, None)
        mock_sheet_values = [['data', 'from', 'sheet']]
        mock_execute_result = {'values': mock_sheet_values}
        mock_sheet_service = MagicMock()
        mock_sheet_service.values().get().execute.return_value = mock_execute_result
        mock_build.return_value.spreadsheets.return_value = mock_sheet_service

        with self.assertLogs(level='INFO') as cm:
            result = load_sheet('sheet_id', 'A1:B2')

        # Assert the results
        self.assertEqual(result, mock_sheet_values)
        self.assertEqual(cm.output, ['INFO:root:1 rows retrieved'])

#    @patch('helpers.helpers.auth.default')
#    @patch('helpers.helpers.build')
#    def test_load_sheet_failure(self, mock_build, mock_auth_default):
#        # Mock the necessary objects
#        temp = {
#            "error": {
#                "code": 404,
#                "message": "Requested entity was not found.",
#                "status": "NOT_FOUND"
#                }
#            }
#        mock_resp = {
#            'vary': 'Origin, X-Origin, Referer',
#            'reason': 'no reason',
#            'content-type': 'application/json; charset=UTF-8',
#            'date': 'Sun, 03 Dec 2023 19:01:22 GMT', 'server': 'ESF',
#            'cache-control': 'private', 'x-xss-protection': '0',
#            'x-frame-options': 'SAMEORIGIN', 'x-content-type-options': 'nosniff',
#            'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
#            'x-l2-request-path': 'l2-managed-6', 'transfer-encoding': 'chunked',
#            'status': '404', 'content-length': '114', '-content-encoding': 'gzip'}
#        mock_content = json.dumps(temp).encode('utf-8')
##        mock_resp = json.dumps(resp).encode('utf-8')
#        mock_credentials = MagicMock()
#        mock_auth_default.return_value = (mock_credentials, None)
#        mock_sheet_service = MagicMock()
#        mock_sheet_service.values().get().execute.side_effect = \
#            HttpError(content=mock_content, resp=mock_resp)
#        mock_build.return_value.spreadsheets.return_value = mock_sheet_service
#
#        # Call the function
#        result = load_sheet('sheet_id', 'A1:B2')
#
#        # Assert the results
#        self.assertEqual(result, [])
#        mock_auth_default.assert_called_once()
#        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_credentials)

class TestEMailVars(TestCase):
    @patch.dict(environ,{
    "EMAIL_SERVER": "smtp.example.com",
    "EMAIL_EMAIL": CONST_EMAIL_EMAIL,
    "EMAIL_PORT": "123",
    "EMAIL_USERNAME": CONST_EMAIL_USERNAME,
    "EMAIL_PASSWORD": CONST_EMAIL_PASSWORD,
    }, clear=True)
    def test_all_email_vars_set(self):
        expected_results = {
            'EMAIL_SERVER': 'smtp.example.com',
            "EMAIL_EMAIL": CONST_EMAIL_EMAIL,
            'EMAIL_PORT': 123,
            'EMAIL_USERNAME': CONST_EMAIL_USERNAME,
            'EMAIL_PASSWORD': CONST_EMAIL_PASSWORD
        }
        rc, result = get_email_vars()
        self.assertEqual(result, expected_results)
        self.assertEqual(rc, 0)

    @patch.dict(environ,{
    "EMAIL_EMAIL": CONST_EMAIL_EMAIL,
    "EMAIL_USERNAME": CONST_EMAIL_USERNAME,
    "EMAIL_PASSWORD": CONST_EMAIL_PASSWORD,
    }, clear=True)
    def test_default_email_vars_set(self):
        expected_results = {
            'EMAIL_SERVER': 'smtp.gmail.com',
            "EMAIL_EMAIL": CONST_EMAIL_EMAIL,
            'EMAIL_PORT': 587,
            'EMAIL_USERNAME': CONST_EMAIL_USERNAME,
            'EMAIL_PASSWORD': CONST_EMAIL_PASSWORD
        }
        rc, result = get_email_vars()
        self.assertEqual(result, expected_results)
        self.assertEqual(rc, 0)

    @patch.dict(environ,{}, clear=True)
    def test_missing_email_vars(self):
        expected_results = {
            'EMAIL_SERVER': 'smtp.gmail.com',
            "EMAIL_EMAIL": None,
            'EMAIL_PORT': 587,
            'EMAIL_USERNAME': None,
            'EMAIL_PASSWORD': None
        }

        with self.assertLogs(level='INFO') as cm:
            rc, result = get_email_vars()
        self.assertEqual(rc, 55)
        self.assertEqual(cm.output,
                         ['INFO:root:EMAIL_SERVER environment variable is missing, defaulting to "smtp.gmail.com"',
                          'INFO:root:EMAIL_PORT environment variable is missing, defaulting to 587',
                          'ERROR:root:EMAIL_USERNAME environment variable is missing',
                          'ERROR:root:EMAIL_EMAIL environment variable is missing',
                          'ERROR:root:EMAIL_PASSWORD environment variable is missing'])
        self.assertEqual(result, expected_results)


class TestMisc(TestCase):
    def test_split_grade_gender_division_valid(self):
        expected_result = {
            "gender": "Girls",
            "grade": "Grade 7/8",
            "division": "D1"
        }
        result = split_grade_gender_division('Girls 7/8 D1')
        self.assertDictEqual(result, expected_result)

    def test_division_exception(self):
        with self.assertLogs(level='DEBUG') as cm:
            result = split_grade_gender_division('Girls 7/8')
        self.assertEqual(result, EMPTY_GENDER_GRADE_DIVISION)
        self.assertEqual(cm.output, [
            "WARNING:root:'Girls 7/8' does not have the expected format"
        ]) 

    def test_gender_exception(self):
        with self.assertLogs(level='DEBUG') as cm:
            result = split_grade_gender_division('Girs 7/8 D1')
        self.assertEqual(result, EMPTY_GENDER_GRADE_DIVISION)
        self.assertEqual(cm.output, [
            "WARNING:root:'Girs 7/8 D1', Gender is Invalid"
        ]) 

    def test_grade_exception(self):
        with self.assertLogs(level='DEBUG') as cm:
            result = split_grade_gender_division('Girls H7/8 D1')
        self.assertEqual(result, EMPTY_GENDER_GRADE_DIVISION)
        self.assertEqual(cm.output, [
            "WARNING:root:'Girls H7/8 D1', Grade Level is Invalid"
        ]) 

    def test_extract_team_name_simple(self):
        result = extract_team_name(CONST_TEAM_NAME)
        self.assertEqual(result, CONST_TEAM_NAME)

    def test_extract_team_name_no_leading(self):
        result = extract_team_name('Team-1')
        self.assertEqual(result, CONST_TEAM_NAME)

    def test_extract_team_name_complicated(self):
        result = extract_team_name('Team-01 (Homer/Marge/Bart/Lis')
        self.assertEqual(result, CONST_TEAM_NAME)

    def test_extract_team_name_no_dash(self):
        with self.assertLogs(level='DEBUG') as cm:
            result = extract_team_name('Team01')
        self.assertEqual(result, 'Team01')
        self.assertEqual(cm.output, [
            "WARNING:root:'Team01' is an invalid team name"
        ]) 

    def test_extract_team_name_none(self):
        with self.assertLogs(level='DEBUG') as cm:
            result = extract_team_name('')
        self.assertEqual(result, '')
        self.assertEqual(cm.output, [
            "WARNING:root:'' is an invalid team name"
        ]) 

if __name__ == '__main__':
    test_main()
