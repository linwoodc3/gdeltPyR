#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##################################
# Standard library imports
##################################
import datetime
import warnings

##################################
# Third party imports
##################################
import numpy as np
from dateutil.parser import parse

##################################
# Local imports
##################################
# from gdelt.vectorizingFuncs import _vectorizer


def _parse_date(date_string):
    """Convert a date string to a Python datetime object.

    Parameters
    ----------
    date_string : string
        A date, written as a string

    Returns
    -------
    datetime object
        Python datetime object.

    Example
    --------
    This is a simple function to return a datetime object from a string.

    >>> _parse_date('2016 10 01')
    datetime.datetime(2016, 10, 1, 0, 0)
    """

    try:
        return np.where(isinstance(parse(date_string), datetime.datetime),
                        parse(date_string), "Error")
    except Exception as e:
        return "You entered an incorrect date.  Check your date format."


def _dateformatter(date_string):
    """Converts arbritary date string into standardized date string

    Parameters
    ----------
    date_string : string
        A date, written as a string

    Returns
    -------
    string
        Standardized date string in YYYY-MM-DD format.

    Example
    --------
    This is a simple function to convert entered date strings into a standard date string format.

    >>> _dateformatter('2016 10 01')
    '2016-10-01'
    """
    return parse(date_string).strftime("%Y-%m-%d")


def _dateRanger(originalArray):
    """Function to vectorize date formatting function.
    Creates datetime.date objects for each day in the range
    and stores in a numpy array.

    """

    minutes = list(map(str, range(00, 60, 15)))
    hours = list(map(str, range(0, 24)))
    times = []
    for l in hours:
        if int(l) < 10:
            l = "0" + l
        for k in minutes:
            if k == "0":
                k = '00'
            times.append('{0}:{1}'.format(l, k))

    if isinstance(originalArray, str):
        """Check user input to retrieve date query."""

        return np.where(len(originalArray) == 0, "crazy",
                        _parse_date(originalArray))

    elif isinstance(originalArray, list):

        if len(originalArray) == 1:
            return np.array(parse("".join(originalArray)))
        elif len(originalArray) > 2:
            #
            #             return np.array(map(parse,originalArray),dtype='datetime64[D]').tolist()
            return np.array(list(map(lambda x: parse(x), originalArray)))
        else:

            cleaner = np.vectorize(_dateformatter)
            converted = cleaner(originalArray).tolist()
            dates = np.arange(converted[0], converted[1],
                              dtype='datetime64[D]')
            dates = list(map(lambda x: datetime.datetime.combine(
                x, datetime.datetime.min.time()), dates.tolist()))
            if len(originalArray) == 2:
                adder = np.datetime64(parse(converted[1]).date())
                adder = datetime.datetime.combine(adder.tolist(),
                                                  datetime.datetime.min.time())
                return np.append(dates,
                                 adder)  # numpy range is not endpoint inclusive
            else:
                pass
            return np.array(dates)


def _gdeltRangeString(element, coverage=None, version=2.0):
    """Takes a numpy datetime and converts to string"""

    ########################
    # Numpy datetime to object
    ########################


    ########################
    #     Current day check
    ########################


    minutes = list(map(str, range(00, 60, 15)))
    hours = list(map(str, range(0, 24)))
    times = []
    for l in hours:
        if int(l) < 10:
            l = "0" + l
        for k in minutes:
            if k == "0":
                k = '00'
            times.append('{0}:{1}'.format(l, k))

    element = element.tolist()

    hour = datetime.datetime.now().hour
    multiplier = (datetime.datetime.now().minute // 15)
    multiple = 15 * multiplier
    conditioner = multiplier + 1

    # calculate nearest 15 minute interval
    if not isinstance(element, list):


        if element.date() == datetime.datetime.now().date():
            if coverage and int(version) != 1:

                converted = np.array(
                    list(map(
                        lambda x: np.datetime64(parse(str(element) + " " + x)
                                                ).tolist().strftime(
                            '%Y%m%d%H%M%S'
                        ), times[:hour * 4 + conditioner])))
            else:

                converted = datetime.datetime.now().replace(
                    minute=multiple, second=0).strftime('%Y%m%d%H%M%S')

        else:
            if coverage and int(version) != 1:
                converted = restOfDay = np.array(
                    list(map(
                        lambda x: np.datetime64(parse(str(element) + " " + x)
                                                ).tolist().strftime(
                            '%Y%m%d%H%M%S'
                        ), times[:])))
            else:

                converted = element.replace(minute=int(
                    multiple), second=0).strftime('%Y%m%d%H%M%S')
                if parse(converted)< datetime.datetime.now():
                    converted = element.replace(minute=45, second=0,hour=23).strftime('%Y%m%d%H%M%S')


    #################################
    # All non-current dates section
    #################################

    else:

        ####################
        # Handling list
        ####################

        if isinstance(element, list) is True:

            #             converted = map(lambda x: x.strftime('%Y%m%d%H%M%S'),element)
            converted = list(map(lambda x: (
                datetime.datetime.combine(x, datetime.time.min) +
                datetime.timedelta(
                    minutes=45, hours=23
                )
            ).strftime('%Y%m%d%H%M%S'), element))

        else:
            converted = (datetime.datetime.combine(
                element, datetime.time.min) +
                         datetime.timedelta(
                             minutes=45, hours=23
                         )
                         ).strftime('%Y%m%d%H%M%S')

        ####################
        # Return all 15 min intervals
        ####################
        if coverage and int(version) != 1:

            converted = []
            for i in element:
                converted.append(np.array(
                    list(map(
                        lambda x: np.datetime64(parse(str(i) + " " + x)
                                                ).tolist().strftime(
                            '%Y%m%d%H%M%S'
                        ), times[:]))))
            converted = np.concatenate(converted, axis=0)
            if len(converted.tolist()) >= (5 * 192):
                warnText = ("This query will download {0} files, and likely "
                            "exhaust your memory with possibly 10s of "
                            "GBs of data in this single query.Hit Ctr-C to kill "
                            "this query if you do not want to "
                            "continue.".format(len(converted.tolist())))
                warnings.warn(warnText)

    ########################
    # Version 1 Datestrings
    #########################
    if int(version) == 1:
        if isinstance(converted, list) is True:

            converted = list(
                map(lambda x: np.where((parse(x) >= parse(
                    '2013 04 01')), parse(x).strftime('%Y%m%d%H%M%S')[:8],
                                       np.where((parse(x) < parse(
                                           '2006 01 01') and (
                                                     int(version) == 1)),
                                                parse(x).strftime(
                                                    '%Y%m%d%H%M%S')[:4],
                                                parse(x).strftime(
                                                    '%Y%m%d%H%M%S')[:6]))
                    , converted))
            converted = list(map(lambda x: x.tolist(), converted))
            converted = list(set(converted))  # account for duplicates
        else:
            converted = np.where((parse(converted) >= parse('2013 04 01')),
                                 parse(converted).strftime('%Y%m%d%H%M%S')[:8],
                                 np.where((parse(converted) < parse(
                                     '2006 01 01') and (int(version) == 1)),
                                          parse(converted).strftime(
                                              '%Y%m%d%H%M%S')[:4],
                                          parse(converted).strftime(
                                              '%Y%m%d%H%M%S')[:6])).tolist()

    return converted


# def _dateMasker(dateString, version):
#     mask = (np.where((int(version == 1) and parse(dateString) >= parse(
#         '2013 04 01')) or (int(version) == 2),
#                      _vectorizer(_gdeltRangeString, _dateRanger(dateString))[:8],
#                      np.where(int(version) == 1 and parse(
#                          dateString) < parse('2006 01'),
#                               _vectorizer(_gdeltRangeString, _dateRanger(
#                                   dateString))[:4],
#                               _vectorizer(_gdeltRangeString, _dateRanger(
#                                   dateString))[:6]))).tolist()
#     return mask

