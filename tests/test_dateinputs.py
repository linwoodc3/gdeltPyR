#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##############################
# Standard Library imports
##############################

import datetime
from unittest import TestCase

##############################
# Third party imports
##############################

import coveralls
import numpy as np
from dateutil.parser import parse

##############################
# Local imports
##############################

from gdelt.inputChecks import _date_input_check
from gdelt.dateFuncs import _dateRanger,_gdeltRangeString


class TestGdeltDateInputs(TestCase):
    def test_gdeltdate_check_v2_fail(self):
        date_sequence = ['2011 10 01', '2016 10 05']
        exp = "GDELT 2.0 only supports 'Feb 18 2015 - Present'queries " \
              "currently. Try another date."
        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence, version=2)
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception), "Dates for version 2 "
                                                         "fail outside of "
                                                         "Feb 18 2015")

    def test_gdeltdate_check_v2_fail_firstgreater(self):
        date_sequence = ['2017 Feb 01','2016 Feb 29']
        exp = ("Start date greater than or equal to end date. Check your "
               "entered date query.")
        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence, version=2)
        the_exception = context.exception

        return self.assertEqual(exp, str(the_exception), "Dates for version"
                                                         " 2 fail outside of "
                                                         "Feb 18 2015")

    def test_gdeltdate_check_v1_fail_current(self):
        date_sequence = str(datetime.datetime.now().date())
        exp = ("You entered today's date for a GDELT 1.0 query. GDELT 1.0's "
               "most recent data is always the trailing day (i.e. "
               "2017-08-11).  Please retry your query.")

        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence, version=1)
        the_exception = context.exception
        print(the_exception)
        return self.assertEqual(exp, str(the_exception), "Too early date "
                                                         "on Version 1")

    def test_gdeltdate_greater_current(self):
        date_sequence = str(datetime.datetime.now().date() + datetime. \
                            timedelta(days=1))
        exp = ('Your date is greater than the current date. '
               'Please enter a relevant date.')
        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence, version=2)
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception), "GDELT can't pull "
                                                         "from the future "
                                                         "error.")

    def test_gdeltdate_old(self):
        date_sequence = str(
            parse('1999 Jan 12').date())

        checked = _date_input_check(date_sequence, version=1)
        return self.assertIsNone(checked, "GDELT can't pull from the "
                                          "future error.")

    def test_gdeltdate_veryold(self):
        date_sequence = ['1982', '1983', '1984'
                         ]
        exp = ('Your date is greater than the current date. '
               'Please enter a relevant date.')

        checked = _date_input_check(date_sequence, version=1)
        return self.assertIsNone(checked, "GDELT can't pull from the "
                                          "future error.")

    def test_gdeltdate_second_greater(self):
        date_sequence = ['2017 Jun 20', '1989 Feb 1']
        exp = ('Start date greater than or equal to end date. '
               'Check your entered date query.')
        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence, version=1)
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception), "Second greater")

    def test_gdeltdate_greater_currentlist(self):
        date_sequence = [(str(datetime.datetime.now().date() + datetime. \
                              timedelta(days=1)))]

        exp = ("One or more of your input date strings does not parse to "
               "a date format. Check input.")
        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence, version=2)
        the_exception = context.exception

        return self.assertEqual(exp, str(the_exception))

    def test_gdeltdate_6am_list(self):
        date_sequence = list(map(lambda x: str(parse(x)),
                                 ['2014 Jun 13', '2016 Feb 1', '2017 Jan 22']))

        exp = ("One or more of your input date strings does not parse to "
               "a date format. Check input.")

        checked = _date_input_check(date_sequence, version=1)

        return self.assertIsNone(checked)

    def test_gdeltdate_greater_current(self):
        holder = (datetime.datetime.now()+datetime.timedelta(days=2))
        date_sequence = list(map(lambda x: str(parse(x)),
                                 ['2016 Feb 1', '{}'.format(str(holder))]))

        exp = ("One of your dates is greater than the current date. Check "
               "your entered date query.")

        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence, version=2)
        the_exception = context.exception

        return self.assertEqual(exp,str(the_exception),'Not greater')


    def test_gdeltdate_two_v2_tooearly(self):

        date_sequence = np.asarray(['2016 Jan 2', '2013 Jan 31','2015 Jan 1'])

        exp = ("GDELT 2.0 only supports \'Feb 18 2015 - Present\'queries "
               "currently. Try another date.")

        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence, version=2)
        the_exception = context.exception

        return self.assertEqual(exp,str(the_exception),'Not greater')

    # @mock.patch.object(gdelt.inputChecks._date_input_check.datetime.datetime, 'now')
    # def test_gdeltdate_6am_v1(self):
    #     holder = (datetime.datetime.now()+datetime.timedelta(days=2))
    #     date_sequence = list(map(lambda x: str(parse(x)),
    #                              ['2016 Feb 1', '{}'.format(str(holder))]))
    #
    #     exp = ("One of your dates is greater than the current date. Check "
    #            "your entered date query.")
    #
    #     with self.assertRaises(Exception) as context:
    #         checked = _date_input_check(date_sequence, version=2)
    #     the_exception = context.exception
    #
    #     return self.assertEqual(exp,str(the_exception),'Not greater')


