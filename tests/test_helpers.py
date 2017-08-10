# #!/usr/bin/python
# # -*- coding: utf-8 -*-
#
# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##############################
# Standard Library Import
##############################

import os
import datetime
import pickle
from unittest import TestCase

##############################
# Third Party Libraries
##############################


import numpy as np
import pandas as pd
import coveralls

##############################
# Custom Library Import
##############################

import gdelt
from gdelt.helpers import _rooturl,_shaper,_cameos
#
class testHelpers(TestCase):
#     def test_testdate(self):
#         """Testing whether a test string works"""
#         datestring = '2016 July 10'
#         exp = datetime.datetime(2016, 7, 10, 0, 0)
#         resp = gdelt.helpers.testdate('2016 July 10')
#         return (self.assertEqual(exp,resp,"The test date function works"))
#
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