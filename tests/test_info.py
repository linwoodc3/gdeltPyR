# #!/usr/bin/python
# # -*- coding: utf-8 -*-
#
# # Author:
# # Linwood Creekmore
# # Email: valinvescap@gmail.com
#
# ##############################
# # Standard Library Import
# ##############################
#
# import os
# from unittest import TestCase
#
# ##############################
# # Third Party Libraries
# ##############################
#
# import pandas as pd
# import numpy as np
# import coveralls
#
# ##############################
# # Custom Library Import
# ##############################
#
# import gdelt
# from gdelt.base import codes, BASE_DIR
#
#
# class testTableValues(TestCase):
#     def test_codedataframe(self):
#         """Test CAMEO Code dataframe."""
#
#         f = os.path.join(BASE_DIR, 'data', 'cameoCodes.json')
#         resp = pd.read_json(f, dtype={'cameoCode': 'str', "GoldsteinScale": np.float64})
#         resp.set_index('cameoCode', drop=False, inplace=True)
#         print("This is {}".format(gdelt.__file__))
#         return (self.assertTrue(resp.equals(codes)))
#
#     def test_events1_columns(self):
#         """Test events 1 column descriptions"""
#
#         f = os.path.join(BASE_DIR, 'data', 'events1.csv')
#         resp = pd.read_csv(f)
#         tabs = gdelt.tableInfo(version=1)
#         ret = tabs.gettable('events')
#         return (self.assertTrue(resp.equals(ret)))
#
#     def test_events2_columns(self):
#         """Test events version 2 column descriptions"""
#
#         f = os.path.join(BASE_DIR, 'data', 'events2.csv')
#         resp = pd.read_csv(f)
#         tabs = gdelt.tableInfo(version=2)
#         ret = tabs.gettable('events')
#         return (self.assertTrue(resp.equals(ret)))
#
#     def test_mentions_columns_pass(self):
#         """Test mentions version 2 pass column descriptions"""
#
#         f = os.path.join(BASE_DIR, 'data', 'mentions.csv')
#         resp = pd.read_csv(f)
#         tabs = gdelt.tableInfo(version=2)
#         ret = tabs.gettable('mentions')
#         return (self.assertTrue(resp.equals(ret)))
#
#     def test_mentions_columns_fail(self):
#         """Fail mentions version 2 pass column descriptions"""
#
#         f = os.path.join(BASE_DIR, 'data', 'mentions.csv')
#         resp = pd.read_csv(f)
#         tabs = gdelt.tableInfo(version=1)
#         exp = 'GDELT 1.0 does not have a mentions table.'
#         with self.assertRaises(Exception) as context:
#             checked = tabs.gettable('mentions')
#         the_exception = context.exception
#         return self.assertEqual(exp, str(the_exception), "Exception for wrong table name.")
#
#     def test_gkg_columns_pass(self):
#         """Test gkg version 2 pass column descriptions"""
#
#         f = os.path.join(BASE_DIR, 'data', 'gkg2.csv')
#         resp = pd.read_csv(f)
#         tabs = gdelt.tableInfo(version=2)
#         ret = tabs.gettable('gkg')
#         return (self.assertTrue(resp.equals(ret)))
#
#     def test_vgkg_columns_pass(self):
#         """Test visual gkg version 2 pass column descriptions"""
#
#         f = os.path.join(BASE_DIR, 'data', 'visualgkg.csv')
#         resp = pd.read_csv(f)
#         tabs = gdelt.tableInfo(version=2)
#         ret = tabs.gettable('vgkg')
#         return (self.assertTrue(resp.equals(ret)))
#
#     def test_iatv_columns_pass(self):
#         """Test iatv pass column descriptions"""
#
#         f = os.path.join(BASE_DIR, 'data', 'iatv.csv')
#         resp = pd.read_csv(f)
#         tabs = gdelt.tableInfo(version=2)
#         ret = tabs.gettable('iatv')
#         return (self.assertTrue(resp.equals(ret)))
#
#
