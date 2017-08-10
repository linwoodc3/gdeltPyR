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
from io import BytesIO, StringIO
import pickle

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

import gdelt
from gdelt.getHeaders import _events2Heads, _events1Heads, _gkgHeads, \
    _mentionsHeads


class testGdeltGetHeaders(TestCase):
    @mock.patch.object(gdelt.getHeaders.requests, 'get')
    def test_events2_headers(self, mock_B):
        """Return csv."""

        with open(os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv'),
                  'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            spam = (csvfile.read())
            response = mock_B()
            response.content = spam
            res = _events2Heads()
        exp = pd.read_csv(BytesIO(response.content))

        return self.assertIsInstance(exp, pd.DataFrame, "Returned dataframe")

    @mock.patch.object(gdelt.getHeaders.requests, 'get')
    def test_events1_headers(self, mock_B):
        """Return csv."""

        spam = pandas.read_csv(
            os.path.join(gdelt.base.BASE_DIR, 'data', 'events1.csv'))[['name']]
        spam.columns = ['tableId']
        df_bytes = spam.to_string(index=False).encode('utf-8')

        response = mock_B()
        response.content = df_bytes

        res = _events1Heads()
        exp = pd.read_csv(BytesIO(response.content))

        return self.assertIsInstance(exp, pandas.DataFrame,
                                     "Returned dataframe")

    @mock.patch.object(gdelt.getHeaders.requests, 'get')
    def test_mentions_headers(self, mock_B):
        """Return csv."""

        spam = pandas.read_csv(
            os.path.join(gdelt.base.BASE_DIR, 'data', 'mentions.csv'))
        spam.columns = ['tableId', 'dataType',
                        'Description']
        buffer = StringIO()
        spam.to_csv(buffer, '\t')
        # df_bytes = spam.to_string(index=False).encode('utf-8')
        data = buffer.getvalue().encode('utf-8')
        response = mock_B()
        response.content = data

        res = _mentionsHeads()
        # exp = pd.read_csv(response.content)

        return self.assertIsInstance(spam, pandas.DataFrame,
                                     "Returned dataframe")

    @mock.patch.object(gdelt.getHeaders.requests, 'get')
    def test_gkg_headers(self, mock_B):
        """Return csv."""

        spam = pandas.read_csv(
            os.path.join(gdelt.base.BASE_DIR, 'data', 'gkg2.csv'))
        spam.columns = ['tableId', 'dataType',
                        'Description']
        buffer = StringIO()
        spam.to_csv(buffer, '\t')
        # df_bytes = spam.to_string(index=False).encode('utf-8')
        data = buffer.getvalue().encode('utf-8')
        response = mock_B()
        response.content = data

        res = _gkgHeads()
        # exp = pd.read_csv(response.content)

        return self.assertIsInstance(spam, pandas.DataFrame,
                                     "Returned dataframe")
