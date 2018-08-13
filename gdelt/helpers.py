#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

import datetime
import os
##############################
# Standard Library Imports
##############################
import re

import numpy as np
import pandas as pd
##############################
# Third party Library Imports
##############################
from dateutil.parser import parse

##############################
# Filter functions for dataframes
##############################

this_dir, this_filename = os.path.split(__file__)
BASE_DIR = os.path.dirname(this_dir)

def _cameos(x, codes):
    try:
        return codes['Description'][x]
    except:
        return "No Description returned for CAMEO code {0}".format(x)


def _shaper(row):
    """
    Parallel function to create shapely points
    from latitude/longitude pair in dataframe

    Parameters
    ----------
    row : pandas or dask dataframe row
        Row containing latitude and longitude variables and data

    Returns
    -------
    shapely point
        Shapely spatial object for geoprocessing in Python.
    """
    try:
        from shapely.geometry import Point
    except:
        raise ImportError('You need to install shapely to use this feature.')

    try:
        import fiona
    except:
        raise ImportError('You need to install fiona to use this feature.')
    try:
        import geopandas
    except:
        raise ImportError('You need to install geopandas to use this feature.')
    try:
        geometry = Point(row['ActionGeo_Long'], row['ActionGeo_Lat'])
    except:
        geometry = Point(row['actiongeolong'], row['actiongeolat'])
    return geometry


def _rooturl(row):
    """Finds the root url of a news article"""
    s = row['SOURCEURL']
    r = re.compile('(?<=http://)([A-Za-z0-9\.-]+)(?=/)')
    r2 = re.compile('(?<=https://)([A-Za-z0-9\.-]+)(?=/)')

    if r.search(s):
        return r.search(s).group()
    elif r2.search(s):
        return r2.search(s).group()

def _testdate(dateString):
    """Test dates of different formats"""
    if len(dateString) == 4:
        comp = datetime.datetime.strptime(dateString, '%Y')
    elif len(dateString) == 6:
        comp = datetime.datetime.strptime(dateString, '%Y%m')
    else:
        comp = parse(dateString)
    return comp


def _tableinfo(table='cameo',version=2):
    """
    Parameters
    -----------
    :param table: str
        Name of GDELT table

    Returns
    --------

    dataframe
        Pandas dataframe containing schema of table

    Examples
    --------
    Example of retrieving the events table schema.

    >>> print([i for i in example_generator(4)])
    [0, 1, 2, 3]
    """



    table = table.lower()

    valid = ['cameo', 'events', 'gkg', 'vgkg', 'iatv',
             'graph', 'ments', 'mentions', 'cloudviz',
             'cloud vision', 'vision']
    if table not in valid:
        raise ValueError('You entered "{}"; this is not a valid table name.'
                         ' Choose from {}.'.format(
            table,", ".join(valid)))

    if table == 'cameo':
        tabs = pd.read_json(
            os.path.join(BASE_DIR, 'data', 'cameoCodes.json'),
            dtype={'cameoCode': 'str', "GoldsteinScale": np.float64})
        tabs.set_index('cameoCode', drop=False, inplace=True)
    elif table == 'events' and float(version) == 1.0:
        tabs = pd.read_csv(os.path.join(BASE_DIR, 'data', 'events1.csv'))

    elif table == 'events' and float(version) == 2.0:
        tabs = pd.read_csv(os.path.join(BASE_DIR, 'data', 'events2.csv'))

    elif table == 'gkg' or table == 'graph':
        tabs = pd.read_csv(os.path.join(BASE_DIR, 'data', 'gkg2.csv'))
    elif table == 'mentions' or table == 'ments':
        if float(version) != 2.0:
            raise ValueError('GDELT 1.0 does not have a mentions table.')
        else:
            tabs = pd.read_csv(
                os.path.join(BASE_DIR, 'data', 'mentions.csv'))

    elif table == 'cloud vision' or table == 'vgkg' or table == 'cloudviz' \
            or table == 'vision':
        tabs = pd.read_csv(os.path.join(BASE_DIR, 'data', 'visualgkg.csv'))

    elif table == 'iatv' or table == 'tv':
        tabs = pd.read_csv(os.path.join(BASE_DIR, 'data', 'iatv.csv'))

    return tabs