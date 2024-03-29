from os import (environ, path)
from sys import (argv, exit, stdout)
from getopt import (getopt, GetoptError)

from dotenv import load_dotenv
import logging
import json
from helpers.helpers import (get_email_vars, get_spreadsheet_vars)
from classes.master_schedule import MasterSchedule
from helpers.email import EMailClient

env_file = environ.get('ENV_FILE', '.env')
load_dotenv(env_file)

log_level = environ.get('LOG_LEVEL', logging.INFO)
logging.basicConfig(stream=stdout,
                    level=int(log_level))
logger = logging.getLogger(__name__)

BASE_DIR = path.dirname(path.realpath(__file__))

def get_arguments(args):
    arguments = {
        'file_name': None
    }

    rc = 0
    USAGE='USAGE: schedule.py -f <assignor file>' 

    try:
        opts, args = getopt(args,"hf:",
                            ["file-name="])
    except GetoptError:
        logger.error(USAGE)
        return 77, arguments

    for opt, arg in opts:
        if opt == '-h':
            logger.error(USAGE)
            return 99, arguments
        elif opt in ("-f", "--file-name"):
            arguments['file_name'] = arg


    if arguments['file_name'] is None:
        logger.error(USAGE)
        return 88

    return rc, arguments

def main():
    logger.info("Starting Schedule Report")
    rc, args = get_arguments(argv[1:])
    if rc:
        exit(rc)

    with open(args['file_name']) as assignor_file:
        assignor_list = json.load(assignor_file)


#    rc, spreadsheet_vars = get_spreadsheet_vars()
#    if rc:
#        exit(rc)

    rc, email_vars = get_email_vars()
    if rc:
        exit(rc)

    email_client = EMailClient(
        email_vars['EMAIL_SERVER'], email_vars['EMAIL_PORT'],
        email_vars['EMAIL_EMAIL'], email_vars['EMAIL_USERNAME'],
        email_vars['EMAIL_PASSWORD'])



#    master_schedule = MasterSchedule(spreadsheet_vars['SPREADSHEET_ID'],
#                                    spreadsheet_vars['SPREADSHEET_RANGE'])
#    master_schedule.read_schedule

    for town in assignor_list.keys():
        content = {
            "subject": f"Home Game Schedule for {town}",
            "content": {
                "town": town,
                "name": assignor_list[town]["first_name"]
            }
        }
        file_name = path.join(BASE_DIR, f"{town}.csv")
        assignor = f"{assignor_list[town]['first_name']}" \
            f" {assignor_list[town]['last_name']}"
        assignor_email = f"<{assignor}>{assignor_list[town]['email']}"
#        town_file = master_schedule.write_schedule(file_name, town,
#                                                   assignor)
        email_client.send_email(content, "email.html.jinja",
                                 assignor_email, file_name,
                                 f"{town}.csv", True)


if __name__ == "__main__":
    main()
