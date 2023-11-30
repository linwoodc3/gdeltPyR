#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##############################
# Standard Library Import
##############################

import platform
try:
    from unittest import TestCase, mock
except:
    from unittest import TestCase
    import mock

import os
from unittest import TestCase

import pandas as pd

import gdelt
from gdelt.vectorizingFuncs import _urlBuilder, _geofilter

##############################
# Third Party Libraries
##############################

try:
    import geopandas
except:
    print('geopandas not installed')

##############################
# Custom Library Import
##############################


#################################
# Test files
#################################

# can't read compressed pickles in old pandas version
try:
    test_df = pd.read_pickle(os.path.join(
        gdelt.base.BASE_DIR, "data", "events2samp.gz"),
        compression="gzip").drop('CAMEOCodeDescription', axis=1)

except:

    if platform.python_version_tuple()[1] == '4':
        import gzip
        import tempfile

        fh = gzip.GzipFile(os.path.join(
            gdelt.base.BASE_DIR, "data", "events2samp.gz"))
        with tempfile.NamedTemporaryFile() as tmp:
            lines = fh.read()
            tmp.write(lines)
            test_df = pd.read_pickle(tmp.name)

    else:
        test_df = pd.read_pickle(os.path.join(
            gdelt.base.BASE_DIR, "data", "events2samp.gz"),
            compression="gzip").drop('CAMEOCodeDescription', axis=1)


class testGDELTVectorizingFuncs(TestCase):

    # print(test_df)

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

    # def test_gdelt_geofilter_events2(self):
    #     """Test ability to turn df into geodataframe"""
    #
    #     # load df
    #     spam = pd.read_pickle(os.path.join(
    #         gdelt.base.BASE_DIR, "data", "events2samp.gz"),
    #         compression="gzip").drop('CAMEOCodeDescription', axis=1)
    #     # print(spam)
    #
    #     try:
    #         import geopandas as gpd
    #         geo = _geofilter(spam)
    #
    #         return self.assertIsInstance(geo,gpd.GeoDataFrame)
    #     except:
    #         warnings.warn('Geopandas is not installed. '
    #                       'Unable to test _geofilter')
    #
    #         exp = "Blank"
    #         return self.assertEqual("Blank",exp)
    def test_geopandas_import_pass(self):
        """Test ability to import geopandas and create spatial object"""
        #import geopandas as gpd

        # exp = "geopandas is not installed. gdeltPyR needs geopandas to export as shapefile. Visit http://geopandas.org/install.html for instructions."
        import geopandas as gpd
        gdf = _geofilter(test_df)

        return self.assertTrue(isinstance(gdf, gpd.geodataframe.GeoDataFrame))

    def test_geopandas_import_pass_normcol(self):
        import geopandas as gpd
        test_df.columns = list(
            map(lambda x: (x.replace('_', "")).lower(), test_df.columns))
        gdf = _geofilter(test_df)
        return self.assertTrue(isinstance(gdf, gpd.geodataframe.GeoDataFrame))


class testFailGeopandas(TestCase):

    def test_geopandas_import_fail(self):
        """Test ability to import geopandas"""
        import sys
        sys.modules['geopandas'] = None
        exp = "geopandas is not installed. gdeltPyR needs geopandas to export as shapefile. Visit http://geopandas.org/install.html for instructions."
        with self.assertRaises(Exception) as context:
            gdf = _geofilter(test_df)
        the_exception = context.exception

        return self.assertTrue(exp, str(the_exception))
