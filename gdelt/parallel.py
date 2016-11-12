import datetime
import multiprocessing
import os
import re
from functools import partial
import warnings
from io import BytesIO
from multiprocessing import cpu_count,current_process,freeze_support

import pandas as pd
import requests


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class NoDaemonProcessPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


def mp_worker(url, table=None):
    """Code to download the urls and blow away the buffer to keep memory usage down"""
    warnings.filterwarnings("ignore",
                            '.*have mixed types. Specify dtype.*')  # ignore pandas warning for GDELT 1.0 dtype
    start = datetime.datetime.now()
    proc_name = current_process().name

    # print (multiprocessing.current_process().name)
    proc = os.getpid()
    # print ('Starting {0}-{1}'.format(proc_name,proc))
    r = requests.get(url)
    # print (multiprocessing.Process(name=multiprocessing.current_process().name).is_alive())
    try:
        buffer = BytesIO(r.content)
        if table == 'events':


            frame = pd.read_csv(buffer, compression='zip', sep='\t',
                                header=None, warn_bad_lines=False,
                                dtype={26: 'str', 27: 'str', 28: 'str'},
                                parse_dates=[1, 2])


        elif table == 'gkg':
            frame = pd.read_csv(buffer, compression='zip', sep='\t',
                                parse_dates=['DATE'], warn_bad_lines=False)

        else:

            frame = pd.read_csv(buffer, compression='zip', sep='\t',
                                header=None, warn_bad_lines=False)
        end = datetime.datetime.now() - start
        # print ("{0} with id {1} finished processing in {2}".format(proc_name,proc,end))
        buffer.flush()
        buffer.close()
        return frame

    except:
        try:
            message = "GDELT did not return data for date time " \
                      "{0}".format(re.search('[0-9]{4,18}', url).group())
            warnings.warn(message)
        except:
            message = "No data returned for {0}".format(r.url)
            warnings.warn(message)

if __name__ == '__main__':
    freeze_support()
    Process(target=mp_worker).start()


##########################
#
#########################﻿﻿
# We must import this explicitly, it is not imported by the top-level
# # multiprocessing module.
# import multiprocessing.pool
# import time
#
# from random import randint
#
#
# class NoDaemonProcess(multiprocessing.Process):
#     # make 'daemon' attribute always return False
#     def _get_daemon(self):
#         return False
#     def _set_daemon(self, value):
#         pass
#     daemon = property(_get_daemon, _set_daemon)
#
# # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# # because the latter is only a wrapper function, not a proper class.
# class MyPool(multiprocessing.pool.Pool):
#     Process = NoDaemonProcess
#
# def sleepawhile(t):
#     print("Sleeping %i seconds..." % t)
#     time.sleep(t)
#     return t
#
# def work(num_procs):
#     print("Creating %i (daemon) workers and jobs in child." % num_procs)
#     pool = multiprocessing.Pool(num_procs)
#
#     result = pool.map(sleepawhile,
#         [randint(1, 5) for x in range(num_procs)])
#
#     # The following is not really needed, since the (daemon) workers of the
#     # child's pool are killed when the child is terminated, but it's good
#     # practice to cleanup after ourselves anyway.
#     pool.close()
#     pool.join()
#     return result
#
# def test():
#     print("Creating 5 (non-daemon) workers and jobs in main process.")
#     pool = MyPool(5)
#
#     result = pool.map(work, [randint(1, 5) for x in range(5)])
#
#     pool.close()
#     pool.join()
#     print(result)
#
# if __name__ == '__main__':
    test()