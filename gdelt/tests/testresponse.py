#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##################################
# Standard library imports
##################################
from unittest import TestCase

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

from gdelt.vectorizingFuncs import urlBuilder
from gdelt.dateFuncs import gdeltRangeString, dateRanger

# import .constants

BASEURL = 'http://data.gdeltproject.org/'

##################################
# Unit Tests
##################################

gdelt1 = urljoin(BASEURL, 'events/index.html')
gdelt2 = urljoin(BASEURL, 'gdeltv2/masterfilelist.txt')


class testresponse(TestCase):
    def test_request_response_version2(self):
        # Send a request to the API server and store the response.
        response = requests.get(gdelt2)
        # if response.ok:
        #     print(response,gdelt2)
        #     return response
        # else:
        #     return None
        answer = response.ok
        exp = True
        # Confirm that the request-response cycle completed successfully.
        return self.assertEquals(exp, answer, "GDELT 2.0 is working")

    def test_request_response_version1(self):
        # Send a request to the API server and store the response.
        response = requests.get(gdelt1)
        # if response.ok:
        #     print(response,gdelt1)
        #     return response
        # else:
        #     return None
        answer = response.ok
        exp = True

        # Confirm that the request-response cycle completed successfully.
        date_sequence = '2016 10 01'
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = urlBuilder(gdeltstring_output, version=1)
        exp2 = 'http://data.gdeltproject.org/events/20161001.export.CSV.zip'
        print(exp2 == urlbuilder_test)
        return self.assertEquals(exp, answer, "GDELT 1.0 is working")
