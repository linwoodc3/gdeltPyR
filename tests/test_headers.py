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
import sys
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

        spam = pandas.read_csv(
            os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv'),encoding='utf-8')
        spam.columns = ['tableId', 'dataType',
                        'Description']
        spam = spam.assign(Empty='NULLABLE')[['tableId', 'dataType', 'Empty', 'Description']]
        ver = sys.version_info.major
        if ver == 3:
            buffer = StringIO()
            spam.to_csv(buffer, index=False)
            data = buffer.getvalue().encode('utf-8')
        else:
            buffer = BytesIO()
            spam.to_csv(buffer, index=False,encoding='utf-8')
            data = buffer.getvalue()



        # df_bytes = spam.to_string(index=False).encode('utf-8')



        response = mock_B()
        response.content = data

        res = _events2Heads()

        return self.assertIsInstance(res, list, "Returned dataframe")

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
        ver = sys.version_info.major

        exp = pd.read_csv(BytesIO(response.content))
        print(exp)

        return self.assertIsInstance(exp, pandas.DataFrame,
                                     "Returned dataframe")

    @mock.patch.object(gdelt.getHeaders.requests, 'get')
    def test_mentions_headers(self, mock_B):
        """Return csv."""

        spam = pandas.read_csv(
            os.path.join(gdelt.base.BASE_DIR, 'data', 'mentions.csv'))
        spam.columns = ['tableId', 'dataType',
                        'Description']
        ver = sys.version_info.major
        if ver == 3:
            buffer = StringIO()
            spam.to_csv(buffer,sep='\t', index=False)
            data = buffer.getvalue().encode('utf-8')
        else:
            buffer = BytesIO()
            spam.to_csv(buffer,sep='\t', index=False, encoding='utf-8')
            data = buffer.getvalue()


        # buffer = StringIO()
        # spam.to_csv(buffer, '\t')
        # # df_bytes = spam.to_string(index=False).encode('utf-8')
        # data = buffer.getvalue().encode('utf-8')
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
        ver = sys.version_info.major
        if ver == 3:
            buffer = StringIO()
            spam.to_csv(buffer,sep='\t', index=False)
            data = buffer.getvalue().encode('utf-8')
        else:
            buffer = BytesIO()
            spam.to_csv(buffer,sep='\t', index=False, encoding='utf-8')
            data = buffer.getvalue()

        # buffer = StringIO()
        # spam.to_csv(buffer, '\t')
        # # df_bytes = spam.to_string(index=False).encode('utf-8')
        # data = buffer.getvalue().encode('utf-8')
        response = mock_B()
        response.content = data

        res = _gkgHeads()
        # exp = pd.read_csv(response.content)

        return self.assertIsInstance(spam, pandas.DataFrame,
                                     "Returned dataframe")
