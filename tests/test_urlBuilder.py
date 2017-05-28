#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com


from unittest import TestCase
import numpy as np
from gdelt.dateFuncs import gdeltRangeString, dateRanger
from gdelt.vectorizingFuncs import urlBuilder


class TestUrlBuilder(TestCase):
    def test_urlbuilder_v1(self):
        date_sequence = '2016 10 01'
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = urlBuilder(gdeltstring_output, version=1)
        exp = 'http://data.gdeltproject.org/events/20161001.export.CSV.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")



    def test_urlbuilder_v2(self):
        date_sequence = '2016 10 01'
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = urlBuilder(gdeltstring_output, version=2)
        exp = 'http://data.gdeltproject.org/gdeltv2/20161001234500.export.CSV.zip'

        return self.assertEqual(exp, urlbuilder_test, "Version 2 Url works.")

    def test_urlbuilder_v3(self):
        date_sequence = '2013 Mar 01'
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = urlBuilder(gdeltstring_output, version=1)
        exp = 'http://data.gdeltproject.org/events/201303.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    def test_urlbuilder_v4(self):
        date_sequence = '2001 Mar 01'
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = urlBuilder(gdeltstring_output, version=1)
        exp = 'http://data.gdeltproject.org/events/2001.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    def test_urlbuilder_v5(self):
        date_sequence = '2013 Apr 01'
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = urlBuilder(gdeltstring_output, table='gkg',version=1)
        exp = 'http://data.gdeltproject.org/gkg/20130401.gkg.csv.zip'
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    # def test_urlbuilder_graph2_fail(self):
    #     """Testing broken query if table is graph and date is less than Feb 18 2015"""
    #     date_sequence = '2013 Apr 01'
    #     ranger_output = dateRanger(date_sequence)
    #     gdeltstring_output = gdeltRangeString(ranger_output, version=2)
    #     exp = 'GDELT 2.0 Global Knowledge Graph requires dates greater than or equal to Feb 18 2015 11 pm.'
    #     with self.assertRaises(Exception) as context:
    #         urlBuilder(gdeltstring_output, table='gkg', version=2)
    #     # urlBuilder(gdeltstring_output, table='gkg', version=2)
    #     the_exception = context.exception
    #     return self.assertEquals(exp, str(the_exception), "graph version 2 failes outside of Feb 18 2015 11pm")

    def test_urlbuilder_graph2_pass(self):
        date_sequence = '2015 Apr 01'
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = urlBuilder(gdeltstring_output, table='gkg', version=2)
        exp = 'http://data.gdeltproject.org/gdeltv2/20150401234500.gkg.csv.zip'
        # print(urlbuilder_test)
        return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    def test_urlbuilder_events2_passlist(self):
        date_sequence = ['2015 Apr 01','2015 Apr 02']
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=2)
        urlbuilder_test = urlBuilder(gdeltstring_output, table='events', version=2)
        exp = np.sort(np.array(['http://data.gdeltproject.org/gdeltv2/20150401234500.export.CSV.zip',
                                'http://data.gdeltproject.org/gdeltv2/20150402234500.export.CSV.zip']))
        return np.testing.assert_array_equal(exp, np.sort(np.array(gdeltstring_test)))
        # return self.assertEqual(exp, urlbuilder_test, "Version 1 Url works.")

    # def test_urlbuilder_events2_faillist(self):
    #     date_sequence = ['2001 Jan 01','2002 Apr 02']
    #     ranger_output = dateRanger(date_sequence)
    #     gdeltstring_output = gdeltRangeString(ranger_output, version=2)
    #     urlbuilder_test = urlBuilder(gdeltstring_output, table='events', version=2)
    #     exp =  ['http://data.gdeltproject.org/gdeltv2/20150401234500.export.CSV.zip',
    #             'http://data.gdeltproject.org/gdeltv2/20150402234500.export.CSV.zip']
    #     # print(urlbuilder_test)
    #     return self.assertEquals(exp, urlbuilder_test, "Version 1 Url works.")

    def test_urlbuilder_events1_passlist(self):
        date_sequence = ['2015 Apr 01', '2015 Apr 02']
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = urlBuilder(gdeltstring_output, table='events', version=1)
        exp = np.sort(np.array(['http://data.gdeltproject.org/events/20150401.export.CSV.zip',
                                'http://data.gdeltproject.org/events/20150402.export.CSV.zip']))
        # print(urlbuilder_test)
        return self.assertEqual(exp, np.sort(np.array(urlbuilder_test)), "Version 1 Url works.")
