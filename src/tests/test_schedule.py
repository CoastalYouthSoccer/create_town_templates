from unittest import TestCase, main as test_main
from schedule import get_arguments

USAGE = "USAGE: schedule.py -f <assignor file> -e <Excel format flag (True/False)>"


class TestSchedule(TestCase):
    def test_get_arguments_help(self):
        with self.assertLogs(level="INFO") as cm:
            rc, args = get_arguments(["-h"])
        self.assertEqual(cm.output, [f"ERROR:schedule:{USAGE}"])
        self.assertEqual(rc, 99)
        self.assertEqual(args, {"file_name": None,
                                "excel_format": False})

    def test_valid_options(self):
        rc, args = get_arguments(["-f", "fileName.csv", "-e", "true"])
        self.assertEqual(rc, 0)
        self.assertEqual(args, {"file_name": "fileName.csv",
                                "excel_format": True})

    def test_valid_options_yes(self):
        rc, args = get_arguments(["-f", "fileName.csv", "-e", "yes"])
        self.assertEqual(rc, 0)
        self.assertEqual(args, {"file_name": "fileName.csv",
                                "excel_format": True})

    def test_valid_options_excel_default(self):
        rc, args = get_arguments(["-f", "fileName.csv"])
        self.assertEqual(rc, 0)
        self.assertEqual(args, {"file_name": "fileName.csv",
                                "excel_format": False})

    def test_no_file_name(self):
        rc, args = get_arguments(['-f'])
        self.assertEqual(rc, 77)
        self.assertEqual(args, {"file_name": None,
                                "excel_format": False})


if __name__ == '__main__':
    test_main()
