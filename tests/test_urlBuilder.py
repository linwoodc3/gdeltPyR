#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##############################
# Standard library imports
##############################
from unittest import TestCase

##############################
# Third party imports
##############################
import numpy as np

##############################
# Local imports
##############################
from gdelt.dateFuncs import _gdeltRangeString, _dateRanger
from gdelt.vectorizingFuncs import _urlBuilder


class TestUrlBuilder(TestCase):
    def test_urlbuilder_v1(self):
        date_sequence = '2016 10 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = _urlBuilder(gdeltstring_output, version=1)
        exp = 'http://data.gdeltproject.org/events/20161001.export.CSV.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    def test_urlbuilder_v2(self):
        date_sequence = '2016 10 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = _urlBuilder(gdeltstring_output, version=2)
        exp = 'http://data.gdeltproject.org/gdeltv2/20161001234500.export.CSV.zip'

        return self.assertEqual(exp, urlbuilder_test, "Version 2 Url works.")

    def test_urlbuilder_v2_translation(self):
        date_sequence = '2016 10 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = _urlBuilder(gdeltstring_output, version=2, translation=True)
        exp = 'http://data.gdeltproject.org/gdeltv2/20161001234500.translation.export.CSV.zip'

        return self.assertEqual(exp, urlbuilder_test, "Version 2 Url works.")

    def test_urlbuilder_v3(self):
        date_sequence = '2013 Mar 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = _urlBuilder(gdeltstring_output, version=1)
        exp = 'http://data.gdeltproject.org/events/201303.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    def test_urlbuilder_v4(self):
        date_sequence = '2001 Mar 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = _urlBuilder(gdeltstring_output, version=1)
        exp = 'http://data.gdeltproject.org/events/2001.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    def test_urlbuilder_v5(self):
        date_sequence = '2013 Apr 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = _urlBuilder(gdeltstring_output, table='gkg',version=1)
        exp = 'http://data.gdeltproject.org/gkg/20130401.gkg.csv.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    def test_urlbuilder_graph2_pass(self):
        date_sequence = '2015 Apr 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = _urlBuilder(gdeltstring_output, table='gkg', version=2)
        exp = 'http://data.gdeltproject.org/gdeltv2/20150401234500.gkg.csv.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 2 Url works.")

    def test_urlbuilder_graph2_pass_translation(self):
        date_sequence = '2015 Apr 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = _urlBuilder(gdeltstring_output, table='gkg', version=2, translation=True)
        exp = 'http://data.gdeltproject.org/gdeltv2/20150401234500.translation.gkg.csv.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 2 Url works with translation.")

    def test_urlbuilder_events2_passlist(self):
        date_sequence = ['2015 Apr 01','2015 Apr 02']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = _urlBuilder(gdeltstring_output, table='events', version=2)
        exp = np.sort(np.array(['http://data.gdeltproject.org/gdeltv2/20150401234500.export.CSV.zip',
                                'http://data.gdeltproject.org/gdeltv2/20150402234500.export.CSV.zip']))
        return np.testing.assert_array_equal(np.sort(np.array(urlbuilder_test)), np.sort(np.array(exp)))

    def test_urlbuilder_events2_passlist_translation(self):
        date_sequence = ['2015 Apr 01','2015 Apr 02']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = _urlBuilder(gdeltstring_output, table='events', version=2, translation=True)
        exp = np.sort(np.array(['http://data.gdeltproject.org/gdeltv2/20150401234500.translation.export.CSV.zip',
                                'http://data.gdeltproject.org/gdeltv2/20150402234500.translation.export.CSV.zip']))
        return np.testing.assert_array_equal(np.sort(np.array(urlbuilder_test)), np.sort(np.array(exp)))

    def test_urlbuilder_events1_passlist(self):
        date_sequence = ['2015 Apr 01', '2015 Apr 02']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_output = _gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = _urlBuilder(gdeltstring_output, table='events', version=1)
        exp = np.sort(np.array(['http://data.gdeltproject.org/events/20150401.export.CSV.zip',
                                'http://data.gdeltproject.org/events/20150402.export.CSV.zip']))
        return np.testing.assert_array_equal(np.sort(np.array(exp)), np.sort(np.array(urlbuilder_test)))
