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

import numpy as np

from gdelt.dateFuncs import _dateRanger


#########################
# Third Party Import
#########################
############################
# Custom Import
############################


class TestDateRanger(TestCase):
    def test_dateRanger_sequence(self):
        date_sequence = ['2016 10 01', '2016 10 05']
        ranger_test = _dateRanger(date_sequence)
        exp = (np.array([datetime.datetime(2016, 10, 1, 0, 0),
                         datetime.datetime(2016, 10, 2, 0, 0),
                         datetime.datetime(2016, 10, 3, 0, 0),
                         datetime.datetime(2016, 10, 4, 0, 0),
                         datetime.datetime(2016, 10, 5, 0, 0)], dtype=object))
        return np.testing.assert_array_equal(exp, ranger_test)

    def test_dateRanger_single_list(self):
        date_sequence = ['2016 10 01']
        ranger_test = _dateRanger(date_sequence)
        exp = (np.array(datetime.datetime(2016, 10, 1, 0, 0), dtype=object))
        return np.testing.assert_array_equal(exp, ranger_test)

    def test_dateRanger_single_string(self):
        date_string = '2016 10 01'
        ranger_test = _dateRanger(date_string)
        exp = (np.array(datetime.datetime(2016, 10, 1, 0, 0), dtype=object))
        return np.testing.assert_array_equal(exp, ranger_test)

    def test_separate_dates(self):
        """Tests more than 3 dates"""

        date_sequence = ['2016 Jun 10','2016 Jun 15','2016 Jun 25']
        ranger_test = _dateRanger(date_sequence)
        exp = (np.array([datetime.datetime(2016, 6, 10, 0, 0),
               datetime.datetime(2016, 6, 15, 0, 0),
               datetime.datetime(2016, 6, 25, 0, 0)], dtype=object))
        return np.testing.assert_array_equal(exp, ranger_test)






