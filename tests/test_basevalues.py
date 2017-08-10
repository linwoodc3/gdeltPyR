#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##############################
# Standard Library Import
##############################

import os
from unittest import TestCase

##############################
# Third Party Libraries
##############################

import pandas as pd
import numpy as np
import coveralls

##############################
# Custom Library Import
##############################
#
import gdelt
from gdelt.base import codes,BASE_DIR

class TestBaseValues(TestCase):
    def test_codedataframe(self):
        """Test install data"""

        f = os.path.join(BASE_DIR, 'data', 'cameoCodes.json')
        resp = pd.read_json(f,dtype={'cameoCode': 'str', "GoldsteinScale": np.float64})
        resp.set_index('cameoCode', drop=False, inplace=True)
        print("This is {}".format(gdelt.__file__))
        return (self.assertTrue(resp.equals(codes)))
#
