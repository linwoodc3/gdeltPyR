from StringIO import StringIO
import pandas as pd
import requests
import zipfile
import re

def downloadAndExtract(gdeltUrl):
    """Downloads and extracts GDELT zips without saving to disk"""
    
    response = requests.get(gdeltUrl, stream=True)
    zipdata = StringIO()
    zipdata.write(response.content)
    gdelt_zipfile = zipfile.ZipFile(zipdata,'r')
    name = re.search('(([\d]{4,}).*)',gdelt_zipfile.namelist()[0]).group().replace('.zip',"")
    data = gdelt_zipfile.read(name)
    gdelt_zipfile.close()
    del zipdata,gdelt_zipfile,name,response
    return pd.read_csv(StringIO(data),delimiter='\t',header=None)
    

def addHeader(table):
    """Returns the header rows for the dataframe"""
    
    if table == "gkg":
        headers = gkgHeaders.tableId.tolist()
    
    elif table == "mentions" or table == "events":
        
        headers = eventsDbHeaders.tableId.tolist() + mentionsHeaders.tableId.tolist()
        
    return headers