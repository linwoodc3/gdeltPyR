#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com



##################################
# Standard library imports
##################################
try:
    from unittest import TestCase, mock
except:
    from unittest import TestCase
    import mock

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import pickle
import os

##################################
# Third party imports
##################################
import requests

##################################
# Local imports
##################################

import gdelt
from gdelt.vectorizingFuncs import geofilter
from tests.constants import BASEURL

# import .constants

# BASEURL = 'http://data.gdeltproject.org/'
this_dir, this_filename = os.path.split(__file__)
BASE_DIR = os.path.dirname(this_dir)
print(BASE_DIR)

##################################
# Unit Tests
##################################

gdelt1 = urljoin(BASEURL, 'events/index.html')
gdelt2 = urljoin(BASEURL, 'gdeltv2/masterfilelist.txt')
gd2 = gdelt.gdelt(version=2)
gd1 = gdelt.gdelt(version=1)


class testresponse(TestCase):
    @mock.patch('gdelt.gdelt.Search')
    def test_request_response_version2_events(self, mock_get):
        """Send a request to the API server and store the response."""
        gd2 = gdelt.gdelt(version=2)

        # loading the mock dataframe return
        f = open(os.path.join(BASE_DIR, 'data', 'gdv2events.pkl'), 'rb')
        events2 = pickle.load(f)
        f.close()

        # Creating the mock object
        mock_get.return_value = mock.Mock()

        # Adding attributes for the mock; setting it to the pickled dataframe
        mock_get.return_value.dataframe = events2

        # real response for testing
        response = gd2.Search('2017 March 12', table='events', coverage=False)

        # Use dataframe method to test for equality
        return (self.assertTrue(response.dataframe.equals(events2)))

    @mock.patch('gdelt.gdelt.Search')
    def test_request_response_version1_events(self, mock_get):
        """Send a request to the API server and store the response."""

        gd1 = gdelt.gdelt(version=1)

        # loading the mock dataframe return
        f = open(os.path.join(BASE_DIR, 'data', 'gdv1events.pkl'),'rb')
        events1 = pickle.load(f)
        f.close()

        # Creating the mock object
        mock_get.return_value = mock.Mock()

        # Adding attributes for the mock; setting it to the pickled dataframe
        mock_get.return_value.dataframe = events1

        # real response for testing
        response = gd1.Search('2017 March 12', table='events', coverage=False)

        # Use dataframe method to test for equality
        return (self.assertTrue(response.dataframe.equals(events1)))
