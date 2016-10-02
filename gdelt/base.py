
import traceback,sys
import pandas as pd
import numpy as np
import lxml.html as lh
import datetime
import requests
from gdelt.inputChecks import (dateInputCheck,tblCheck)
from gdelt.dateFuncs import (parse_date, dateFormatter,
                             dateRanger,gdeltRangeString)
from gdelt.vectorizingFuncs import (vectorizer, urlFinder,
                                    vectorizedUrlFinder, downloadVectorizer)
from gdelt.extractors import (downloadAndExtract,addHeader)
from gdelt.parallel import parallelDownload

import os
this_dir, this_filename = os.path.split(__file__)
CSV_PATH = os.path.join(this_dir, "utils", "schema_csvs")
print(CSV_PATH)



class gdelt(object):
    """Placeholder string"""
    
    def __init__(self,
                 gdelt2MasterUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt',
                 gdelt1MasterUrl = 'http://data.gdeltproject.org/events/', # index.html, events/20160930.export.CSV.zip
                 version = 2.0
                 ):
        
        self.version=version
        
        if int(version) == 2:
            self.baseUrl = gdelt2MasterUrl
        elif int(version) == 1:
            self.baseUrl = gdelt1MasterUrl
        
        
    
        
    def Search(self,
              date,
              table='events',
              headers = None,
              masterdf = None,
              clean = None,
              queryTime = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
              ):
        dateInputCheck(date,self.version)
        self.version = self.version
        self.date = date 
        self.baseUrl=self.baseUrl
        self.table=table
        # self.mask = dateMasker(date,version=self.version)
        self.mask = vectorizer(gdeltRangeString,dateRanger(self.date))
        print self.baseUrl
        if int(self.version) == 2:
            # Get the list of files for download
            directory = requests.get(self.baseUrl)
            clean = directory.content.split('\n')
            clean = map(lambda x: x.split(' '),clean)
            del clean[-1]
            
            self.masterdf = pd.DataFrame(clean)
            self.masterdf.fillna('',inplace=True)
        
            
            
            # vectorizer returns today's date for odd reason; return none and remove
            if isinstance(self.mask,list)==True:
                try:
                    self.mask.remove('None')
                except:
                    pass
                filterString="|".join(self.mask)
            else:
                filterString=self.mask
            
            self.filtereddf = self.masterdf[2][self.masterdf[2].str.contains(filterString)].reset_index(drop=True)
            
            if self.table == 'events' or self.table=='':
                self.filtereddf=self.filtereddf[self.filtereddf.str.contains('export')]
                self.mentionsdf=self.filtereddf[self.filtereddf.str.contains('mentions')]
            elif self.table == 'gkg':
                self.filtereddf=self.filtereddf[self.filtereddf.str.contains('gkg')]
                 
            else:
                raise ValueError('Incorrect table entry')
                
            self.results=parallelDownload(downloadAndExtract,self.filtereddf.tolist())
            return self.results
            
            
            
            
           
                
    
            
            

        # GDELT Version 1.0 Search
        elif int(self.version) == 1:
            
            page = requests.get(self.baseUrl+'index.html')
            doc = lh.fromstring(page.content)
            link_list = doc.xpath("//*/ul/li/a/@href")
            self.masterdf = pd.DataFrame(link_list)
            
            if isinstance(self.mask,list)==True:
                try:
                    self.mask.remove('None')
                except:
                    pass
                filterString="|".join(self.mask)
            else:
                filterString=self.mask
            self.filtereddf = (self.masterdf[0][self.masterdf[0].str.contains(filterString)].reset_index(drop=True)).apply(lambda x: self.baseUrl+x)
            self.results=parallelDownload(downloadAndExtract,self.filtereddf.tolist())
            return self.results
            
          
        
            
            

        
    
    
         
    
        
        
        
        
        
            
            

        
        
        
