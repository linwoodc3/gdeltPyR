import datetime
import sys
import traceback

import numpy as np
from dateutil.parser import parse


def dateInputCheck(date, version):
    """Function to check date entered by user.



    Parameters
    ----------
        date : {string or list},
            Input data, where ``date`` is a single date string,
            two dates representing a range, or several dates
            that represent individual days of interest.

        version: {int},
            An integer between 1 and 2 representing the version
            of GDELT used.
    Returns
    -------
    self : None
        Returns self.
        :param date:
        :param version:
    """

    if isinstance(date, str):

        if date != "":
            if parse(date) > datetime.datetime.now():
                raise ValueError(
                    'Your date is greater than the current date. Please enter a relevant date.'
                )
            elif parse(date) < parse('Feb 18 2015') and int(version) != 1:
                raise ValueError(
                    '''GDELT 2.0 only supports \'Feb 18 2015 - Present\' queries currently. Try another date.'''
                )
        if version == 1 and parse(date).date() == datetime.datetime.now().date():
            print('yay')
            raise ValueError(
                ("You entered today's date for a GDELT 1.0 query.  GDELT 1.0's most recent data is always the\n"
                 "trailing day (i.e. {0}).  Please retry your query.").format(
                    np.datetime64(datetime.datetime.now().date()) - np.timedelta64(1, 'D'))
            )

    elif isinstance(date, list) or isinstance(date, np.ndarray):

        if len(date) == 1:

            try:
                if parse("".join(date)) > datetime.datetime.now():
                    raise ValueError(
                        'Your date is greater than the current date.  Please enter a relevant date.'
                    )
                elif parse("".join(date)) < parse('Feb 18 2015') and int(version) != 1:
                    raise ValueError(
                        '''GDELT 2.0 only supports \'Feb 18 2015 - Present\'queries currently. Try another date.'''
                    )
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError(
                    "One or more of your input date strings does not parse to a date format. Check input."
                )
            return "".join(date)

        elif len(date) == 2 and (isinstance(date, list) or isinstance(date, np.ndarray)):


            try:
                map(parse, date)
            except Exception as exc:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError(
                    "One or more of your input date strings does not parse to a date format. Check input."
                )

            if bool(parse(date[0]) < parse(date[1])) == False:
                raise ValueError(
                    'Start date greater than end date. Check date strings.'
                )

            elif np.all(
                    np.logical_not(np.array(map(parse, date)) > datetime.datetime.now())
            ) == False:
                raise ValueError(
                    "One of your dates is greater than the current date. Check input date strings."
                )
            elif np.any(
                    np.logical_not(np.array(map(parse, date)
                                            ) > parse("Feb 18 2015"))) == True and int(version) != 1:
                raise ValueError(
                    '''GDELT 2.0 only supports \'Feb 18 2015 - Present\'queries currently. Try another date.'''
                )

            elif version == 1:
                if np.all(
                        np.logical_not(np.array(map(lambda x: parse(x), date), dtype='datetime64[D]') >= np.datetime64(
                            datetime.datetime.now().date()))) == False:
                    raise ValueError(
                        '''You have today's date in your query for GDELT 1.0.  GDELT 1.0\'s most recent\ndata'''
                        '''is always the trailing day (i.e. {0}).  Please retry your query.'''.format(
                            np.datetime64(datetime.datetime.now().date()) - np.timedelta64(1, 'D'))
                    )


        elif len(date) > 2:

            try:
                map(parse, date)
            except Exception as exc:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError(
                    "One or more of your input date strings does not parse to a date format. Check input."
                )

            if np.all(
                    np.logical_not(np.array(map(parse, date)) > datetime.datetime.now())
            ) == False:
                raise ValueError(
                    "One or more of your input date strings does not parse to a date format. Check input."
                )

            elif np.any(
                    np.logical_not(np.array(map(parse, date)
                                            ) > parse("Feb 18 2015"))) == True and int(version) != 1:
                raise ValueError(
                    '''GDELT 2.0 only supports \'Feb 18 2015 - Present\'queries currently. Try another date.'''
                )
            elif version == 1:

                if np.all(
                        np.logical_not(np.array(map(lambda x: parse(x), date), dtype='datetime64[D]') >= np.datetime64(
                            datetime.datetime.now().date()))) == False:
                    raise ValueError(
                        '''You have today's date in your query for GDELT 1.0.  GDELT 1.0\'s most recent\ndata'''
                        '''is always the trailing day (i.e. {0}).  Please retry your query.'''.format(
                            np.datetime64(datetime.datetime.now().date()) - np.timedelta64(1, 'D'))
                    )


def tblCheck(dataframe, tbl):
    """Checking the input of tblType."""
    if tbl == 'events' or tbl == '' or tbl == 'mentions':
        resultsUrlList = dataframe[2][dataframe[2].str.contains('export|mentions')]
    elif tbl == 'gkg':
        resultsUrlList = dataframe[2][dataframe[2].str.contains('gkg')]
    else:
        raise ValueError(
            "Incorrect parameter \'{0}\' entered.  Did you mean to use \'{0}\' as the parameter?"
            "\nPlease check your \'tblType\' parameters.".format(tbl))
    return resultsUrlList
