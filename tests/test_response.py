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
import os

import pandas as pd

import gdelt
from tests.constants import BASEURL

##################################
# Third party imports
##################################
##################################
# Local imports
##################################


this_dir, this_filename = os.path.split(__file__)
BASE_DIR = os.path.dirname(this_dir)


##################################
# Unit Tests
##################################

gdelt1 = urljoin(BASEURL, 'events/index.html')
gdelt2 = urljoin(BASEURL, 'gdeltv2/masterfilelist.txt')
gd2 = gdelt.gdelt(version=2)
gd1 = gdelt.gdelt(version=1)

class testresponse(TestCase):

    @mock.patch('gdelt.gdelt.Search')
    def test_request_response_version2_events(self,mock_get):
        """Send a request to the API server and store the response."""
        gd2 = gdelt.gdelt(version=2)


        # loading the mock dataframe return
        events2 = pd.read_pickle(os.path.join(
            gdelt.base.BASE_DIR, "data",
            "events2samp.gz"),
            compression="gzip")

        # Creating the mock object
        mock_get.return_value = mock.Mock()

        # Adding attributes for the mock; setting it to the pickled dataframe
        mock_get.return_value.dataframe = events2

        # real response for testing
        response = gd2.Search('2017 Jul 1',table='events',coverage=False)

        # Use dataframe method to test for equality
        return (self.assertTrue(response.dataframe.equals(events2)))

    @mock.patch('gdelt.gdelt.Search')
    def test_request_response_version1_events(self,mock_get):
        """Send a request to the API server and store the response."""

        gd1 = gdelt.gdelt(version=1)

        # loading the mock dataframe return

        events1 = pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events1samp.gz"),
                compression="gzip")


        # Creating the mock object
        mock_get.return_value = mock.Mock()

        # Adding attributes for the mock; setting it to the pickled dataframe
        mock_get.return_value.dataframe = events1

        # real response for testing
        response = gd1.Search('2017 Jul 1', table='events', coverage=False)

        # Use dataframe method to test for equality
        return (self.assertTrue(response.dataframe.equals(events1)))

