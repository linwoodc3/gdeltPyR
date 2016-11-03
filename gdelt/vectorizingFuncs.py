import numpy as np
import pandas as pd
from dateutil.parser import parse


def vectorizer(function, dateArray):
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


def urlFinder(dataframe, targetDate, col):
    return dataframe[col][dataframe[col].str.contains(targetDate)]


def vectorizedUrlFinder(function, urlList, frame):
    helper = np.vectorize(function)
    return pd.concat(helper(urlList, frame).tolist())


def downloadVectorizer(function, urlList):
    """Vectorized function to download urls"""
    helper = np.vectorize(function)
    return pd.concat(helper(urlList).tolist()).reset_index(drop=True)


def urlBuilder(dateString, version, table='events'):
    """
    Takes date string from gdeltRange string and creates GDELT urls


    Parameters
    ------------

    table types:
                * events and mentions (default)
                * gkg
                * mentions only
                :param dateString:
                :param version:
                :param table:
    """
    if version == 2:
        base = "http://data.gdeltproject.org/gdeltv2/"

    if version == 1:

        base = "http://data.gdeltproject.org/"

    if table == "events":
        base += 'events/'
        caboose = ".export.CSV.zip"
    elif table == "mentions":
        caboose = ".mentions.CSV.zip"
    elif table == "gkg":
        if version == 1:
            base += 'gkg/'
        caboose = ".gkg.csv.zip"
    else:
        raise ValueError('You entered an incorrect GDELT table type.'
                         ' Choose between \"events\",\"mentions\",'
                         'and \"gkg\".')

    if isinstance(dateString, list) is True or isinstance(dateString,
                                                          np.ndarray) is True:

        if (np.all(list(
                map(
                    lambda x: x > parse('2013 04 1'), list(
                        map(
                            parse, dateString)))))) == False:

            return (list(
                map(lambda x: base + x + ".zip" if parse(
                    x).date() < parse(
                    '2013 04 01').date() else base + x + caboose,
                    dateString)))

        else:

            return list(map(lambda x: base + x + caboose, dateString))

    elif isinstance(dateString, str) is True or len(dateString) == 1:
        if version == 1:

            if parse(dateString) < parse('2013 Apr 01'):
                caboose = ".zip"
        if isinstance(dateString, list) is True or isinstance(
                dateString, np.ndarray) is True:
            dateString = dateString[0]
            if parse(dateString[0]) < parse('2013 Apr 01'):
                caboose = ".zip"

        return base + dateString + caboose
