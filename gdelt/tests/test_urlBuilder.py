#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com


from unittest import TestCase

from gdelt.dateFuncs import gdeltRangeString, dateRanger
from gdelt.vectorizingFuncs import urlBuilder


class TestUrlBuilder(TestCase):
    def test_urlbuilder_v1(self):
        date_sequence = '2016 10 01'
        ranger_output = dateRanger(date_sequence)
        gdeltstring_output = gdeltRangeString(ranger_output, version=1)
        urlbuilder_test = urlBuilder(gdeltstring_output, version=1)
        exp = 'http://data.gdeltproject.org/events/20161001.export.CSV.zip'
        return self.assertEquals(exp, urlbuilder_test, "Version 1 Url works.")
