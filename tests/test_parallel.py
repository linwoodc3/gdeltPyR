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

import os
import sys
import warnings
from io import BytesIO, StringIO
from unittest import TestCase
from zipfile import ZipFile

import numpy as np
import pandas as pd

import gdelt
from gdelt.parallel import _mp_worker


##############################
# Third Party Libraries
##############################
##############################
# Custom Library Import
##############################


class testParallelWorker(TestCase):



    @mock.patch.object(gdelt.parallel.requests, 'get')
    def test_parallel_events2_pass(self, mock_B):
        """Return csv."""

        # set up return value for mock
        ver = sys.version_info.major
        spam = pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "events2samp.gz"),
                compression="gzip").drop('CAMEOCodeDescription',axis=1)
        spam.columns = np.arange(len(spam.columns))
        spam[[26,27,28]] = spam[[26,27,28]].astype('str')

        if ver == 3:
            buffer = StringIO()
            spam.to_csv(buffer, sep='\t', header=False,index=False)
        else:
            buffer = BytesIO()
            spam.to_csv(buffer, sep='\t', header=False, index=False)
        # print(spam)

        # making the zipfile
        inMemoryOutputFile = BytesIO()
        zipFile = ZipFile(inMemoryOutputFile, 'w')
        zipFile.writestr('OEBPS/20170701234500.export.CSV.zip',
                         buffer.getvalue())
        zipFile.close()

        # make the mock object
        response = mock_B()
        response.status_code=200
        response.content = inMemoryOutputFile.getvalue()
        response.return_value = inMemoryOutputFile

        # run the function of gdelt
        url = 'http://data.gdeltproject.org/gdeltv2/20170701234500.export.CSV.zip'
        res = _mp_worker(url,table='events')

        # the test
        return self.assertTrue(res[[0,1,2,3]].equals(spam[[0,1,2,3]]), "Returned dataframe")

    @mock.patch.object(gdelt.parallel.requests, 'get')
    def test_parallel_404_warnings(self, mock_B):
        """Return csv."""

        # make the mock object
        response = mock_B()
        response.status_code=404

        # run the function of gdelt
        url = 'http://data.gdeltproject.org/gdeltv2/20170727234500.export.CSV.zip'
        exp = [("GDELT does not have a url for date time 20170727234500"),
               ("GDELT did not return data for date time 20170727234500")]

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            res = _mp_worker(url, table='events')
            # Verify some things
            # print(str(w[0].message),str(w[1].message))
            # assert len(w) == 1
            # assert issubclass(w[-1].category, UserWarning)
            # assert "deprecated" in str(w[-1].message)

        # the test
        return self.assertEqual([str(w[0].message),str(w[1].message)],exp, "Returned dataframe")

    @mock.patch.object(gdelt.parallel.requests, 'get')
    def test_parallel_gkgv2_pass(self, mock_B):
        """Return csv."""

        # set up return value for mock
        spam = pd.read_pickle(os.path.join(
            gdelt.base.BASE_DIR, "data", "gkg2samp.gz"),
            compression="gzip")
        spam.columns = np.arange(len(spam.columns))
        ver = sys.version_info.major
        if ver == 3:
            buffer = StringIO()
            spam.to_csv(buffer, sep='\t', header=False,index=False)
        else:
            buffer = BytesIO()
            spam.to_csv(buffer, sep='\t', header=False, index=False,encoding='utf-8')

        # print(spam)

        # making the zipfile
        inMemoryOutputFile = BytesIO()
        zipFile = ZipFile(inMemoryOutputFile, 'w')
        zipFile.writestr('OEBPS/20170701234500.gkg.csv.zip',
                         buffer.getvalue())
        zipFile.close()

        # make the mock object
        response = mock_B()
        response.status_code = 200
        response.content = inMemoryOutputFile.getvalue()
        response.return_value = inMemoryOutputFile

        # run the function of gdelt
        url = 'http://data.gdeltproject.org/gdeltv2/20170701234500.gkg.csv.zip'
        res = _mp_worker(url, table='gkg')

        # the test
        return self.assertTrue(res[[0, 1, 2, 3]].equals(spam[[0, 1, 2, 3]]),
                               "Returned dataframe")

    @mock.patch.object(gdelt.parallel.requests, 'get')
    def test_parallel_mentions_pass(self, mock_B):
        """Return csv."""

        # set up return value for mock
        spam = pd.read_pickle(os.path.join(
            gdelt.base.BASE_DIR, "data", "mentionssamp.gz"),
            compression="gzip")
        spam.columns = np.arange(len(spam.columns))
        ver = sys.version_info.major
        if ver == 3:
            buffer = StringIO()
            spam.to_csv(buffer, sep='\t', header=False, index=False)
        else:
            buffer = BytesIO()
            spam.to_csv(buffer, sep='\t', header=False, index=False,
                        encoding='utf-8')
        # print(spam)

        # making the zipfile
        inMemoryOutputFile = BytesIO()
        zipFile = ZipFile(inMemoryOutputFile, 'w')
        zipFile.writestr('OEBPS/20170701234500.mentions.CSV.zip',
                         buffer.getvalue())
        zipFile.close()

        # make the mock object
        response = mock_B()
        response.status_code = 200
        response.content = inMemoryOutputFile.getvalue()
        response.return_value = inMemoryOutputFile

        # run the function of gdelt
        url = ('http://data.gdeltproject.org/gdeltv2/'
               '20170701234500.mentions.CSV.zip')
        res = _mp_worker(url, table='gkg')

        # the test
        return self.assertTrue(res[[0, 1, 2, 3]].equals(spam[[0, 1, 2, 3]]),
                               "Returned dataframe")