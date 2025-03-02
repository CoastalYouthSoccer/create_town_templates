from os import environ
import logging
import re
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
            logger.warning(f"'{text}' does not have the expected format")
            return None, None
        
        grade = split_values[0]
        gender = split_values[1]
        
        return grade, gender

    except Exception as e:
        logger.warning(f"An error occurred: {e} splitting {text}")
        return None, None

def split_grade_gender_division(text) -> dict:
    result  = {
        "gender": None,
        "grade": None,
        "division": None
    }

    match = re.match(r'^(\w+)\s+([\d/]+)\s+(.+)$', text)
    if match:
        result["gender"] = match.group(1)  # First word (e.g., 'Boys')
        result["grade"] = f"Grade {match.group(2)}"     # The '7/8' part
        result["division"] = match.group(3)  # The rest ('Division 3' or 'D1')
        if result["gender"].title() not in ('Boys', 'Girls'):
            logger.warning(f"'{text}', Gender is Invalid")
        if match.group(2) not in ('1/2', '3/4', '5/6', '7/8'):
            logger.warning(f"'{text}', Grade Level is Invalid")
        return result
    logger.warning(f"'{text}' does not have the expected format")   
    return result

def extract_team_name(text) -> str:
    match = re.match(r'^([A-Za-z\s-]+)(\d{2})', text)
    if match is None:
        match = re.match(r'^([A-Za-z\s-]+)(\d{1})', text)

    if match:
        # 'Sacred Heart' has a space in it's causing the team name to be converted
        # to 'Sacred-Heart'
        if 'sacred' in match.group(1).strip().lower():
            name = match.group(1).strip()
        else:
            name = match.group(1).strip().replace(" ", "-")  # Replace spaces with hyphens
        number = str(int(match.group(2)))  # Convert '01' to '1'
        if '-' in name:
            return f"{name}{number}"
        else:
            return f"{name}-{number}"
    
    logger.warning(f"'{text}' is an invalid team name")
    return(text)

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
