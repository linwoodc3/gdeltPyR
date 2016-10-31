import datetime
import multiprocessing
import os
import re
import time
import warnings
from io import BytesIO
from multiprocessing import current_process

import pandas as pd
import requests



def mp_worker(url,table=None):

    '''Code to download the urls and blow away the buffer to keep memory usage down'''
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

            frame = pd.read_csv(buffer,compression='zip', sep='\t',
                            header=None, warn_bad_lines=False,
                                dtype={26:'str',27:'str',28:'str'},
                                parse_dates=[1,2,59])
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


def mp_handler(function, urllist):
    result = []
    p = multiprocessing.Pool(4)
    dfs = p.imap_unordered(function, urllist)
    if dfs:
        try:
            result.extend(dfs)
            time.sleep(1)
        except:
            pass

    else:
        pass
    return result

# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
# http://stackoverflow.com/questions/20577472/how-to-keep-track-of-asynchronous-results-returned-from-a-multiprocessing-pool

# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
# http://stackoverflow.com/questions/20577472/how-to-keep-track-of-asynchronous-results-returned-from-a-multiprocessing-pool

#
# def parallelDownload():
#     p = Pool()
#     results = []
#     rs = p.imap_unordered(downloadAndExtract, urlList)
#     for frame in rs:
#         results.append(frame)
#     # print results
#     # print results[0].head()
#     return pd.concat(results).reset_index(drop=True)
#
# if __name__ == '__main__':
#     parallelDownload(function,urlList)
