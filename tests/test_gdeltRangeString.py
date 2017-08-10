#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

#########################
# Standard Library Import
#########################

from unittest import TestCase

#########################
# Third Party Import
#########################

import coveralls
import pandas as pd
from dateutil.parser import parse

############################
# Custom Import
############################

from gdelt.dateFuncs import _dateRanger, _gdeltRangeString
from gdelt.inputChecks import *


class TestGdeltRangeString(TestCase):
    def test_gdeltrange_sequence_v1(self):
        date_sequence = ['2016 10 01', '2016 10 05']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_test = np.sort(_gdeltRangeString(ranger_output, version=1))
        exp = np.sort(np.array(['20161003', '20161001', '20161002', '20161005', '20161004']))
        np.testing.assert_array_equal(exp, gdeltstring_test)

    def test_gdeltrange_nearest_single(self):
        date_string = _dateRanger([str((datetime.datetime.now()).date())])
        ranger_test = _gdeltRangeString(date_string,coverage=False,version=2)
        # build time range including 30 minutes before and 30 after current
        r = pd.date_range(
            datetime.datetime.now() - datetime.timedelta(minutes=30),
            datetime.datetime.now() + datetime.timedelta(minutes=30),
            freq='15min')
        return self.assertTrue(r[0]<parse(ranger_test) < r[-1])

    def test_gdeltrange_nearest_full(self):
        date_string = _dateRanger([str((datetime.datetime.now()).date())])
        ranger_test = _gdeltRangeString(date_string,coverage=True,version=2)

        # convert result to array of python datetimes

        vect = np.vectorize(parse)
        comp = vect(ranger_test)

        # build time range of all day up to latest 15 minute interval
        # convert to pydatetime array
        exp = (pd.date_range(start=str(datetime.datetime.now().date()),
                            periods=len(ranger_test), freq='15 min')).\
            to_pydatetime()

        # compare arrays
        return np.testing.assert_array_equal(comp, exp, 'Not equal')


    def test_gdeltrange_sequence_v2_single_string(self):
        date_sequence = '2016 10 01'
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_test = _gdeltRangeString(ranger_output, version=2)
        exp = '20161001234500'
        return self.assertEqual(exp, gdeltstring_test)

    def test_gdeltrange_sequence_v2_single_tester(self):
        date_sequence = ['2016 10 01','2016 Dec 31']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_test = _gdeltRangeString(ranger_output, coverage=True, version=2)
        print(gdeltstring_test.dtype)
        return self.assertIsInstance(gdeltstring_test,np.ndarray)

    def test_gdeltrange_sequence_v2(self):
        date_sequence = ['2016 10 01', '2016 10 05']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_test = np.sort(np.array(_gdeltRangeString(ranger_output, version=2)))
        exp = np.sort(np.array(['20161001234500',
                                '20161002234500',
                                '20161003234500',
                                '20161004234500',
                                '20161005234500']))
        np.testing.assert_array_equal(exp, gdeltstring_test)

    def test_gdeltrange_sequence_v2_with_coverage(self):
        date_sequence = ['2016 10 01']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_test = np.sort(np.array(_gdeltRangeString(ranger_output, coverage=True, version=2)))
        exp = np.sort(np.array(['20161001000000', '20161001001500', '20161001003000',
                                '20161001004500', '20161001010000', '20161001011500',
                                '20161001013000', '20161001014500', '20161001020000',
                                '20161001021500', '20161001023000', '20161001024500',
                                '20161001030000', '20161001031500', '20161001033000',
                                '20161001034500', '20161001040000', '20161001041500',
                                '20161001043000', '20161001044500', '20161001050000',
                                '20161001051500', '20161001053000', '20161001054500',
                                '20161001060000', '20161001061500', '20161001063000',
                                '20161001064500', '20161001070000', '20161001071500',
                                '20161001073000', '20161001074500', '20161001080000',
                                '20161001081500', '20161001083000', '20161001084500',
                                '20161001090000', '20161001091500', '20161001093000',
                                '20161001094500', '20161001100000', '20161001101500',
                                '20161001103000', '20161001104500', '20161001110000',
                                '20161001111500', '20161001113000', '20161001114500',
                                '20161001120000', '20161001121500', '20161001123000',
                                '20161001124500', '20161001130000', '20161001131500',
                                '20161001133000', '20161001134500', '20161001140000',
                                '20161001141500', '20161001143000', '20161001144500',
                                '20161001150000', '20161001151500', '20161001153000',
                                '20161001154500', '20161001160000', '20161001161500',
                                '20161001163000', '20161001164500', '20161001170000',
                                '20161001171500', '20161001173000', '20161001174500',
                                '20161001180000', '20161001181500', '20161001183000',
                                '20161001184500', '20161001190000', '20161001191500',
                                '20161001193000', '20161001194500', '20161001200000',
                                '20161001201500', '20161001203000', '20161001204500',
                                '20161001210000', '20161001211500', '20161001213000',
                                '20161001214500', '20161001220000', '20161001221500',
                                '20161001223000', '20161001224500', '20161001230000',
                                '20161001231500', '20161001233000', '20161001234500'],
                               dtype='<U14'))
        np.testing.assert_array_equal(exp, gdeltstring_test)

    def test_gdeltrange_sequence_v1_2013(self):
        date_sequence = ['2013 Feb 01', '2013 Feb 05']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_test = np.sort(np.array(_gdeltRangeString(ranger_output, version=1)))
        exp = np.array(['201302'])
        np.testing.assert_array_equal(exp, gdeltstring_test)


    def test_gdeltrange_sequence_v1_2005(self):
        date_sequence = ['2001 Feb 01', '2005 Feb 05']
        ranger_output = _dateRanger(date_sequence)
        gdeltstring_test = np.sort(np.array(_gdeltRangeString(ranger_output, version=1)))
        exp = np.sort(np.array(['2001', '2002', '2003', '2004', '2005']))
        np.testing.assert_array_equal(exp, gdeltstring_test)

    def test_separate_rangestring_24hours(self):
        """Tests more than 3 dates"""

        date_array = np.array(datetime.datetime(2017, 8, 6, 0, 0), dtype=object)
        bottom_number = (datetime.datetime.now().time().hour)*4
        ranger_test = _gdeltRangeString(date_array,coverage=True)

        return self.assertGreaterEqual((ranger_test).shape[0],bottom_number)

