from multiprocessing import Pool

import pandas as pd

from gdelt.extractors import (downloadAndExtract)


def do_work(x):
    r = downloadAndExtract(x)
    return r


def parallelDownload(function,urlList):
    p = Pool()
    results = []
    rs = p.imap_unordered(downloadAndExtract, urlList)
    for frame in rs:
        results.append(frame)
    # print results
    # print results[0].head()
    return pd.concat(results).reset_index(drop=True)

if __name__ == '__main__':
    parallelDownload(function,urlList)
