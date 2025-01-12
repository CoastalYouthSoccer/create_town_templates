from os import environ
import logging
import gspread
from google import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io
import pandas as pd

logger = logging.getLogger()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def split_grade_and_gender(text):
    try:
        split_values = text.rsplit(' ', 1)
        
        if len(split_values) != 2:
<<<<<<< HEAD
            raise ValueError("String does not have the expected format")
=======
            logger.warning(f"'{text}' does not have the expected format")
            return None, None
>>>>>>> origin/main
        
        grade = split_values[0]
        gender = split_values[1]
        
        return grade, gender

    except Exception as e:
<<<<<<< HEAD
        print(f"An error occurred: {e} splitting {text}")
        return None, None
    
=======
        logger.warning(f"An error occurred: {e} splitting {text}")
        return None, None

def split_grade_gender_division(text) -> dict:
    empty  = {
        "gender": None,
        "grade": None,
        "division": None
    }

    split_values = text.rsplit(' ')
        
    if len(split_values) != 3:
        logger.warning(f"'{text}' does not have the expected format")
        return empty

    if split_values[0].title() not in ('Boys', 'Girls'):
        logger.warning(f"'{text}', Gender is Invalid")
        return empty

# What's the value(s) for high school
    if split_values[1] not in ('1/2', '3/4', '5/6', '7/8'):
        logger.warning(f"'{text}', Grade Level is Invalid")
        return empty

    return {
        "gender": split_values[0].title(),
        "grade": f"Grade {split_values[1]}",
        "division": split_values[2]
    }

def extract_team_name(text) -> str:
    split_values = text.rsplit(' ')
    if len(split_values) < 1 or '-' not in split_values[0]:
        logger.warning(f"'{text}' is an invalid team name")
        return(text)
    
    return split_values[0].replace("-0", "-")

>>>>>>> origin/main
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

def load_excel_sheet(sheet_id, sheet_range) -> list:
    sheet_name = sheet_range.split('!')[0]
    credentials, _ = auth.default()
    sheet_values = []

    try:
        _ = gspread.authorize(credentials)
        service = build('drive', 'v3', credentials=credentials)
        request = service.files().get_media(fileId=sheet_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()

        fh.seek(0)

        df = pd.read_excel(fh, sheet_name=sheet_name)
        df["HOME#"] = df["HOME#"].astype('string')
        df["AWAY#"] = df["AWAY#"].astype('string')
        df["DATE"] = df["DATE"].astype('string')

        sheet_values = df.values.tolist()

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
