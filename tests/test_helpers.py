# #!/usr/bin/python
# # -*- coding: utf-8 -*-
#
# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##############################
# Standard Library Import
##############################

import datetime
import os
import platform
from unittest import TestCase

import numpy as np
import pandas as pd

import gdelt
from gdelt.helpers import _rooturl, _shaper, _cameos, _testdate, _tableinfo

##############################
# Third Party Libraries
##############################
##############################
# Custom Library Import
##############################

##############################
# Directories
##############################

this_dir, this_filename = os.path.split(__file__)
BASE_DIR = os.path.dirname(this_dir)


class testHelpers(TestCase):
    """Test helper functions"""
    def test_date(self):

        res = _testdate('1980')
        return self.assertIsInstance(res,datetime.datetime)


    def test_urlgetter(self):
        """Pull the root url from a news story url"""
        dd = pd.read_pickle(os.path.join(
            gdelt.base.BASE_DIR, "data", "events2samp.gz"),
            compression="gzip").drop('CAMEOCodeDescription', axis=1)
        test = dd.drop_duplicates('SOURCEURL')[:9]

        exp = np.array(
            ['www.cvilletomorrow.org', 'www.thetowntalk.com',
             'www.comicsbeat.com', 'www.nbcnews.com', 'www.thearabweekly.com',
             'www.thestar.com.my', 'www.thetimes.co.uk',
             'timesofindia.indiatimes.com', 'www.woad.com'], dtype=object)

        resp = test.apply(_rooturl, axis=1).values
        return np.testing.assert_array_equal(exp, resp)

    def test_shaper(self):
        """Make the points"""
        if platform.python_version_tuple()[1] == '4':
            return self.assertIsNone(None)
        dd = pd.read_pickle(os.path.join(
            gdelt.base.BASE_DIR, "data", "events2samp.gz"),
            compression="gzip").drop('CAMEOCodeDescription', axis=1)

        try:
            # Applying the function
            fin = dd.apply(_shaper, axis=1)

            return self.assertIsInstance(fin, pd.Series)
        except:
            exp= ('You need to install shapely to use this feature.')
            with self.assertRaises(Exception) as context:
                fin = dd.apply(_shaper, axis=1)
            the_exception = context.exception


            return self.assertIsInstance(str(the_exception),str, "Not installed")


    def test_cameo(self):
        """Make the cameo code description"""
        codes = pd.read_json(os.path.join(
            gdelt.base.BASE_DIR, "data", "cameoCodes.json"))

        dd = pd.read_pickle(os.path.join(
            gdelt.base.BASE_DIR, "data", "events2samp.gz"),
            compression="gzip").drop('CAMEOCodeDescription', axis=1)
        da = dd.apply(lambda x: _cameos(dd,codes))
        return self.assertIsInstance(da,pd.Series)

    def testtable_events2(self):
        """Make the cameo code description"""
        tabs = pd.read_csv(
            os.path.join(BASE_DIR, 'data', 'events2.csv'))
        return self.assertTrue(tabs.equals(_tableinfo('events',version=2)))

    def testtable_gkg2(self):
        """Make the cameo code description"""
        tabs = pd.read_csv(
            os.path.join(BASE_DIR, 'data', 'gkg2.csv'))
        return self.assertTrue(tabs.equals(_tableinfo('gkg',version=2)))

    def testtable_events1(self):
        """Make the cameo code description"""
        tabs = pd.read_csv(
            os.path.join(BASE_DIR, 'data', 'events1.csv'))
        return self.assertTrue(tabs.equals(_tableinfo('events',version=1)))

    def testtable_mentspass(self):
        """Make the cameo code description"""
        tabs = pd.read_csv(
            os.path.join(BASE_DIR, 'data', 'mentions.csv'))
        return self.assertTrue(tabs.equals(_tableinfo('ments',version=2)))

    def testtable_mentsfail(self):
        """Make the cameo code description"""
        exp = 'GDELT 1.0 does not have a mentions table.'
        with self.assertRaises(Exception) as context:
            checked = _tableinfo('ments',version=1)
        the_exception = context.exception

        return self.assertEqual(exp, str(the_exception))

    def testtable_cloudviz(self):
        """Make the cameo code description"""
        tabs = pd.read_csv(
            os.path.join(BASE_DIR, 'data', 'visualgkg.csv'))
        return self.assertTrue(tabs.equals(_tableinfo('vision',version=2)))

    def testtable_iatv(self):
        """Make the cameo code description"""
        tabs = pd.read_csv(
            os.path.join(BASE_DIR, 'data', 'iatv.csv'))
        return self.assertTrue(tabs.equals(_tableinfo('iatv',version=2)))


    def testtable_cameo(self):
        """Make the cameo code description"""
        tabs = pd.read_json(
            os.path.join(BASE_DIR, 'data', 'cameoCodes.json'),
            dtype={'cameoCode': 'str', "GoldsteinScale": np.float64})

        return self.assertEqual(_tableinfo('cameo').shape,tabs.shape)


    def testtable_fail(self):
        """Make the cameo code description"""
        table = 'bobby'
        valid = ['cameo', 'events', 'gkg', 'vgkg', 'iatv',
                 'graph', 'ments', 'mentions', 'cloudviz',
                 'cloud vision', 'vision']
        exp = ('You entered "{}"; this is not a valid table name.'
                         ' Choose from {}.'.format(
            table,", ".join(valid)))
        with self.assertRaises(Exception) as context:
            checked = _tableinfo('bobby',version=1)
        the_exception = context.exception

        return self.assertEqual(exp, str(the_exception))




