from os import path, getcwd
from unittest import TestCase, main as test_main
from helpers.email import EMailClient, get_email_components

CONST_EMAIL_SERVER = "smtp.example.com"
CONST_EMAIL_EMAIL = "test@example.com"
CONST_EMAIL_NAME = "Test User"
CONST_EMAIL_PORT = 123
CONST_EMAIL_PASSWORD = "badpassword"
CONST_DOMAIN = "example.com"
CONST_ADDRESS = "test"
CONST_TOWN = "Springfield"
CONST_SUBJECT = f"Home Game Schedule for {CONST_TOWN}"
CONST_DATA_NO_MESSAGE = {
    'email': CONST_EMAIL_EMAIL,
    'subject': CONST_SUBJECT,
    'name': CONST_EMAIL_NAME
}
CONST_TEMPLATE_HTML = 'email.html.jinja'
CONST_START_MESSAGE = "DEBUG:helpers.email:Starting create message ..."
CONST_END_MESSAGE = "DEBUG:helpers.email:Completed create message ..."
CONST_DATA_MESSAGE = {
    'subject': CONST_SUBJECT,
    'content': {
        'town': CONST_TOWN,
        'name': 'Homer Simpson'
    }
}


class TestEmailClient(TestCase):
    def test_init(self):
        result = EMailClient(CONST_EMAIL_SERVER, CONST_EMAIL_PORT,
                             CONST_EMAIL_EMAIL, CONST_EMAIL_NAME,
                             CONST_EMAIL_PASSWORD)
        self.assertEqual(result.sender_email, CONST_EMAIL_EMAIL)
        self.assertEqual(result.sender_name, CONST_EMAIL_NAME)
        self.assertEqual(result.password, CONST_EMAIL_PASSWORD)
        self.assertEqual(result.smtp_server, CONST_EMAIL_SERVER)
        self.assertEqual(result.smtp_port, CONST_EMAIL_PORT)

    def test_send_email_missing_subject_content(self):
        data = {}

        email_client = EMailClient(
            CONST_EMAIL_SERVER, CONST_EMAIL_PORT,
            CONST_EMAIL_EMAIL, CONST_EMAIL_NAME,
            CONST_EMAIL_PASSWORD)
        with self.assertLogs(level='DEBUG') as cm:
            result = email_client.send_email(data, CONST_EMAIL_EMAIL,
                                             'no_template')
        self.assertEqual(result, 33)
        self.assertEqual(cm.output, [
            "DEBUG:helpers.email:Starting send email ...",
            "ERROR:helpers.email:'content' is required",
            "ERROR:helpers.email:'subject' is required"
        ])        

    def test_create_message_missing_template(self):
        email_client = EMailClient(
            CONST_EMAIL_SERVER, CONST_EMAIL_PORT,
            CONST_EMAIL_EMAIL, CONST_EMAIL_NAME,
            CONST_EMAIL_PASSWORD)

        with self.assertLogs(level='DEBUG') as cm:
            message = email_client.create_message(CONST_DATA_NO_MESSAGE, 'missing.txt')
        self.assertEqual(cm.output, [
            CONST_START_MESSAGE,
            "ERROR:helpers.email:Missing File: missing.txt",
            CONST_END_MESSAGE
        ])
        self.assertIsNone(message)

    def test_create_email_html(self):
        addresses = "<user one>user.one@example.org,<user two>user.two@example.org"
        email_client = EMailClient(
            CONST_EMAIL_SERVER, CONST_EMAIL_PORT,
            CONST_EMAIL_EMAIL, CONST_EMAIL_NAME,
            CONST_EMAIL_PASSWORD)

        file_name = "send_file.csv"
        full_file_name = path.join(path.dirname(path.realpath(__file__)),
                                   file_name)

        with self.assertLogs(level='DEBUG') as cm:
            message = email_client.create_email(CONST_DATA_MESSAGE,
                                                CONST_TEMPLATE_HTML,
                                                addresses,
                                                full_file_name,
                                                file_name, True)
        self.assertEqual(cm.output, [
            "DEBUG:helpers.email:Starting create email ...",
            CONST_START_MESSAGE,
            CONST_END_MESSAGE,
            "DEBUG:helpers.email:Completed create email ..."
        ])
        self.assertEqual(message._headers[0][0], 'From')
        self.assertEqual(message._headers[0][1],
             f'{CONST_EMAIL_NAME} <{CONST_EMAIL_EMAIL}>')
        self.assertEqual(message._headers[1][0], 'To')
        self.assertEqual(message._headers[1][1],
            'user one <user.one@example.org>, user two <user.two@example.org>')
        self.assertEqual(message._headers[2][0], 'Subject')
        self.assertEqual(message._headers[2][1], CONST_SUBJECT)
        self.assertEqual(message._headers[3][0], 'MIME-Version')
        self.assertEqual(message._headers[3][1], '1.0')

    def test_create_message_html(self):
        with open('src/tests/files/expected_email.txt', 'r') as file:
            expected_msg = file.readline()

        email_client = EMailClient(
            CONST_EMAIL_SERVER, CONST_EMAIL_PORT,
            CONST_EMAIL_EMAIL, CONST_EMAIL_NAME,
            CONST_EMAIL_PASSWORD)

        message = email_client.create_message(CONST_DATA_MESSAGE['content'],
                                                CONST_TEMPLATE_HTML)
        self.assertEqual(message, expected_msg)



class TestEmailComponents(TestCase):
    def test_get_email_components_success(self):
        expected_result = {
            'name': CONST_EMAIL_NAME,
            'address': CONST_ADDRESS,
            'domain': CONST_DOMAIN
        }
        result = get_email_components(f"<{CONST_EMAIL_NAME}>{CONST_EMAIL_EMAIL}")
        self.assertEqual(result, expected_result)

    def test_get_email_components_missing_name(self):
        with self.assertLogs(level='INFO') as cm:
            result = get_email_components(CONST_EMAIL_EMAIL)
        self.assertEqual(cm.output,
                         [f'ERROR:helpers.email:Could not determine name for {CONST_EMAIL_EMAIL}'])
        self.assertEqual(result, {
            'name': None,
            'address': None,
            'domain': None
        })

    def test_get_email_components_invalid_email(self):
        with self.assertLogs(level='INFO') as cm:
            result = get_email_components(f"<{CONST_EMAIL_NAME}>example.com")
        self.assertEqual(cm.output,
                         [f'ERROR:helpers.email:Invalid email address: <{CONST_EMAIL_NAME}>example.com'])
        self.assertEqual(result, {
            'name': CONST_EMAIL_NAME,
            'address': None,
            'domain': None
        })

    def test_get_email_components_invalid_domain(self):
        with self.assertLogs(level='INFO') as cm:
            result = get_email_components(f"<{CONST_EMAIL_NAME}>test@example")
        self.assertEqual(cm.output,
                         [f'ERROR:helpers.email:Invalid domain name: <{CONST_EMAIL_NAME}>test@example'])
        self.assertEqual(result, {
            'name': CONST_EMAIL_NAME,
            'address': CONST_ADDRESS,
            'domain': None
        })


if __name__ == '__main__':
    test_main()
