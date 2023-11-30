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

import os
from unittest import TestCase

import pandas as pd

import gdelt


##############################
# Third party imports
##############################

import geopandas as gpd


##############################
# Local imports
##############################


class TestGdeltBaseSearch(TestCase):
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

    @mock.patch.object(gdelt.gdelt, 'Search')
    def test_search_events_fail_nodata(self, response):
        """Raise exception with empty dataframe."""

        gd = gdelt.gdelt(version=2)
        gd.Search('2017 27 Jul').return_value = pd.DataFrame()
        gd.Search('2017 27 Jul').side_effect = ValueError("This GDELT query "
                                                          "returned no "
                                                          "data. Check query "
                                                          "parameters "
                                                          "and retry")

        exp = "This GDELT query returned no data. Check query parameters and" \
              " retry"


        with self.assertRaises(Exception) as context:
            gd.Search('2017 Jul 27')()

        the_exception = context.exception

        return self.assertEqual(exp, str(the_exception), "Raise exception for"
                                                         " zero data return.")

    # @mock.patch.object(gdelt.gdelt, 'Search')
    # def test_search_table_fail_name(self, response):
    #     """Fail on using an invalid table name"""
    #
    #     table = 'even'
    #     valid = ['events', 'gkg', 'vgkg', 'iatv', 'mentions']
    #
    #     if table not in valid:
    #         gd = gdelt.gdelt(version=2)
    #         gd.Search('2017 27 Jul', table='even'). \
    #             side_effect = ValueError('"You entered "event"; this is not '
    #                                      'a valid table name. Choose from '
    #                                      '"events", "mentions", or "gkg".')
    #
    #     exp = ('"You entered "event"; this is not a valid table name. '
    #            'Choose from "events", "mentions", or "gkg".')
    #     with self.assertRaises(Exception) as context:
    #         gd.Search('2017 Jul 27', table='event')()
    #     the_exception = context.exception
    #     return self.assertEqual(exp, str(the_exception),
    #                             "Exception for wrong table name.")

    def test_basedir(self):
        """Fail on using an invalid table name"""

        exp = (gdelt.base.BASE_DIR)
        this_dir, this_filename = os.path.split(__file__)
        BASE_DIR = os.path.dirname(this_dir)
        BASE = "/".join(this_dir.split('/')[:-1])
        return self.assertIsInstance(BASE_DIR,str)

    def test_Search_load(self):
        """Just load the class"""

        gd = gdelt.gdelt()
        return self.assertIsInstance(gd,gdelt.gdelt)

    # patching in order; bottom to top is first to last
    @mock.patch.object(gdelt.base,'_mp_worker')
    @mock.patch.object(gdelt.base,'_events2Heads')
    def test_my_method_mock_events2_pass(self, mock_B,mock_A):

        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "events2samp.gz"),
                compression="gzip")))

        gd = gdelt.gdelt(version=2)

        res = gd.Search('2017 Jul 1', table='events')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

        # patching in order; bottom to top is first to last
    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_events2Heads')
    def test_my_method_mock_events2_fail_table_name(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "events2samp.gz"),
                compression="gzip")))

        gd = gdelt.gdelt(version=2)
        with self.assertRaises(Exception) as context:
            res = gd.Search('2017 Jul 1', table='evens')

        the_exception = context.exception
        exp = (
        """You entered "evens"; this is not a valid table name. Choose from "events", "mentions", or "gkg".""")


        # returning the objects
        return self.assertEqual(exp,str(context.exception))


    # patching in order; bottom to top is first to last
    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_gkgHeads')
    def test_my_method_mock_gkgv2_pass(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'gkg2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data" ,"gkg2samp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd=gdelt.gdelt(version=2)

        res = gd.Search('2017 Jul 1',table='gkg')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

        # patching in order; bottom to top is first to last
    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_mentionsHeads')
    def test_my_method_mock_events1_pass(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events1.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "events1samp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=1)

        res = gd.Search('2017 Jul 1', table='events')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_mentionsHeads')
    def test_my_method_mock_events1_fail_mentions(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events1.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "events1samp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=1)

        with self.assertRaises(Exception) as context:
            res = gd.Search('2017 Jul 1', table='mentions')

        the_exception = context.exception
        exp = ('GDELT 1.0 does not have the "mentions"'
                                    ' table. Specify the "events" or "gkg"'
                                    'table.')


        # returning the objects
        return self.assertEqual(exp,str(context.exception))

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_mentionsHeads')
    def test_my_method_mock_events1_fail_translation(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events1.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "events1samp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=1)

        with self.assertRaises(Exception) as context:
            res = gd.Search('2017 Jul 1', translation=True)

        the_exception = context.exception
        exp = ('GDELT 1.0 does not have an option to'
                                    ' return translated table data. Switch to '
                                    'version 2 by reinstantiating the gdelt '
                                    'object with <gd = gdelt.gdelt(version=2)>')

        # returning the objects
        return self.assertEqual(exp, str(context.exception))

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_events1Heads')
    def test_my_method_mock_mentions_pass(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'mentions.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "mentionssamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search('2017 Jul 1', table='mentions')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    def test_my_method_mock_gkgv1_pass(self, mock_B):
        # instantiating the first mock; need the headers
        # mock_B = mock.MagicMock(return_value=pd.read_csv(
        #     (os.path.join(gdelt.base.BASE_DIR, 'data', 'mentions.csv')))[
        #     'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "gkg1samp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=1)

        res = gd.Search('2017 Jul 1', table='gkg')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_events1Heads')
    def test_my_method_mock_eventsv2_trans_pass(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data", "events2Transsamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search('2017 Jul 1', table='events',translation=True)

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_mentionsHeads')
    def test_my_method_mock_mentions_trans_pass(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'mentions.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "mentionsTranssamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search('2017 Jul 1', table='mentions', translation=True)

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_gkgHeads')
    def test_my_method_mock_gkg2_trans_pass(self, mock_B, mock_A):
        # instantiating the first mock; need the headers
        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'gkg2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock
        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "gkg2Transsamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search('2017 Jul 1', table='gkg', translation=True)

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_events2Heads')
    @mock.patch.object(gdelt.base,'Pool')
    @mock.patch.object(gdelt.base.pd, 'concat')
    def test_my_method_mock_events2_list_pass(self, mock_D,mock_C,mock_B, mock_A):
        # instantiating the first mock; need the headers

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock

        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search(date=['2017 May 1','2017 Jun 1','2017 Jul 1'])

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_mentionsHeads')
    @mock.patch.object(gdelt.base, 'Pool')
    @mock.patch.object(gdelt.base.pd, 'concat')
    @mock.patch.object(gdelt.base.concurrent.futures, 'ProcessPoolExecutor')
    def test_my_method_mock_mentions_list_pass(self, mock_E, mock_D, mock_C, mock_B,
                                              mock_A):
        # instantiating the first mock; need the headers

        mock_E = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "mentionslistsamp.gz"),
                compression="gzip")))

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "mentionslistsamp.gz"),
                compression="gzip")))

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "mentionslistsamp.gz"),
                compression="gzip")))

        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'mentions.csv')))[
            'name'].values.tolist())

        # instantiating the second mock

        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "mentionslistsamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search(date=['2017 May 1', '2017 Jun 1', '2017 Jul 1'],table='mentions')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_gkgHeads')
    @mock.patch.object(gdelt.base, 'Pool')
    @mock.patch.object(gdelt.base.pd, 'concat')
    @mock.patch.object(gdelt.base.concurrent.futures, 'ProcessPoolExecutor')
    def test_my_method_mock_gkg2_list_pass(self, mock_E, mock_D, mock_C,
                                               mock_B,
                                               mock_A):
        # instantiating the first mock; need the headers

        mock_E = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "gkg2listsamp.gz"),
                compression="gzip")))

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "gkg2listsamp.gz"),
                compression="gzip")))

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "gkg2listsamp.gz"),
                compression="gzip")))

        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'gkg2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock

        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "gkg2listsamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search(date=['2017 May 1', '2017 Jun 1', '2017 Jul 1'],
                        table='gkg')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)


    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_events2Heads')
    @mock.patch.object(gdelt.base,'Pool')
    @mock.patch.object(gdelt.base.pd, 'concat')
    def test_my_method_mock_events2_list_df(self, mock_D,mock_C,mock_B, mock_A):
        # instantiating the first mock; need the headers

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock

        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search(date=['2017 May 1','2017 Jun 1','2017 Jul 1'],
                        output='df')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_events2Heads')
    @mock.patch.object(gdelt.base,'Pool')
    @mock.patch.object(gdelt.base.pd, 'concat')
    def test_my_method_mock_events2_list_json(self, mock_D,mock_C,mock_B, mock_A):
        # instantiating the first mock; need the headers

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock

        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search(date=['2017 May 1','2017 Jun 1','2017 Jul 1'],
                        output='json')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_events2Heads')
    @mock.patch.object(gdelt.base, 'Pool')
    @mock.patch.object(gdelt.base.pd, 'concat')
    def test_my_method_mock_events2_list_csv(self, mock_D, mock_C, mock_B,
                                            mock_A):
        # instantiating the first mock; need the headers

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        mock_C = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock

        mock_A = mock.MagicMock(return_value=(
            pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search(date=['2017 May 1', '2017 Jun 1', '2017 Jul 1'],
                        output='csv')

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

    @mock.patch.object(gdelt.base, '_mp_worker')
    @mock.patch.object(gdelt.base, '_events2Heads')
    @mock.patch.object(gdelt.base, 'Pool')
    @mock.patch.object(gdelt.base.pd, 'concat')
    @mock.patch.object(gdelt.base,'_geofilter')
    def test_my_method_mock_gpd_normcols(self, mock_E,mock_D, mock_C, mock_B,
                                             mock_A):
        # instantiating the first mock; need the headers
        d = pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2listsamp.gz"),
                compression="gzip")
        mock_E = mock.MagicMock(return_value=(
            d))

        mock_C = mock.MagicMock(return_value=(
            d))

        mock_B = mock.MagicMock(return_value=pd.read_csv(
            (os.path.join(gdelt.base.BASE_DIR, 'data', 'events2.csv')))[
            'name'].values.tolist())

        # instantiating the second mock

        mock_A = mock.MagicMock(return_value=(
            d))

        # print(mock_A.return_value.columns)
        gd = gdelt.gdelt(version=2)

        res = gd.Search(date=['2017 May 1', '2017 Jun 1', '2017 Jul 1'],
                        output='gpd',normcols=True)

        # returning the objects
        return self.assertGreater(mock_A.return_value.shape[0], 0)

