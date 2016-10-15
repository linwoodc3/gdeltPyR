import datetime

import lxml.html as lh
import pandas as pd
import requests

from gdelt.dateFuncs import (dateRanger, gdeltRangeString)
from gdelt.extractors import (downloadAndExtract)
from gdelt.getHeaders import events1Heads, events2Heads, mentionsHeads, gkgHeads
from gdelt.inputChecks import (dateInputCheck)
from gdelt.parallel import parallelDownload
from gdelt.vectorizingFuncs import (vectorizer)


# import os
# this_dir, this_filename = os.path.split(__file__)
# CSV_PATH = os.path.join(this_dir, "utils","schema_csvs","GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv")
# print(CSV_PATH)

# print HEADER_PATH = os.path.join(this_dir,"utils","schema_csvs","GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv")
    

# header = pd.read_csv(HEADER_PATH,delimiter='\t',usecols=['tableId','dataType','Description'])

# print header

##############################
# Core GDELT class
##############################
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
        
        
    ###############################
    # Searcher function for GDELT
    ###############################
        
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
        self.mask = vectorizer(gdeltRangeString,dateRanger(self.date))
        
        
        
        
        #####################################
        # GDELT Version 2.0 Analytics
        #####################################
        
        if int(self.version) == 2:
            
            #########################################
            # Create the filter string of dates
            #########################################
            
            if isinstance(self.mask,list)==True :
                filterString="|".join(self.mask)
            else:
                filterString=self.mask

            ########################################
            # Get the master list of GDELT files
            ########################################
            
            directory = requests.get(self.baseUrl)
            clean = directory.content.split('\n')
            clean = map(lambda x: x.split(' '),clean)
            del clean[-1]
            
            self.masterdf = pd.DataFrame(clean)
            self.masterdf.fillna('',inplace=True)
            

            
            ########################################
            # Filter the master list of CSVs
            # Use filter string from above
            ########################################
            
            self.filtereddf = self.masterdf[2][self.masterdf[2].str.contains(filterString)].reset_index(drop=True)
            
            
            ###########################################
            # Filter the master list based on table
            ###########################################
            
            if self.table == 'events' or self.table=='':
                self.eventsdf=self.filtereddf[self.filtereddf.str.contains('export')]
                self.mentionsdf=self.filtereddf[self.filtereddf.str.contains('mentions')]
            
                
                ###################################
                # Parallel function to download results
                # Set headers
                ###################################
                
                self.results=parallelDownload(downloadAndExtract,self.eventsdf.tolist())
                print(self.results.head())
                self.results.columns = events2Heads()
                
                self.mentions=parallelDownload(downloadAndExtract,self.mentionsdf.tolist())
                self.mentions.columns = mentionsHeads()
                self.finalResults = pd.merge(self.results,self.mentions,on='GLOBALEVENTID')
                return self.finalResults



            elif self.table == 'gkg':
                self.gkgdf = self.filtereddf[self.filtereddf.str.contains('gkg')]
                self.gkg = parallelDownload(downloadAndExtract, self.gkgdf.tolist())
                self.gkg.columns = gkgHeads()
                return self.gkg

            else:
                raise ValueError('Incorrect table entry')
            
            

        #####################################
        # GDELT Version 1.0 Analytics
        #####################################   
          
        elif int(self.version) == 1:
            
            #########################################
            # Create the filter string of dates
            #########################################
            
            if isinstance(self.mask,list)==True:
                filterString="|".join(self.mask)
            else:
                filterString=self.mask
            
            ########################################
            # Get the master list of GDELT files
            ########################################
            
            page = requests.get(self.baseUrl+'index.html')
            doc = lh.fromstring(page.content)
            link_list = doc.xpath("//*/ul/li/a/@href")
            self.masterdf = pd.DataFrame(link_list)
            
            
            ########################################
            # Filter the master list of CSVs
            # Use filter string from above
            ########################################
            
            self.filtereddf = (self.masterdf[0][self.masterdf[0].str.contains(filterString)].reset_index(drop=True)).apply(lambda x: self.baseUrl+x)
            
            ###################################
            # Parallel function to download results
            # Set headers
            ###################################
            
            self.results=parallelDownload(downloadAndExtract,self.filtereddf.tolist())
            self.results.columns = events1Heads()
            
            return self.results
    
         
    
        
        
        
        
        
            
            

        
        
        
