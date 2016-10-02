from multiprocessing import Pool
import requests
import pandas as pd
import zipfile
from StringIO import StringIO
import re

from gdelt.extractors import (downloadAndExtract,addHeader)

def parallelDownload(function,urlList):
    p = Pool()
    return pd.concat(p.map(downloadAndExtract, urlList)).reset_index(drop=True)

if __name__ == '__main__':
    parallelDownload(function,urlList)