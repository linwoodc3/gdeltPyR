from dateutil.parser import parse
import traceback,sys
import numpy as np
import datetime

def dateInputCheck(date, version):
        """Function to check date entered by user.

        Example

        Parameters
            ----------
            date : {string or list}, 
                Input data, where ``date`` is a single date string, 
                two dates representing a range, or several dates \
                that represent individual days of interest.
        Returns
        -------
        self : None
            Returns self.
        """
        
        if isinstance(date,str):
            if date != "":
                if parse(date) > datetime.datetime.now():
                    raise ValueError(
                        'Your date is greater than the current date. Please enter a relevant date.'
                        )
                elif parse(date)<parse('Feb 18 2015') and int(version) != 1:
                    raise ValueError(
                        '''GDELT 2.0 only supports \'Feb 18 2015 - Present\' queries currently. Try another date.'''
                        )

        elif isinstance(date,list):
            if len(date)==1:
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
        
            elif len(date)==2 and isinstance(date,list):
                
                try:
                    map(parse,date)
                except Exception as exc:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                    traceback.print_exception(exc_type, exc_value, exc_traceback,
                                              limit=2, file=sys.stdout)
                    raise ValueError(
                        "One or more of your input date strings does not parse to a date format. Check input."
                        )

                if bool(parse(date[0])<parse(date[1])) == False:
                    raise ValueError(
                        'Start date greater than end date. Check date strings.'
                        )

                elif np.all(
                        np.logical_not(np.array(map(parse,date))> datetime.datetime.now())
                        ) == False:
                    raise ValueError(
                        "One of your dates is greater than the current date. Check input date strings."
                        )
                elif np.any(
                    np.logical_not(np.array(map(parse,date)
                                           )> parse("Feb 18 2015"))) == True and int(version) != 1:
                    raise ValueError(
                        '''GDELT 2.0 only supports \'Feb 18 2015 - Present\'queries currently. Try another date.'''
                        )


            elif len(date)>2:

                try:
                    map(parse,date)
                except Exception as exc:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                    traceback.print_exception(exc_type, exc_value, exc_traceback,
                                              limit=2, file=sys.stdout)
                    raise ValueError(
                        "One or more of your input date strings does not parse to a date format. Check input."
                        )

                if np.all(
                        np.logical_not(np.array(map(parse,date))> datetime.datetime.now())
                        ) == False:
                    raise ValueError(
                        "One or more of your input date strings does not parse to a date format. Check input."
                        )
                    
                elif np.any(
                    np.logical_not(np.array(map(parse,date)
                                           )> parse("Feb 18 2015"))) == True and int(version) != 1:
                    raise ValueError(
                        '''GDELT 2.0 only supports \'Feb 18 2015 - Present\'queries currently. Try another date.'''
                        )
                    
def tblCheck(dataframe,tbl):
    '''Checking the input of tblType.'''
    if tbl == 'events' or tbl == '' or tbl == 'mentions' or tbl == None:
        resultsUrlList = dataframe[2][dataframe[2].str.contains('export|mentions')]
    elif tbl == 'gkg':
        resultsUrlList = dataframe[2][dataframe[2].str.contains('gkg')]
    else:
        raise ValueError ("Incorrect parameter \'{0}\' entered.  Did you mean to use \'{0}\' as the parameter?\nPlease check your \'tblType\' parameters.".format(tblType))
    return resultsUrlList