import datetime
from unittest import TestCase

from gdelt.dateFuncs import parse_date


class TestParse_date(TestCase):
    def test_parse_date(self):
        date_string = '2016 10 01'
        parsed_test = parse_date(date_string)
        exp = datetime.datetime(2016, 10, 1, 0, 0)
        self.assertEqual(parsed_test, exp)

    def test_parse_date_fail(self):
        date_string = 'random string'
        parsed_test = parse_date(date_string)
        exp = 'You entered an incorrect date.  Check your date format.'
        self.assertEqual(parsed_test, exp)
