from os import environ
import logging
from google import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def load_sheet(sheet_id, sheet_range) -> list:
    credentials, _ = auth.default()
    sheet_values = []

    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=sheet_id, range=sheet_range).execute()
        sheet_values = result.get('values', [])
        logger.info(f"{len(sheet_values)} rows retrieved")
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
    
    return sheet_values

def get_spreadsheet_vars():
    rc = 0
    env_vars = {
        'SPREADSHEET_ID': None,
        'SPREADSHEET_RANGE': None,
        'GOOGLE_APPLICATION_CREDENTIALS': None
    }

    try:
        env_vars['GOOGLE_APPLICATION_CREDENTIALS'] = environ['GOOGLE_APPLICATION_CREDENTIALS']
    except KeyError:
        logger.error('GOOGLE_APPLICATION_CREDENTIALS environment variable is missing')
        rc = 55

    try:
        env_vars['SPREADSHEET_ID'] = environ['SPREADSHEET_ID']
    except KeyError:
        logger.error('SPREADSHEET_ID environment variable is missing')
        rc = 55

    try:
        env_vars['SPREADSHEET_RANGE'] = environ['SPREADSHEET_RANGE']
    except KeyError:
        logger.error('SPREADSHEET_RANGE environment variable is missing')
        rc = 55

    return rc, env_vars

def get_email_vars():
    rc = 0
    env_vars = {
        'EMAIL_SERVER': 'smtp.gmail.com',
        'EMAIL_PORT': 587,
        'EMAIL_USERNAME': None,
        'EMAIL_EMAIL': None,
        'EMAIL_PASSWORD': None
    }

    try:
        env_vars['EMAIL_SERVER'] = environ['EMAIL_SERVER']
    except KeyError:
        logger.info('EMAIL_SERVER environment variable is missing, defaulting to "smtp.gmail.com"')

    try:
        env_vars['EMAIL_PORT'] = int(environ['EMAIL_PORT'])
    except KeyError:
        logger.info('EMAIL_PORT environment variable is missing, defaulting to 587')
    except ValueError:
        logger.error('EMAIL_PORT environment variable is not an integer')
        rc = 55

    try:
        env_vars['EMAIL_USERNAME'] = environ['EMAIL_USERNAME']
    except KeyError:
        logger.error('EMAIL_USERNAME environment variable is missing')
        rc = 55

    try:
        env_vars['EMAIL_EMAIL'] = environ['EMAIL_EMAIL']
    except KeyError:
        logger.error('EMAIL_EMAIL environment variable is missing')
        rc = 55

    try:
        env_vars['EMAIL_PASSWORD'] = environ['EMAIL_PASSWORD']
    except KeyError:
        logger.error('EMAIL_PASSWORD environment variable is missing')
        rc = 55

    return rc, env_vars
