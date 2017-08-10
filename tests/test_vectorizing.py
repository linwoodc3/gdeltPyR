#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##############################
# Standard Library Import
##############################

try:
    from unittest import TestCase, mock
except:
    from unittest import TestCase
    import mock

from unittest import TestCase
import os
import csv
from io import BytesIO,StringIO
from zipfile import ZipFile
import warnings

##############################
# Third Party Libraries
##############################

import pandas as pd
import pandas
import numpy as np
import coveralls

##############################
# Custom Library Import
##############################

from gdelt.vectorizingFuncs import _urlBuilder,_geofilter
# from gdelt.dateFuncs import _gdeltRangeString,_dateRanger
import gdelt


class testGDELTVectorizingFuncs(TestCase):
    def test_gdeltdate_urlbuilder_events_v1_three(self):
        date_sequence = ['20160101234500', '20160102234500', '20160103234500']
        exp = [
            'http://data.gdeltproject.org/events/20160101234500.export.CSV.zip',
            'http://data.gdeltproject.org/events/20160102234500.export.CSV.zip',
            'http://data.gdeltproject.org/events/20160103234500.export.CSV.zip']

        result = _urlBuilder(['20160101234500', '20160102234500',
                              '20160103234500'],version=1)

        return self.assertEqual(exp, result, "Events 1 more than 2 failed.")

    def test_gdeltdate_urlbuilder_events_v1_fail_single(self):
        date_sequence = '201301'

        exp = ("GDELT 1.0 Global Knowledge Graph requires dates greater than "
               "or equal to April 1 2013")

        with self.assertRaises(Exception) as context:
            result = _urlBuilder(date_sequence, version=1, table='gkg')
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception),
                                "Version 1 old, gkg fail.")

    def test_gdeltdate_urlbuilder_events_v1_fail_list(self):
        date_sequence = ['201301', '201302']

        exp = ("GDELT 1.0 Global Knowledge Graph requires dates greater than "
               "or equal to April 1 2013")

        with self.assertRaises(Exception) as context:
            result = _urlBuilder(date_sequence, version=1, table='gkg')
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception),
                                "Version 1 old, gkg fail.")

    def test_gdelt_geofilter_events2(self):
        """Test ability to turn df into geodataframe"""

        # load df
        spam = pd.read_pickle(os.path.join(
            gdelt.base.BASE_DIR, "data", "events2samp.gz"),
            compression="gzip").drop('CAMEOCodeDescription', axis=1)

        try:
            import geopandas as gpd
            geo = _geofilter(spam)

            return self.assertIsInstance(geo,gpd.GeoDataFrame)
        except:
            warnings.warn('Geopandas is not installed. '
                          'Unable to test _geofilter')

            exp = "Blank"
            return self.assertEqual("Blank",exp)
