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

import datetime
from unittest import TestCase

##############################
# Third party imports
##############################

import coveralls

##############################
# Local imports
##############################

import gdelt


class TestGdeltDateInputs(TestCase):
    @mock.patch('gdelt.gdelt.Search')
    def test_search_events_fail_nodata(self, mock_get):
        """Send a request to the API server and store the response."""

        # gd1 = gdelt.gdelt(version=2)
        #
        # # loading the mock dataframe return
        # mockin = mock.Mock(side_effect=ValueError("This GDELT query returned no data. Check internet connection or query parameters and retry"))
        # # Creating the mock object
        #
        #
        # # Adding attributes for the mock; setting it to the pickled dataframe
        # mock_get.return_value.dataframe = exp
        #
        # # real response for testing
        # response = gd1.Search('2017 July', table='events', coverage=False)
        #
        # # Use dataframe method to test for equality
        # return (self.assertTrue(response.dataframe.equals(events1)))

    def test_search_events_fail_nodata(self):
        """Raise exception with empty dataframe."""

        gd = gdelt.gdelt(version=2)
        exp = "This GDELT query returned no data. Check query parameters and retry"
        with self.assertRaises(Exception) as context:
            checked = gd.Search('2017 Jul 27',table='events')
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception), "Raise exception for zero data return.")

    def test_search_table_fail_name(self):
        """Fail on using an invalid table name"""

        gd = gdelt.gdelt(version=2)
        exp = """You entered "event"; this is not a valid table name. Choose from "events", "mentions", or "gkg"."""
        with self.assertRaises(Exception) as context:
            checked = gd.Search('2017 Jul 27',table='event')
        the_exception = context.exception
        return self.assertEqual(exp, str(the_exception), "Exception for wrong table name.")
