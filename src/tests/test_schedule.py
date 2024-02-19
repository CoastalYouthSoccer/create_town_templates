from unittest import TestCase, main as test_main
from schedule import get_arguments

USAGE='USAGE: schedule.py -f <assignor file>' 


class TestSchedule(TestCase):
    def test_get_arguments_help(self):
        with self.assertLogs(level='INFO') as cm:
            rc, args = get_arguments(['-h'])
        self.assertEqual(cm.output, [f"ERROR:schedule:{USAGE}"])
        self.assertEqual(rc, 99)
        self.assertEqual(args, {'file_name': None})

    def test_valid_options(self):
        rc, args = get_arguments(['-f', 'fileName.csv'])
        self.assertEqual(rc, 0)
        self.assertEqual(args, {'file_name': 'fileName.csv'})

    def test_no_file_name(self):
        rc, args = get_arguments(['-f'])
        self.assertEqual(rc, 88)
        self.assertEqual(args, {'file_name': None})


if __name__ == '__main__':
    test_main()
