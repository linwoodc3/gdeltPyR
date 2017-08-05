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

##############################
# Local imports
##############################

from gdelt.inputChecks import _date_input_check
import gdelt




class TestGdeltDateInputs(TestCase):

    def test_gdeltdate_check_v2_fail(self):
        date_sequence = ['2011 10 01', '2016 10 05']
        exp = "GDELT 2.0 only supports 'Feb 18 2015 - Present'queries currently. Try another date."
        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence,version=2)
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception), "Dates for version 2 fail outside of Feb 18 2015")

    def test_gdeltdate_check_v2_fail(self):
        date_sequence = ['2011 10 01', '2016 10 05']
        exp = "GDELT 2.0 only supports 'Feb 18 2015 - Present'queries currently. Try another date."
        with self.assertRaises(Exception) as context:
            checked = _date_input_check(date_sequence,version=2)
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception), "Dates for version 2 fail outside of Feb 18 2015")
