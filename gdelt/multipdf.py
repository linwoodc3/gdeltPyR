#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##################################
# Standard library imports
##################################
import argparse
from multiprocessing import cpu_count

##################################
# Third party imports
##################################
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

##################################
# Local imports
##################################
from gdelt.helpers import _shaper

cores = cpu_count()
e = ProcessPoolExecutor(max_workers=cores)


# def _shaper(row):
#     """
#     Parallel function to create shapely points
#     from latitude/longitude pair in dataframe
#
#     Parameters
#     ----------
#     row : pandas or dask dataframe row
#         Row containing latitude and longitude variables and data
#
#     Returns
#     -------
#     shapely point
#         Shapely spatial object for geoprocessing in Python.
#     """
#     try:
#         from shapely.geometry import Point
#     except:
#         raise ImportError('You need to install shapely to use this feature.')
#
#     try:
#         import fiona
#     except:
#         raise ImportError('You need to install fiona to use this feature.')
#     try:
#         import geopandas
#     except:
#         raise ImportError('You need to install geopandas to use this feature.')
#     geometry = Point(row['ActionGeo_Long'], row['ActionGeo_Lat'])
#     return geometry


def _call_apply_fn(df):
    return df.apply(_shaper, axis=1)


def _parallelize_dataframe(df):
    """Applying function"""
    df_split = np.array_split(df, cores * 2)
    finaldf = pd.concat(list(e.map(_call_apply_fn, df_split)))
    return finaldf


#
# if __name__ == '__main__':
#     import sys
#     parallelize_dataframe(sys.argv[1:])
if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser(description='Parallelize pandas apply function')
    parser.add_argument('--df', metavar='pandas.core.frame.DataFrame', required=True,
                        help='The target dataframe to apply the function.')
    parser.add_argument('--func', metavar='function', required=False,
                        help='The function to be applied to the dataframe.')
    args = parser.parse_args()
    # model_schema(df=args.df, func=args.func)
