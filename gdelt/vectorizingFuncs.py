#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##################################
# Standard Library imports
##################################
import datetime

############################
# Third Party imports
#############################
import numpy as np
import pandas as pd
from dateutil.parser import parse

################################
# Local Imports
################################
from gdelt.multipdf import _parallelize_dataframe
from gdelt.helpers import _testdate


def _vectorizer(function, dateArray):
    helper = np.vectorize(function)

    final = helper(dateArray.tolist()).tolist()

    if isinstance(final, list):

        final = list(set(final))
    elif isinstance(final, str):
        final = final
    else:
        pass

    return final


# Finds the urls from an array of dates


def _urlFinder(dataframe, targetDate, col):
    return dataframe[col][dataframe[col].str.contains(targetDate)]


def _vectorizedUrlFinder(function, urlList, frame):
    helper = np.vectorize(function)
    return pd.concat(helper(urlList, frame).tolist())


def _downloadVectorizer(function, urlList):
    """Vectorized function to download urls"""
    helper = np.vectorize(function)
    return pd.concat(helper(urlList).tolist()).reset_index(drop=True)

def _urlBuilder(dateString, version, table='events', translation=False):
    """
    Takes date string from gdeltRange string and creates GDELT urls


    Parameters
    ------------

    table types:
                * events and mentions (default)
                * gkg
                * mentions only
                :type version: object
                :param dateString:
                :param version:
                :param table:
    """

    if version == 2:
        base = "http://data.gdeltproject.org/gdeltv2/"

    if version == 1:
        base = "http://data.gdeltproject.org/"

    if table == "events":
        if version == 1:
            base += 'events/'
        if not translation:
            caboose = ".export.CSV.zip"
        else:
            caboose = ".translation.export.CSV.zip"
    elif table == "mentions":
        if not translation:
            caboose = ".mentions.CSV.zip"
        else:
            caboose = ".translation.mentions.CSV.zip"
    elif table == "gkg":
        if version == 1:
            base += 'gkg/'
            if isinstance(dateString,str):
                comp = _testdate(dateString)
                if comp < parse('2013 Apr 1'):
                    raise Exception('GDELT 1.0 Global Knowledge Graph requires dates greater'
                                    ' than or equal to April 1 2013')
            elif isinstance(dateString, list) or isinstance(dateString,
                                                          np.ndarray):
                if not (np.all(list(
                        map(
                            lambda x: x > parse('2013 04 01'), list(
                                map(
                                    _testdate, dateString)))))):
                    raise Exception('GDELT 1.0 Global Knowledge Graph requires dates greater'
                                    ' than or equal to April 1 2013')

            # if len(dateString) == 4:
            #     comp = datetime.datetime.strptime(dateString, '%Y')
            # elif len(dateString) == 6:
            #     comp = datetime.datetime.strptime(dateString, '%Y%m')
            # else:
            #     comp = parse(dateString)
            # if comp < parse('2013 Apr 1'):
            #     raise Exception('GDELT 1.0 Global Knowledge Graph requires dates greater'
            #                     ' than or equal to April 1 2013')


        if not translation:
            caboose = ".gkg.csv.zip"
        else:
            caboose = ".translation.gkg.csv.zip"
    else:
        raise ValueError('You entered an incorrect GDELT table type.'
                         ' Choose between \"events\",\"mentions\",'
                         'and \"gkg\".')

    # if version == 2:
    #     base = "http://data.gdeltproject.org/gdeltv2/"
    #
    # if version == 1:
    #     base = "http://data.gdeltproject.org/"
    #
    # if isinstance(dateString,str):
    #     if len(dateString) == 4:
    #         comp = datetime.datetime.strptime(dateString, '%Y')
    #     elif len(dateString) == 6:
    #         comp = datetime.datetime.strptime(dateString, '%Y%m')
    #     else:
    #         comp = parse(dateString)
    #
    # if table == "events":
    #     if version ==1 and isinstance(dateString,str):
    #         base += 'events/'
    #         try:
    #             if comp<parse('2006 Jan 1'):
    #                 caboose = ".zip"
    #         except:
    #             try:
    #                 if comp < parse('2006 Jan 1'):
    #                     caboose='.zip'
    #             except :
    #                 raise Exception('Invalid date entry')
    #     else:
    #         caboose = ".export.CSV.zip"
    #
    # elif table == "mentions":
    #     caboose = ".mentions.CSV.zip"
    # # elif table == "gkg":
    # #     print(dateString)
    # #     if version == 1:
    # #         if comp< parse('2013 Apr 01'):
    # #             raise Exception('GDELT 1.0 Global Knowledge Graph requires dates greater than or equal to April 1 2013.')
    # #         base += 'gkg/'
    # #     elif version == 2:
    # #         if comp < parse('2015 Feb 18 11:30'):
    # #             raise Exception('GDELT 2.0 Global Knowledge Graph requires dates greater than or equal to Feb 18 2015 11 pm.')
    # #     caboose = ".gkg.csv.zip"
    # else:
    #     raise ValueError('You entered an incorrect GDELT table type.'
    #                      ' Choose between \"events\",\"mentions\",'
    #                      'and \"gkg\".')


    if isinstance(dateString, list) is True or isinstance(dateString,
                                                          np.ndarray) is True:
        # print("This is before any changes {}".format(dateString))
        newdate = []
        olddateString = dateString
        date=dateString
        for l in date:
            if len(l) == 4:
                test = (str(datetime.datetime.strptime(l, '%Y')))
                newdate.append(test)
            elif len(l) == 6:
                test = str(datetime.datetime.strptime(l, '%Y%m'))
                newdate.append(test)
            else:

                test = str(parse(str(l)))
                newdate.append(test)
            # if parse(test) < parse('Feb 18 2015') and version == 2:
            #     raise ValueError(
            #         "GDELT 2.0 only supports \'Feb 18 2015 - "
            #         "Present\'queries currently. Try another date."
            #     )
        # dateString = newdate
        # print("This is the vectorizor datestring {}".format(dateString))
        if version ==1:
            if table != 'gkg':
                # print(base)
                base
                # print("After {}".format(base))

        if not (np.all(list(
                map(
                    lambda x: x > parse('2013 04 01'), list(
                        map(
                            _testdate, dateString)))))):

            return (list(
                map(lambda x: base + x + ".zip" if _testdate(
                    x).date() < parse(
                    '2013 04 01').date() else base + x + caboose,
                    dateString)))

        else:

            return list(map(lambda x: base + x + caboose, olddateString))

    elif isinstance(dateString, str) is True or len(dateString) == 1:

        if version == 1:
            if table=='events':
                if len(dateString) == 4:
                    comp = datetime.datetime.strptime(dateString,'%Y')
                elif len(dateString) == 6:
                    comp = datetime.datetime.strptime(dateString, '%Y%m')
                else:
                    comp = parse(dateString)
                if comp < parse('2013 Apr 01'):
                    caboose = ".zip"
                elif table == 'events':
                    caboose = ".export.CSV.zip"

        if isinstance(dateString, list) is True or isinstance(
                dateString, np.ndarray) is True:
            dateString = dateString[0]
            if parse(dateString[0]) < parse('2013 Apr 01'):
                caboose = ".zip"

        return base + dateString + caboose

def _geofilter(frame):
    """Filters dataframe for conversion to geojson or shapefile"""
    try:
        import geopandas as gpd

        # Remove rows with no latitude and longitude
        try:

            filresults = frame[(frame['ActionGeo_Lat'].notnull()
                                ) | (frame['ActionGeo_Long'].notnull()
                                     )]
        except:

            filresults = frame[(frame['actiongeolat'].notnull()
                                ) | (frame['actiongeolong'].notnull()
                                     )]
        gdf = gpd.GeoDataFrame(filresults.assign(geometry=_parallelize_dataframe(filresults)),
                               crs={'init': 'epsg:4326'})
        gdf.columns = list(map(lambda x: (x.replace('_', "")).lower(), gdf.columns))

        # final = gpd.GeoDataFrame(filresults.assign(geometry=_parallelize_dataframe(filresults)),
        #                               crs={'init': 'epsg:4326'})

        final = gdf[gdf.geometry.notnull()]

        return final


    except:
        raise ImportError("You need to install geopandas for this feature.")
