from dateutil.parser import parse
import traceback,sys
import pandas as pd
import numpy as np
import datetime
import requests
from gdelt.datecheck import dateInputCheck


class gdeltSearch(object):
    """Placeholder string"""
    
    def __init__(self,
                 gdelt2MasterUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt',
                 gdelt1MasterUrl = 'http://data.gdeltproject.org/events/index.html',
                 tblType = None,
                 headers = None,
                 masterdf = None,
                 clean = None,
                 queryTime = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
                 ):
        self.gdelt2MasterUrl=gdelt2MasterUrl
        self.gdelt1MasterUrl=gdelt1MasterUrl
        self.clean = map(
                    lambda x: x.split(' '),
                    requests.get(self.gdelt2MasterUrl).content.split('\n')
                        )
        del self.clean[-1]
        self.masterdf = pd.DataFrame(self.clean)
        self.masterdf.fillna('', inplace=True)
        self.queryTime=queryTime
        
        def Search(date):
            return 2 + 3
