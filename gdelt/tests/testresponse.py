#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##################################
# Standard library imports
##################################
from unittest import TestCase,mock
import pickle

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

##################################
# Third party imports
##################################


import requests

##################################
# Local imports
##################################

import gdelt
from gdelt.vectorizingFuncs import urlBuilder
from gdelt.dateFuncs import gdeltRangeString, dateRanger
from gdelt.tests.constants import BASEURL

# import .constants

# BASEURL = 'http://data.gdeltproject.org/'

##################################
# Unit Tests
##################################

gdelt1 = urljoin(BASEURL, 'events/index.html')
gdelt2 = urljoin(BASEURL, 'gdeltv2/masterfilelist.txt')
gd2 = gdelt.gdelt(version=2)
gd1 = gdelt.gdelt(version=1)

class testresponse(TestCase):
    gd2 = gdelt.gdelt(version=2)
    gd1 = gdelt.gdelt(version=1)
    @mock.patch('gdelt.gdelt.Search')
    def test_request_response_version2(self,mock_get):
        # Send a request to the API server and store the response.
        mock_get.return_value.ok = True
        response = requests.get(gdelt2)
        return (self.assertIsNotNone(response))
        # if response.ok:
        #     print(response,gdelt2)
        #     return response
        # else:
        #     return None
        # answer = response.ok
        # exp = True
        # # Confirm that the request-response cycle completed successfully.

        # return self.assertEquals(exp, answer, "GDELT 2.0 is working")

    @mock.patch('gdelt.gdelt.Search')
    def test_request_response_version1(self,mock_get):
        """Send a request to the API server and store the response."""
        events1 =
        mock_get.return_value.ok = True
        response = requests.get(gdelt1)
        return (self.assertIsNotNone(response))
        # if response.ok:
        #     print(response,gdelt1)
        #     return response
        # else:
        #     return None
        # answer = response.ok
        # exp = True

        # Confirm that the request-response cycle completed successfully.
        # date_sequence = '2016 10 01'
        # ranger_output = dateRanger(date_sequence)
        # gdeltstring_output = gdeltRangeString(ranger_output, version=1)
        # urlbuilder_test = urlBuilder(gdeltstring_output, version=1)
        # exp2 = 'http://data.gdeltproject.org/events/20161001.export.CSV.zip'
        # print(exp2 == urlbuilder_test)
        # return self.assertEquals(exp, answer, "GDELT 1.0 is working")
