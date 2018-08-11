#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

import datetime
import multiprocessing
import re
import time
import warnings
from io import BytesIO
from multiprocessing import freeze_support

import pandas as pd
import requests


# class NoDaemonProcess(multiprocessing.Process):
#     # make 'daemon' attribute always return False
#     def _get_daemon(self):
#         return False
#
#     def _set_daemon(self, value):
#         pass
#
#     daemon = property(_get_daemon, _set_daemon)
#
#
# # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# # because the latter is only a wrapper function, not a proper class.
# class NoDaemonProcessPool(multiprocessing.pool.Pool):
#     Process = NoDaemonProcess


def _mp_worker(url, table=None, proxies=None):
    """Code to download the urls and blow away the buffer to keep memory usage
     down"""

    warnings.filterwarnings("ignore",
                            '.*have mixed types. Specify dtype.*')  # ignore
    # pandas warning for GDELT 1.0 dtype
    # start = datetime.datetime.now()
    # proc_name = current_process().name
    #
    # proc = os.getpid()

    #################################
    # DEBUG Prints
    #################################

    # print(url)
    # print(multiprocessing.current_process().name)
    # print('Starting {0}-{1}'.format(proc_name, proc))
    time.sleep(0.001)
    # print("Getting to request process finished in {}".\
    # format(datetime.datetime.now() - start))
    # start = datetime.datetime.now()
    #################################

    r = requests.get(url, proxies=proxies, timeout=5)
    # print("Request finished in {}".format(datetime.datetime.now() - start))
    if r.status_code == 404:
        message = "GDELT does not have a url for date time " \
                  "{0}".format(re.search('[0-9]{4,18}', url).group())
        warnings.warn(message)

    # print (multiprocessing.Process(name=multiprocessing.current_process().\
    # name).is_alive())
    start = datetime.datetime.now()
    try:
        buffer = BytesIO(r.content)
        if table == 'events':

            frame = pd.read_csv(buffer, compression='zip', sep='\t',
                                header=None, warn_bad_lines=False,
                                dtype={26: 'str', 27: 'str', 28: 'str'})  # ,
            # parse_dates=[1, 2])

        elif table == 'gkg':
            frame = pd.read_csv(buffer, compression='zip', sep='\t',
                                header=None, warn_bad_lines=False)
            # parse_dates=['DATE'], warn_bad_lines=False)

        else:  # pragma: no cover

            frame = pd.read_csv(buffer, compression='zip', sep='\t',
                                header=None, warn_bad_lines=False)

        # print("Pandas load finished in {}".\
        # format(datetime.datetime.now() - start))
        # print ("{0} with id {1} finished processing in {2}".\
        # format(proc_name,proc,end))
        buffer.flush()
        buffer.close()
        return frame

    except:
        try:
            message = "GDELT did not return data for date time " \
                      "{0}".format(re.search('[0-9]{4,18}', url).group())
            warnings.warn(message)
        except:  # pragma: no cover
            message = "No data returned for {0}".format(r.url)
            warnings.warn(message)


if __name__ == '__main__':  # pragma: no cover
    freeze_support()
    p = multiprocessing.Process(target=_mp_worker)
    p.start()
    # # Wait 10 seconds for foo
    # # time.sleep(35)
    # #
    # # # Terminate foo
    # # p.terminate()
    #
    # # Cleanup
    # p.join()
