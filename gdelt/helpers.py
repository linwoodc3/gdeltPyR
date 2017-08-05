#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##############################
# Standard Library Imports
##############################
import re


##############################
# Standard Library Imports
##############################
# from gdelt.multipdf import parallelize_dataframe

##############################
# Filter functions for dataframes
##############################

def cameos(x, codes):
    try:
        return codes['Description'][x]
    except:
        return "No Description returned for CAMEO code {0}".format(x)


def shaper(row):
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
    geometry = Point(row['ActionGeo_Long'], row['ActionGeo_Lat'])
    return geometry


def rooturl(row):
    """Finds the root url of a news article"""
    s = row['SOURCEURL']
    r = re.compile('(?<=http://)([A-Za-z0-9\.]+)(?=/)')
    r2 = re.compile('(?<=https://)([A-Za-z0-9\.-]+)(?=/)')

    if r.search(s):
        return r.search(s).group()
    elif r2.search(s):
        return r2.search(s).group()
