#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

#########################
# Standard Library Import
#########################

from unittest import TestCase

from gdelt.dateFuncs import _dateformatter


############################
# Custom Import
############################

class TestDateFormatter(TestCase):
    def test_dateFormatter(self):
        date_string = 'March 22 2016'
        formatter_test = _dateformatter(date_string)
        exp = '2016-03-22'
        self.assertEqual(formatter_test, exp, "_dateformatter working")

