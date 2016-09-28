def dateInputCheck(date):
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
                raise ValueError('Your date is greater than the current date.\
                Please enter a relevant date.')
            elif parse(date)<parse('Feb 18 2015'):
                raise ValueError('GDELT 2.0 only supports \'Feb 18 2015 - Present\'\
                queries currently. Try another date.')

    elif isinstance(date,list):
        if len(date)==1:
            try:
                if parse("".join(date)) > datetime.datetime.now():
                    raise ValueError('Your date is greater than the current\
                    date.  Please enter a relevant date.')
                elif parse("".join(date)) < parse('Feb 18 2015'):
                    raise ValueError('GDELT 2.0 only supports \'Feb 18 2015 - Present\' \
                    queries currently. Try another date.')
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError("One or more of your input date strings does \
                not parse to a date format. Check input.")


        elif len(date)==2:
            try:
                map(parse,date)
            except Exception as exc:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError("One or more of your input date strings \
                does not parse to a date format. Check input.")

            if bool(parse(date[0])<parse(date[1])) == False:
                raise ValueError('Start date greater than end date. Check date \
                strings.')

            if np.all(
                    np.logical_not(np.array(map(parse,date))> datetime.datetime.now())
                    ) == False:
                raise ValueError("One of your dates is greater than the current \
                date. Check input date strings.")


        elif len(date)>2:

            try:
                map(parse,date)
            except Exception as exc:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError("One or more of your input date strings does \
                not parse to a date format. Check input.")

            if np.all(
                    np.logical_not(np.array(map(parse,date))> datetime.datetime.now())
                    ) == False:
                raise ValueError("One or more of your input date strings does not \
                parse to a date format. Check input.")