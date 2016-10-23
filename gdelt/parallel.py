import datetime
import multiprocessing
import os
import time
from io import BytesIO
from multiprocessing import current_process

import pandas as pd
import requests


def mp_worker(url):
    start = datetime.datetime.now()
    proc_name = current_process().name
    # print (multiprocessing.current_process().name)
    proc = os.getpid()
    # print ('Starting {0}-{1}'.format(proc_name,proc))
    r = requests.get(url)
    # print (multiprocessing.Process(name=multiprocessing.current_process().name).is_alive())
    frame = pd.read_csv(BytesIO(r.content), compression='zip', sep='\t', header=None)
    end = datetime.datetime.now() - start
    # print ("{0} with id {1} finished processing in {2}".format(proc_name,proc,end))
    return frame


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
