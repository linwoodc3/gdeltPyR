#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

#########################
# Standard Library Import
#########################
import datetime
from unittest import TestCase

#########################
# Third Party Import
#########################

import numpy as np
import coveralls


############################
# Custom Import
############################

from gdelt.dateFuncs import dateRanger


class TestDateRanger(TestCase):
    def test_dateRanger_sequence(self):
        date_sequence = ['2016 10 01', '2016 10 05']
        ranger_test = dateRanger(date_sequence)
        exp = (np.array([datetime.datetime(2016, 10, 1, 0, 0),
                         datetime.datetime(2016, 10, 2, 0, 0),
                         datetime.datetime(2016, 10, 3, 0, 0),
                         datetime.datetime(2016, 10, 4, 0, 0),
                         datetime.datetime(2016, 10, 5, 0, 0)], dtype=object))
        return np.testing.assert_array_equal(exp, ranger_test)

    def test_dateRanger_single_list(self):
        date_sequence = ['2016 10 01']
        ranger_test = dateRanger(date_sequence)
        exp = (np.array(datetime.datetime(2016, 10, 1, 0, 0), dtype=object))
        return np.testing.assert_array_equal(exp, ranger_test)

    def test_dateRanger_single_string(self):
        date_string = '2016 10 01'
        ranger_test = dateRanger(date_string)
        exp = (np.array(datetime.datetime(2016, 10, 1, 0, 0), dtype=object))
        return np.testing.assert_array_equal(exp, ranger_test)
