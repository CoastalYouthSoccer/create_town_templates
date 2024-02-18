from os import path
from unittest import TestCase, main as test_main
from unittest.mock import (patch, MagicMock)
from helpers.email import EMailClient, get_email_components

CONST_EMAIL_SERVER = "smtp.example.com"
CONST_EMAIL_EMAIL = "test@example.com"
CONST_EMAIL_NAME = "Test User"
CONST_EMAIL_PORT = 123
CONST_EMAIL_PASSWORD = "badpassword"
CONST_DOMAIN = "example.com"
CONST_ADDRESS = "test"


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
