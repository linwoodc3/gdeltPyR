
# GDELT 1.0 Code (skip)


```python
import requests
import lxml.html as lh

gdelt_base_url = 'http://data.gdeltproject.org/events/'
gdelt_gkg_url = 'http://api.gdeltproject.org/api/v1/gkg_geojson'
# get the list of all the links on the gdelt file page
page = requests.get(gdelt_base_url+'index.html')
doc = lh.fromstring(page.content)
link_list = doc.xpath("//*/ul/li/a/@href")

# separate out those links that begin with four digits 
file_list = [x for x in link_list if str.isdigit(x[0:4])]

```


```python
masterListUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
directory = requests.get(masterListUrl)
results = directory.content.split('\n')
```


```python
results;
```


```python
import pandas as pd

pd.options.display.max_rows = 200
# df = pd.DataFrame(data.json())
```


```python
df['coords'] = df.features.apply(lambda row: row['geometry']['coordinates'])
df['lat'] = df.features.apply(lambda row: row['geometry']['coordinates'][1])
df['lon'] = df.features.apply(lambda row: row['geometry']['coordinates'][0])
df['name'] = df.features.apply(lambda row: row['properties']['name'])
df['pubdate'] = df.features.apply(lambda row: row['properties']['urlpubtimedate'])
df['urltone'] = df.features.apply(lambda row: row['properties']['urltone'])
df['mentionedNames'] = df.features.apply(lambda row: row['properties']['mentionednames'])
df['mentioinedThemes'] = df.features.apply(lambda row: row['properties']['mentionedthemes'])
df['url'] = df.features.apply(lambda row: row['properties']['url'])
```

# GDELT 2.0 Access


```python
import requests
masterListUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
directory = requests.get(masterListUrl)
clean = directory.content.split('\n')
clean = map(lambda x: x.split(' '),clean)
```

# Logic for GDELT module

Enter a date
* default is take current time and most recent file
* enter historical date; defaults to no time specificity
    * parse
    * add feature to enter time for historical and pull closest 15 minute file
    
choose a database
*  Select between events, event mentions or gkg

return it as a python or R dataframe
*  use the feather library for Python


## Parameters


```python
# table type = tblType

all = "mentions", "eventsDatabase", "gdelt knowledge graph"
gkg = ["gdelt knowledge graph"]
events = "events" "database"
mentions =  "mentions database"

alls = ['gkg','events']
```

## Global variables


```python
gkgHeaders = pd.read_csv(
    '../utils/schema_csvs/GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv',
    delimiter='\t',usecols=['tableId','dataType','Description']
    )
gkgHeaders.tableId.tolist();

eventsDbHeaders = pd.read_csv('../utils/schema_csvs/GDELT_2.0_Events_Column_Labels_Header_Row_Sep2016.csv',
                         delimiter=',',usecols=['tableId','dataType','Description'])
eventsDbHeaders.tableId.tolist();

mentionsHeaders = pd.read_csv('../utils/schema_csvs/GDELT_2.0_eventMentions_Column_Labels_Header_Row_Sep2016.tsv',
                         delimiter='\t',usecols=['tableId','dataType','Description'])
mentionsHeaders.tableId.tolist();


```


```python
strings = ['http://data.gdeltproject.org/gdeltv2/20150225234500.gkg.csv.zip',
          'http://data.gdeltproject.org/gdeltv2/20160919070000.mentions.CSV.zip',
          'http://data.gdeltproject.org/gdeltv2/20160919070000.export.CSV.zip']

dbType = re.search(
            '(mentions|export|gkg)',
            strings[2]
        ).group()
dbType
```




    'export'



## Code Pieces and Functions


```python
defaultDateEntry = ""
stringDateEntry = " 2016 09 18"
historicalDateEntry = "2015 02 25"
errorDate = "What in the heck"
```


```python
date = defaultDateEntry
time = ""
```

# Date Functionality (Date ranges)

Use the numpy date range functionality to create strings of dates between ranges in a list.  Then, use the dateutil tool to parse those strings into the correct format.  Then run a query for each date, return the dataframe, and concatenate into a single one.  


```python
import numpy as np
np.arange('2016-08-01', '2016-09-16', dtype='datetime64[D]')
```




    array(['2016-08-01', '2016-08-02', '2016-08-03', '2016-08-04',
           '2016-08-05', '2016-08-06', '2016-08-07', '2016-08-08',
           '2016-08-09', '2016-08-10', '2016-08-11', '2016-08-12',
           '2016-08-13', '2016-08-14', '2016-08-15', '2016-08-16',
           '2016-08-17', '2016-08-18', '2016-08-19', '2016-08-20',
           '2016-08-21', '2016-08-22', '2016-08-23', '2016-08-24',
           '2016-08-25', '2016-08-26', '2016-08-27', '2016-08-28',
           '2016-08-29', '2016-08-30', '2016-08-31', '2016-09-01',
           '2016-09-02', '2016-09-03', '2016-09-04', '2016-09-05',
           '2016-09-06', '2016-09-07', '2016-09-08', '2016-09-09',
           '2016-09-10', '2016-09-11', '2016-09-12', '2016-09-13',
           '2016-09-14', '2016-09-15'], dtype='datetime64[D]')



### Pulling Date information


```python
#############################################
# Parse the date
#############################################


from dateutil.parser import parse
import pandas as pd
import numpy as np 
import requests
import datetime



def parse_date(var):
    """Return datetime object from string."""
    
    try:
        return np.where(isinstance(parse(var),datetime.datetime),
                 parse(var),"Error")             
    except:
        return "You entered an incorrect date.  Check your date format."

    
def dateInputCheck(parse_DateVar):
    """Check user input to retrieve date query."""
    
    return np.where(len(parse_DateVar)==0,datetime.datetime.now(),
             parse_date(parse_DateVar)) 


def gdelt_timeString(dateInputVar):
    """Convert date to GDELT string file format for query."""
    
    multiplier = dateInputVar.tolist().minute / 15
    multiple = 15 * multiplier
    queryDate = np.where(
            multiplier > 1,dateInputVar.tolist().replace(
            minute=0, second=0) + datetime.timedelta(
            minutes=multiple),
            dateInputVar.tolist().replace(
            minute=0, second=0,microsecond=0000)
            )
    
    # Check for date equality on historical query
    modifierTip = datetime.datetime.now().replace(
        hour=0,minute=0,second=0,microsecond=0
        ) == queryDate.tolist().replace(
        hour=0,minute=0,second=0,microsecond=0
        )
    
    # Based on modifier, get oldest file for historical query
    queryDate = np.where(
        modifierTip==False,
        queryDate.tolist().replace(
            hour=23,
            minute=45,
            second=00,
            microsecond=0000
            ),queryDate
        )
    
#     print modifierTip
    return queryDate.tolist().strftime("%Y%m%d%H%M%S")

#############################################
# Match parsed date to GDELT master list
#############################################

def match_date(dateString):
    """Return dataframe with GDELT data for matching date"""
    
    masterListUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
    directory = requests.get(masterListUrl)
    results = directory.content.split('\n')
    results = map(lambda x: x.split(' '),results)
    masterListdf = pd.DataFrame(results)
    return masterListdf[
        masterListdf[2].str.contains(
            dateString
            )==True
        ]
    

```


```python
results = match_date(gdelt_timeString(dateInputCheck(date)))
```


```python
results
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>166641</th>
      <td>174299</td>
      <td>39ba2ff2f6324fc991c4e1a108156539</td>
      <td>http://data.gdeltproject.org/gdeltv2/201609212...</td>
    </tr>
    <tr>
      <th>166642</th>
      <td>439023</td>
      <td>2f07528e827198da2ef4d4edff1eb098</td>
      <td>http://data.gdeltproject.org/gdeltv2/201609212...</td>
    </tr>
    <tr>
      <th>166643</th>
      <td>16871119</td>
      <td>2e923aa27d18fed741e9b03b4c5b2d2b</td>
      <td>http://data.gdeltproject.org/gdeltv2/201609212...</td>
    </tr>
  </tbody>
</table>
</div>



## Munging Data: Extracting Specific Datasets or all of them

Work with the returned GDELT dataframe.  Specific whether we are pulling the `mentions`, `events`, or `gkg` date for the day or all.  


```python
zippie2 = results.reset_index().ix[1][2]
```


```python
#############################################
# GDELT data download and extraction
#############################################

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
    

def add_header(gdeltUrl):
    """Returns the header rows for the dataframe"""
    
    dbType = re.search(
        '(mentions|export|gkg)',
        gdeltUrl
        ).group()
    
    if dbType == "gkg":
        headers = gkgHeaders.tableId.tolist()
    
    elif dbType == "mentions":
        headers = mentionsHeaders.tableId.tolist()
        
    elif dbType == "export":
        headers = eventsDbHeaders.tableId.tolist()
        
    return headers
```


```python
zippie2
```




    'http://data.gdeltproject.org/gdeltv2/20160921230000.mentions.CSV.zip'




```python
gdelt_df = downloadAndExtract(zippie)
gdelt_df.columns = add_header(zippie)
```


```python
gdelt_df2 = downloadAndExtract(zippie2)
gdelt_df2.columns = add_header(zippie2)
```


```python
combined = gdelt_df.merge(gdelt_df2,how='right',on='GLOBALEVENTID')
```


```python
combined.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 11767 entries, 0 to 11766
    Data columns (total 76 columns):
    GLOBALEVENTID                11767 non-null float64
    SQLDATE                      2785 non-null float64
    MonthYear                    2785 non-null float64
    Year                         2785 non-null float64
    FractionDate                 2785 non-null float64
    Actor1Code                   2550 non-null object
    Actor1Name                   2550 non-null object
    Actor1CountryCode            1573 non-null object
    Actor1KnownGroupCode         63 non-null object
    Actor1EthnicCode             31 non-null object
    Actor1Religion1Code          55 non-null object
    Actor1Religion2Code          13 non-null object
    Actor1Type1Code              1220 non-null object
    Actor1Type2Code              68 non-null object
    Actor1Type3Code              0 non-null float64
    Actor2Code                   2005 non-null object
    Actor2Name                   2005 non-null object
    Actor2CountryCode            1246 non-null object
    Actor2KnownGroupCode         40 non-null object
    Actor2EthnicCode             18 non-null object
    Actor2Religion1Code          43 non-null object
    Actor2Religion2Code          12 non-null object
    Actor2Type1Code              931 non-null object
    Actor2Type2Code              67 non-null object
    Actor2Type3Code              1 non-null object
    IsRootEvent                  2785 non-null float64
    EventCode                    2785 non-null float64
    EventBaseCode                2785 non-null float64
    EventRootCode                2785 non-null float64
    QuadClass                    2785 non-null float64
    GoldsteinScale               2785 non-null float64
    NumMentions                  2785 non-null float64
    NumSources                   2785 non-null float64
    NumArticles                  2785 non-null float64
    AvgTone                      2785 non-null float64
    Actor1Geo_Type               2785 non-null float64
    Actor1Geo_FullName           2502 non-null object
    Actor1Geo_CountryCode        2502 non-null object
    Actor1Geo_ADM1Code           2502 non-null object
    Actor1Geo_ADM2Code           1349 non-null object
    Actor1Geo_Lat                2502 non-null float64
    Actor1Geo_Long               2502 non-null float64
    Actor1Geo_FeatureID          2502 non-null object
    Actor2Geo_Type               2785 non-null float64
    Actor2Geo_FullName           1965 non-null object
    Actor2Geo_CountryCode        1965 non-null object
    Actor2Geo_ADM1Code           1965 non-null object
    Actor2Geo_ADM2Code           858 non-null object
    Actor2Geo_Lat                1965 non-null float64
    Actor2Geo_Long               1965 non-null float64
    Actor2Geo_FeatureID          1965 non-null object
    ActionGeo_Type               2785 non-null float64
    ActionGeo_FullName           2734 non-null object
    ActionGeo_CountryCode        2734 non-null object
    ActionGeo_ADM1Code           2734 non-null object
    ActionGeo_ADM2Code           1207 non-null object
    ActionGeo_Lat                2734 non-null float64
    ActionGeo_Long               2734 non-null float64
    ActionGeo_FeatureID          2734 non-null object
    DATEADDED                    2785 non-null float64
    SOURCEURL                    2785 non-null object
    EventTimeDate                11767 non-null int64
    MentionTimeDate              11767 non-null int64
    MentionType                  11767 non-null int64
    MentionSourceName            11767 non-null object
    MentionIdentifier            11767 non-null object
    SentenceID                   11767 non-null int64
    Actor1CharOffset             11767 non-null int64
    Actor2CharOffset             11767 non-null int64
    ActionCharOffset             11767 non-null int64
    InRawText                    11767 non-null int64
    Confidence                   11767 non-null int64
    MentionDocLen                11767 non-null int64
    MentionDocTone               11767 non-null float64
    MentionDocTranslationInfo    0 non-null float64
    Extras                       0 non-null float64
    dtypes: float64(29), int64(10), object(37)
    memory usage: 6.9+ MB



```python
combined.tail()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GLOBALEVENTID</th>
      <th>SQLDATE</th>
      <th>MonthYear</th>
      <th>Year</th>
      <th>FractionDate</th>
      <th>Actor1Code</th>
      <th>Actor1Name</th>
      <th>Actor1CountryCode</th>
      <th>Actor1KnownGroupCode</th>
      <th>Actor1EthnicCode</th>
      <th>...</th>
      <th>SentenceID</th>
      <th>Actor1CharOffset</th>
      <th>Actor2CharOffset</th>
      <th>ActionCharOffset</th>
      <th>InRawText</th>
      <th>Confidence</th>
      <th>MentionDocLen</th>
      <th>MentionDocTone</th>
      <th>MentionDocTranslationInfo</th>
      <th>Extras</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>11762</th>
      <td>581379923.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>879</td>
      <td>929</td>
      <td>901</td>
      <td>1</td>
      <td>100</td>
      <td>1547</td>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11763</th>
      <td>581387463.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>499</td>
      <td>477</td>
      <td>521</td>
      <td>1</td>
      <td>100</td>
      <td>1547</td>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11764</th>
      <td>581408219.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>687</td>
      <td>630</td>
      <td>665</td>
      <td>1</td>
      <td>20</td>
      <td>813</td>
      <td>-9.929078</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11765</th>
      <td>581408220.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>704</td>
      <td>617</td>
      <td>682</td>
      <td>0</td>
      <td>20</td>
      <td>813</td>
      <td>-9.929078</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11766</th>
      <td>581408221.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>683</td>
      <td>596</td>
      <td>661</td>
      <td>0</td>
      <td>20</td>
      <td>813</td>
      <td>-9.929078</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 76 columns</p>
</div>




```python
# combined.[(combined.Confidence != None) & (combined.MonthYear != None)]
combined.fillna('')[combined.GoldsteinScale <= -5.2]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GLOBALEVENTID</th>
      <th>SQLDATE</th>
      <th>MonthYear</th>
      <th>Year</th>
      <th>FractionDate</th>
      <th>Actor1Code</th>
      <th>Actor1Name</th>
      <th>Actor1CountryCode</th>
      <th>Actor1KnownGroupCode</th>
      <th>Actor1EthnicCode</th>
      <th>...</th>
      <th>SentenceID</th>
      <th>Actor1CharOffset</th>
      <th>Actor2CharOffset</th>
      <th>ActionCharOffset</th>
      <th>InRawText</th>
      <th>Confidence</th>
      <th>MentionDocLen</th>
      <th>MentionDocTone</th>
      <th>MentionDocTranslationInfo</th>
      <th>Extras</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>36</th>
      <td>581409211.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7</td>
      <td>LBNGOV</td>
      <td>TYRE</td>
      <td>LBN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1600</td>
      <td>1641</td>
      <td>1661</td>
      <td>0</td>
      <td>10</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>37</th>
      <td>581409212.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7</td>
      <td>LBNGOV</td>
      <td>TYRE</td>
      <td>LBN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1600</td>
      <td>1636</td>
      <td>1647</td>
      <td>1</td>
      <td>30</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>46</th>
      <td>581409221.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1600</td>
      <td>-1</td>
      <td>1694</td>
      <td>0</td>
      <td>10</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>55</th>
      <td>581409230.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.71</td>
      <td>LBN</td>
      <td>TYRE</td>
      <td>LBN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>842</td>
      <td>791</td>
      <td>829</td>
      <td>1</td>
      <td>60</td>
      <td>2749</td>
      <td>-7.922912</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>56</th>
      <td>581409231.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.71</td>
      <td>LBN</td>
      <td>TYRE</td>
      <td>LBN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>842</td>
      <td>854</td>
      <td>829</td>
      <td>0</td>
      <td>40</td>
      <td>2749</td>
      <td>-7.922912</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>67</th>
      <td>581409242.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.71</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>192</td>
      <td>499</td>
      <td>342</td>
      <td>0</td>
      <td>20</td>
      <td>1777</td>
      <td>-9.003215</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>81</th>
      <td>581409255.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>-1</td>
      <td>1943</td>
      <td>2012</td>
      <td>1</td>
      <td>100</td>
      <td>2229</td>
      <td>-3.140097</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>111</th>
      <td>581409284.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>29</td>
      <td>39</td>
      <td>1</td>
      <td>50</td>
      <td>3242</td>
      <td>-4.504505</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>137</th>
      <td>581409305.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>-1</td>
      <td>3980</td>
      <td>4010</td>
      <td>0</td>
      <td>20</td>
      <td>7521</td>
      <td>-0.867508</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>138</th>
      <td>581409305.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>9</td>
      <td>-1</td>
      <td>3719</td>
      <td>3741</td>
      <td>1</td>
      <td>100</td>
      <td>6763</td>
      <td>-1.218451</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>151</th>
      <td>581409318.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>-1</td>
      <td>1192</td>
      <td>1236</td>
      <td>1</td>
      <td>30</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>152</th>
      <td>581409319.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>126</td>
      <td>192</td>
      <td>1</td>
      <td>10</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>159</th>
      <td>581409326.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>59</td>
      <td>8</td>
      <td>1</td>
      <td>30</td>
      <td>2405</td>
      <td>-1.913876</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>160</th>
      <td>581409327.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>59</td>
      <td>8</td>
      <td>0</td>
      <td>20</td>
      <td>2405</td>
      <td>-1.913876</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>206</th>
      <td>581409366.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>-1</td>
      <td>471</td>
      <td>550</td>
      <td>0</td>
      <td>30</td>
      <td>2685</td>
      <td>-6.060606</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>207</th>
      <td>581409367.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>-1</td>
      <td>471</td>
      <td>566</td>
      <td>1</td>
      <td>60</td>
      <td>2685</td>
      <td>-6.060606</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>231</th>
      <td>581409386.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>-1</td>
      <td>388</td>
      <td>369</td>
      <td>1</td>
      <td>100</td>
      <td>3571</td>
      <td>-6.260297</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>232</th>
      <td>581409387.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>-1</td>
      <td>388</td>
      <td>403</td>
      <td>1</td>
      <td>100</td>
      <td>3571</td>
      <td>-6.260297</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>234</th>
      <td>581409389.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>-1</td>
      <td>1819</td>
      <td>1805</td>
      <td>1</td>
      <td>100</td>
      <td>2947</td>
      <td>6.108202</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>279</th>
      <td>581409427.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>-1</td>
      <td>567</td>
      <td>391</td>
      <td>1</td>
      <td>30</td>
      <td>5801</td>
      <td>-2.300110</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>281</th>
      <td>581409429.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>-1</td>
      <td>1547</td>
      <td>1596</td>
      <td>1</td>
      <td>100</td>
      <td>3722</td>
      <td>-1.712329</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>282</th>
      <td>581409430.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>401</td>
      <td>419</td>
      <td>0</td>
      <td>40</td>
      <td>1270</td>
      <td>-11.872146</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>283</th>
      <td>581409431.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>77</td>
      <td>256</td>
      <td>0</td>
      <td>60</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>284</th>
      <td>581409432.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>28</td>
      <td>-1</td>
      <td>7204</td>
      <td>7222</td>
      <td>0</td>
      <td>30</td>
      <td>7190</td>
      <td>-6.610169</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>285</th>
      <td>581409433.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>27</td>
      <td>-1</td>
      <td>10011</td>
      <td>10165</td>
      <td>0</td>
      <td>10</td>
      <td>11927</td>
      <td>1.317790</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>290</th>
      <td>581409438.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>-1</td>
      <td>128</td>
      <td>240</td>
      <td>1</td>
      <td>30</td>
      <td>10235</td>
      <td>-2.095460</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>291</th>
      <td>581409439.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>178</td>
      <td>256</td>
      <td>0</td>
      <td>20</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>297</th>
      <td>581409445.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>-1</td>
      <td>2749</td>
      <td>2763</td>
      <td>0</td>
      <td>30</td>
      <td>5372</td>
      <td>-4.966887</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>299</th>
      <td>581409447.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>-1</td>
      <td>1159</td>
      <td>1172</td>
      <td>0</td>
      <td>30</td>
      <td>1435</td>
      <td>-8.433735</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>365</th>
      <td>581409500.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>AUS</td>
      <td>AUSTRALIA</td>
      <td>AUS</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>240</td>
      <td>350</td>
      <td>306</td>
      <td>0</td>
      <td>40</td>
      <td>2152</td>
      <td>-0.787402</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>392</th>
      <td>581409524.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BRA</td>
      <td>BRAZIL</td>
      <td>BRA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2231</td>
      <td>2208</td>
      <td>2322</td>
      <td>1</td>
      <td>50</td>
      <td>3140</td>
      <td>-7.952286</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>448</th>
      <td>581409576.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>BANK</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>20</td>
      <td>6936</td>
      <td>-1</td>
      <td>6980</td>
      <td>1</td>
      <td>60</td>
      <td>12032</td>
      <td>-2.600996</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>449</th>
      <td>581409577.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>BANK</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>20</td>
      <td>6936</td>
      <td>-1</td>
      <td>6980</td>
      <td>0</td>
      <td>40</td>
      <td>12032</td>
      <td>-2.600996</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>452</th>
      <td>581409580.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>COMPANIES</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>992</td>
      <td>-1</td>
      <td>1032</td>
      <td>1</td>
      <td>100</td>
      <td>3203</td>
      <td>-1.792829</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>458</th>
      <td>581409586.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>AIRLINE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>68</td>
      <td>106</td>
      <td>87</td>
      <td>1</td>
      <td>100</td>
      <td>2967</td>
      <td>0.795229</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>478</th>
      <td>581409602.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>COMPANIES</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2823</td>
      <td>2694</td>
      <td>2833</td>
      <td>1</td>
      <td>80</td>
      <td>3191</td>
      <td>-2.994012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>505</th>
      <td>581409628.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>COMPANIES</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2843</td>
      <td>2700</td>
      <td>2847</td>
      <td>0</td>
      <td>20</td>
      <td>3191</td>
      <td>-2.994012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>524</th>
      <td>581409645.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2103</td>
      <td>-1</td>
      <td>2139</td>
      <td>1</td>
      <td>100</td>
      <td>3290</td>
      <td>-4.419890</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>525</th>
      <td>581409646.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2094</td>
      <td>-1</td>
      <td>2130</td>
      <td>0</td>
      <td>10</td>
      <td>3290</td>
      <td>-4.419890</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>526</th>
      <td>581409647.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>2653</td>
      <td>2677</td>
      <td>2660</td>
      <td>0</td>
      <td>40</td>
      <td>6742</td>
      <td>1.115880</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>527</th>
      <td>581409648.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>2552</td>
      <td>2576</td>
      <td>2559</td>
      <td>0</td>
      <td>20</td>
      <td>5668</td>
      <td>1.368421</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>529</th>
      <td>581409650.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1773</td>
      <td>1815</td>
      <td>1866</td>
      <td>0</td>
      <td>40</td>
      <td>2452</td>
      <td>6.913580</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>537</th>
      <td>581409658.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>2425</td>
      <td>2460</td>
      <td>2432</td>
      <td>0</td>
      <td>20</td>
      <td>5329</td>
      <td>1.325178</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>539</th>
      <td>581409660.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>14</td>
      <td>2975</td>
      <td>2987</td>
      <td>2982</td>
      <td>0</td>
      <td>10</td>
      <td>5372</td>
      <td>-4.966887</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>540</th>
      <td>581409661.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>14</td>
      <td>2993</td>
      <td>3021</td>
      <td>3000</td>
      <td>0</td>
      <td>10</td>
      <td>5372</td>
      <td>-4.966887</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>554</th>
      <td>581409675.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CHN</td>
      <td>CHINA</td>
      <td>CHN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>522</td>
      <td>546</td>
      <td>528</td>
      <td>1</td>
      <td>80</td>
      <td>686</td>
      <td>3.252033</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>555</th>
      <td>581409676.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CHN</td>
      <td>CHINA</td>
      <td>CHN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>522</td>
      <td>546</td>
      <td>528</td>
      <td>0</td>
      <td>20</td>
      <td>686</td>
      <td>3.252033</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>572</th>
      <td>581409693.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CHRCTH</td>
      <td>CATHOLIC</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>759</td>
      <td>-1</td>
      <td>798</td>
      <td>0</td>
      <td>10</td>
      <td>6114</td>
      <td>-4.872881</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>573</th>
      <td>581409694.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CHRCTH</td>
      <td>CATHOLIC</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>759</td>
      <td>-1</td>
      <td>798</td>
      <td>0</td>
      <td>10</td>
      <td>6114</td>
      <td>-4.872881</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>584</th>
      <td>581409703.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COG</td>
      <td>CONGO</td>
      <td>COG</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>-1</td>
      <td>17</td>
      <td>1</td>
      <td>100</td>
      <td>2567</td>
      <td>-14.492754</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>585</th>
      <td>581409703.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COG</td>
      <td>CONGO</td>
      <td>COG</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>-1</td>
      <td>17</td>
      <td>1</td>
      <td>100</td>
      <td>2672</td>
      <td>-14.251208</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>608</th>
      <td>581409723.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2631</td>
      <td>-1</td>
      <td>2591</td>
      <td>1</td>
      <td>20</td>
      <td>5249</td>
      <td>-7.407407</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>609</th>
      <td>581409724.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1823</td>
      <td>-1</td>
      <td>1877</td>
      <td>1</td>
      <td>60</td>
      <td>2452</td>
      <td>6.913580</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>610</th>
      <td>581409725.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>342</td>
      <td>-1</td>
      <td>424</td>
      <td>1</td>
      <td>100</td>
      <td>2710</td>
      <td>-3.794643</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>615</th>
      <td>581409730.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>SECURITY FORCE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>15</td>
      <td>4507</td>
      <td>-1</td>
      <td>4523</td>
      <td>1</td>
      <td>100</td>
      <td>10652</td>
      <td>-4.256804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>616</th>
      <td>581409731.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>315</td>
      <td>-1</td>
      <td>363</td>
      <td>1</td>
      <td>100</td>
      <td>608</td>
      <td>-10.714286</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>617</th>
      <td>581409732.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>306</td>
      <td>-1</td>
      <td>315</td>
      <td>1</td>
      <td>100</td>
      <td>1806</td>
      <td>-3.594771</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>619</th>
      <td>581409734.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2358</td>
      <td>2378</td>
      <td>2365</td>
      <td>1</td>
      <td>100</td>
      <td>2964</td>
      <td>-3.821656</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>627</th>
      <td>581409742.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>304</td>
      <td>313</td>
      <td>322</td>
      <td>1</td>
      <td>50</td>
      <td>2710</td>
      <td>-3.794643</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>640</th>
      <td>581409753.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>159</td>
      <td>64</td>
      <td>80</td>
      <td>1</td>
      <td>50</td>
      <td>548</td>
      <td>-7.692308</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>641</th>
      <td>581409754.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>484</td>
      <td>442</td>
      <td>460</td>
      <td>1</td>
      <td>100</td>
      <td>2518</td>
      <td>-7.226107</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>647</th>
      <td>581409760.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>SECURITY FORCE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>14</td>
      <td>4403</td>
      <td>4388</td>
      <td>4340</td>
      <td>0</td>
      <td>10</td>
      <td>10652</td>
      <td>-4.256804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>649</th>
      <td>581409762.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>SECURITY FORCE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1235</td>
      <td>1089</td>
      <td>1216</td>
      <td>1</td>
      <td>50</td>
      <td>3736</td>
      <td>-0.860585</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>670</th>
      <td>581409780.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>-1</td>
      <td>-1</td>
      <td>0</td>
      <td>10</td>
      <td>1864</td>
      <td>-4.666667</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>671</th>
      <td>581409780.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1083</td>
      <td>980</td>
      <td>1070</td>
      <td>1</td>
      <td>100</td>
      <td>2730</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>672</th>
      <td>581409781.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>412</td>
      <td>367</td>
      <td>400</td>
      <td>0</td>
      <td>20</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>673</th>
      <td>581409782.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>181</td>
      <td>45</td>
      <td>162</td>
      <td>0</td>
      <td>20</td>
      <td>594</td>
      <td>-7.547170</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>674</th>
      <td>581409783.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>510</td>
      <td>440</td>
      <td>498</td>
      <td>0</td>
      <td>20</td>
      <td>3015</td>
      <td>-3.543307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>675</th>
      <td>581409784.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>531</td>
      <td>461</td>
      <td>519</td>
      <td>0</td>
      <td>20</td>
      <td>3015</td>
      <td>-3.543307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>676</th>
      <td>581409785.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2687</td>
      <td>2616</td>
      <td>2662</td>
      <td>1</td>
      <td>70</td>
      <td>9235</td>
      <td>-3.241491</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>677</th>
      <td>581409786.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>412</td>
      <td>367</td>
      <td>391</td>
      <td>0</td>
      <td>20</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>678</th>
      <td>581409787.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>143</td>
      <td>162</td>
      <td>150</td>
      <td>1</td>
      <td>100</td>
      <td>4250</td>
      <td>-4.526749</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>679</th>
      <td>581409788.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>-1</td>
      <td>2667</td>
      <td>2714</td>
      <td>0</td>
      <td>10</td>
      <td>9235</td>
      <td>-3.241491</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>681</th>
      <td>581409790.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>DEPUTY</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1217</td>
      <td>1182</td>
      <td>1195</td>
      <td>0</td>
      <td>10</td>
      <td>1435</td>
      <td>-8.433735</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>700</th>
      <td>581409809.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CRM</td>
      <td>CRIMINAL</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1787</td>
      <td>1960</td>
      <td>1928</td>
      <td>0</td>
      <td>10</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>744</th>
      <td>581409851.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CVL</td>
      <td>VILLAGE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2818</td>
      <td>-1</td>
      <td>2749</td>
      <td>1</td>
      <td>30</td>
      <td>3971</td>
      <td>-1.401051</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>745</th>
      <td>581409852.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CVL</td>
      <td>COMMUNITY</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>29</td>
      <td>-1</td>
      <td>39</td>
      <td>1</td>
      <td>50</td>
      <td>3242</td>
      <td>-4.504505</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>765</th>
      <td>581409872.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CVL</td>
      <td>NEIGHBORHOOD</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>418</td>
      <td>261</td>
      <td>349</td>
      <td>1</td>
      <td>100</td>
      <td>1155</td>
      <td>-7.619048</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>816</th>
      <td>581409920.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>SCHOOL</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2058</td>
      <td>-1</td>
      <td>2027</td>
      <td>1</td>
      <td>100</td>
      <td>3579</td>
      <td>-4.232804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>818</th>
      <td>581409922.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>8</td>
      <td>-1</td>
      <td>34</td>
      <td>1</td>
      <td>100</td>
      <td>883</td>
      <td>-3.311258</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>819</th>
      <td>581409923.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>59</td>
      <td>-1</td>
      <td>85</td>
      <td>1</td>
      <td>100</td>
      <td>883</td>
      <td>-3.311258</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>826</th>
      <td>581409930.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>UNIVERSITY</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>132</td>
      <td>236</td>
      <td>270</td>
      <td>1</td>
      <td>100</td>
      <td>3579</td>
      <td>-4.232804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>861</th>
      <td>581409965.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1062</td>
      <td>1132</td>
      <td>1071</td>
      <td>0</td>
      <td>20</td>
      <td>2744</td>
      <td>-4.291845</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>862</th>
      <td>581409966.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>700</td>
      <td>737</td>
      <td>709</td>
      <td>1</td>
      <td>100</td>
      <td>955</td>
      <td>-6.666667</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>863</th>
      <td>581409967.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>1877</td>
      <td>1937</td>
      <td>1886</td>
      <td>0</td>
      <td>20</td>
      <td>11363</td>
      <td>-6.850054</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>865</th>
      <td>581409969.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDUEDU</td>
      <td>SCHOOL</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>132</td>
      <td>277</td>
      <td>262</td>
      <td>1</td>
      <td>100</td>
      <td>883</td>
      <td>-3.311258</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>886</th>
      <td>581409983.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ESP</td>
      <td>BARCELONA</td>
      <td>ESP</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>86</td>
      <td>-1</td>
      <td>153</td>
      <td>1</td>
      <td>50</td>
      <td>3232</td>
      <td>-4.609929</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>887</th>
      <td>581409984.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ESP</td>
      <td>BARCELONA</td>
      <td>ESP</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>-1</td>
      <td>67</td>
      <td>1</td>
      <td>70</td>
      <td>3232</td>
      <td>-4.609929</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>974</th>
      <td>581410049.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GBR</td>
      <td>BRITAIN</td>
      <td>GBR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2293</td>
      <td>2430</td>
      <td>2504</td>
      <td>0</td>
      <td>20</td>
      <td>5595</td>
      <td>-6.992231</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1030</th>
      <td>581410104.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>FIREFIGHTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2208</td>
      <td>2231</td>
      <td>2322</td>
      <td>1</td>
      <td>50</td>
      <td>3140</td>
      <td>-7.952286</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1038</th>
      <td>581410112.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>KING</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>172</td>
      <td>97</td>
      <td>123</td>
      <td>1</td>
      <td>100</td>
      <td>331</td>
      <td>-4.761905</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1039</th>
      <td>581410113.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>GOVERNMENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>596</td>
      <td>654</td>
      <td>553</td>
      <td>1</td>
      <td>60</td>
      <td>1190</td>
      <td>-0.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1056</th>
      <td>581410130.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>PRIME MINISTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2860</td>
      <td>2926</td>
      <td>2931</td>
      <td>0</td>
      <td>20</td>
      <td>3843</td>
      <td>0.975610</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1057</th>
      <td>581410131.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>PRIME MINISTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2860</td>
      <td>2926</td>
      <td>2931</td>
      <td>1</td>
      <td>40</td>
      <td>3843</td>
      <td>0.975610</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1065</th>
      <td>581410138.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>DESPOT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>97</td>
      <td>221</td>
      <td>203</td>
      <td>1</td>
      <td>30</td>
      <td>5722</td>
      <td>-2.558854</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1066</th>
      <td>581410139.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>DESPOT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>97</td>
      <td>227</td>
      <td>209</td>
      <td>0</td>
      <td>20</td>
      <td>5722</td>
      <td>-2.558854</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1090</th>
      <td>581410163.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>GOVERNMENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>964</td>
      <td>931</td>
      <td>938</td>
      <td>0</td>
      <td>20</td>
      <td>1714</td>
      <td>-6.756757</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1098</th>
      <td>581410171.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>INTERIOR MINIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>817</td>
      <td>866</td>
      <td>835</td>
      <td>1</td>
      <td>100</td>
      <td>1192</td>
      <td>-8.490566</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1118</th>
      <td>581410188.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>MINIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>18</td>
      <td>3593</td>
      <td>3637</td>
      <td>3603</td>
      <td>1</td>
      <td>100</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1131</th>
      <td>581410200.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOVHLH</td>
      <td>HEALTH DEPARTMENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>126</td>
      <td>-1</td>
      <td>192</td>
      <td>1</td>
      <td>10</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2050</th>
      <td>581411023.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>SYRMIL</td>
      <td>SYRIA</td>
      <td>SYR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>1833</td>
      <td>1899</td>
      <td>1890</td>
      <td>0</td>
      <td>20</td>
      <td>3290</td>
      <td>-4.419890</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2057</th>
      <td>581411030.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUN</td>
      <td>TUNISIA</td>
      <td>TUN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>17</td>
      <td>-1</td>
      <td>5</td>
      <td>0</td>
      <td>20</td>
      <td>9566</td>
      <td>-4.032766</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2058</th>
      <td>581411031.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUN</td>
      <td>TUNISIA</td>
      <td>TUN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>17</td>
      <td>-1</td>
      <td>5</td>
      <td>1</td>
      <td>80</td>
      <td>9566</td>
      <td>-4.032766</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2059</th>
      <td>581411032.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUN</td>
      <td>TUNISIA</td>
      <td>TUN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>829</td>
      <td>934</td>
      <td>787</td>
      <td>1</td>
      <td>100</td>
      <td>9566</td>
      <td>-4.032766</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2061</th>
      <td>581411034.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>TURKISH</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>480</td>
      <td>396</td>
      <td>429</td>
      <td>0</td>
      <td>10</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2062</th>
      <td>581411035.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>ISTANBUL</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>19</td>
      <td>3036</td>
      <td>2983</td>
      <td>2996</td>
      <td>1</td>
      <td>80</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2063</th>
      <td>581411036.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>ISTANBUL</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>19</td>
      <td>3067</td>
      <td>3010</td>
      <td>3020</td>
      <td>0</td>
      <td>20</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2066</th>
      <td>581411039.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>TURKISH</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>1459</td>
      <td>1368</td>
      <td>1445</td>
      <td>0</td>
      <td>10</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2067</th>
      <td>581411040.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>TURKISH</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>1459</td>
      <td>1368</td>
      <td>1445</td>
      <td>0</td>
      <td>10</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2072</th>
      <td>581411045.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TURCOP</td>
      <td>TURKISH</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>1442</td>
      <td>1368</td>
      <td>1432</td>
      <td>1</td>
      <td>30</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2086</th>
      <td>581411059.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>15</td>
      <td>3663</td>
      <td>3687</td>
      <td>3673</td>
      <td>0</td>
      <td>20</td>
      <td>3943</td>
      <td>-5.376344</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2087</th>
      <td>581411060.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>MILITANT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>17</td>
      <td>4749</td>
      <td>4766</td>
      <td>4759</td>
      <td>1</td>
      <td>30</td>
      <td>10652</td>
      <td>-4.256804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2088</th>
      <td>581411061.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>FIGHTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1231</td>
      <td>1256</td>
      <td>1244</td>
      <td>1</td>
      <td>30</td>
      <td>4593</td>
      <td>-1.859230</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2089</th>
      <td>581411062.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1990</td>
      <td>2014</td>
      <td>2000</td>
      <td>1</td>
      <td>100</td>
      <td>2272</td>
      <td>2.298851</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2090</th>
      <td>581411063.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2166</td>
      <td>2190</td>
      <td>2176</td>
      <td>0</td>
      <td>20</td>
      <td>2413</td>
      <td>-4.116223</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2091</th>
      <td>581411064.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2166</td>
      <td>2190</td>
      <td>2176</td>
      <td>0</td>
      <td>20</td>
      <td>2413</td>
      <td>-4.116223</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2092</th>
      <td>581411065.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2166</td>
      <td>2190</td>
      <td>2176</td>
      <td>1</td>
      <td>60</td>
      <td>2413</td>
      <td>-4.116223</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2093</th>
      <td>581411066.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>FIGHTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>123</td>
      <td>163</td>
      <td>98</td>
      <td>0</td>
      <td>40</td>
      <td>4593</td>
      <td>-1.859230</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2094</th>
      <td>581411067.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>FIGHTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>123</td>
      <td>163</td>
      <td>98</td>
      <td>0</td>
      <td>40</td>
      <td>4593</td>
      <td>-1.859230</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2265</th>
      <td>581411221.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>160</td>
      <td>-1</td>
      <td>209</td>
      <td>0</td>
      <td>10</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2266</th>
      <td>581411222.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>179</td>
      <td>-1</td>
      <td>241</td>
      <td>0</td>
      <td>30</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2267</th>
      <td>581411223.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>OHIO</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>173</td>
      <td>-1</td>
      <td>197</td>
      <td>1</td>
      <td>10</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2268</th>
      <td>581411224.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>NEW YORK</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>3471</td>
      <td>-1</td>
      <td>3526</td>
      <td>0</td>
      <td>20</td>
      <td>9235</td>
      <td>-3.241491</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2269</th>
      <td>581411225.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>16</td>
      <td>3565</td>
      <td>-1</td>
      <td>3589</td>
      <td>0</td>
      <td>40</td>
      <td>4250</td>
      <td>-4.526749</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2270</th>
      <td>581411226.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>488</td>
      <td>-1</td>
      <td>502</td>
      <td>0</td>
      <td>40</td>
      <td>1481</td>
      <td>-12.015504</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2276</th>
      <td>581411232.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>95</td>
      <td>-1</td>
      <td>191</td>
      <td>0</td>
      <td>20</td>
      <td>2633</td>
      <td>-5.870445</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2277</th>
      <td>581411233.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>21</td>
      <td>5828</td>
      <td>-1</td>
      <td>5846</td>
      <td>0</td>
      <td>20</td>
      <td>6627</td>
      <td>-8.340728</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2278</th>
      <td>581411234.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>339</td>
      <td>-1</td>
      <td>427</td>
      <td>0</td>
      <td>40</td>
      <td>1481</td>
      <td>-12.015504</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2279</th>
      <td>581411235.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>68</td>
      <td>-1</td>
      <td>140</td>
      <td>0</td>
      <td>40</td>
      <td>1116</td>
      <td>-13.440860</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2280</th>
      <td>581411236.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>61</td>
      <td>-1</td>
      <td>206</td>
      <td>0</td>
      <td>40</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2281</th>
      <td>581411237.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>77</td>
      <td>-1</td>
      <td>256</td>
      <td>0</td>
      <td>10</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2282</th>
      <td>581411238.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>77</td>
      <td>-1</td>
      <td>256</td>
      <td>0</td>
      <td>10</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2283</th>
      <td>581411239.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>27</td>
      <td>10011</td>
      <td>-1</td>
      <td>10165</td>
      <td>0</td>
      <td>10</td>
      <td>11927</td>
      <td>1.317790</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2284</th>
      <td>581411240.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>452</td>
      <td>-1</td>
      <td>466</td>
      <td>0</td>
      <td>20</td>
      <td>2053</td>
      <td>-8.955224</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2285</th>
      <td>581411241.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>AMERICAN</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>75</td>
      <td>-1</td>
      <td>21</td>
      <td>1</td>
      <td>100</td>
      <td>483</td>
      <td>0.000000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2288</th>
      <td>581411244.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>9</td>
      <td>2554</td>
      <td>2785</td>
      <td>2596</td>
      <td>0</td>
      <td>10</td>
      <td>5570</td>
      <td>-4.596413</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2289</th>
      <td>581411245.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>9</td>
      <td>2533</td>
      <td>2764</td>
      <td>2575</td>
      <td>0</td>
      <td>10</td>
      <td>5570</td>
      <td>-4.596413</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2350</th>
      <td>581411297.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ARKANSAS</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>586</td>
      <td>646</td>
      <td>653</td>
      <td>1</td>
      <td>100</td>
      <td>1687</td>
      <td>-4.332130</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2351</th>
      <td>581411298.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>440</td>
      <td>510</td>
      <td>498</td>
      <td>0</td>
      <td>20</td>
      <td>3015</td>
      <td>-3.543307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2352</th>
      <td>581411299.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>461</td>
      <td>531</td>
      <td>519</td>
      <td>0</td>
      <td>20</td>
      <td>3015</td>
      <td>-3.543307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2353</th>
      <td>581411300.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1799</td>
      <td>1899</td>
      <td>1891</td>
      <td>0</td>
      <td>10</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2359</th>
      <td>581411306.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1976</td>
      <td>2065</td>
      <td>1992</td>
      <td>0</td>
      <td>20</td>
      <td>3323</td>
      <td>1.711027</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2364</th>
      <td>581411311.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1055</td>
      <td>-1</td>
      <td>1162</td>
      <td>0</td>
      <td>20</td>
      <td>1368</td>
      <td>-0.429185</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2365</th>
      <td>581411312.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1070</td>
      <td>-1</td>
      <td>1177</td>
      <td>0</td>
      <td>20</td>
      <td>1368</td>
      <td>-0.429185</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2366</th>
      <td>581411313.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>TEXAS</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1097</td>
      <td>1208</td>
      <td>1115</td>
      <td>1</td>
      <td>60</td>
      <td>1368</td>
      <td>-0.429185</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2381</th>
      <td>581411325.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ORLANDO</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2358</td>
      <td>2426</td>
      <td>2405</td>
      <td>0</td>
      <td>20</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2382</th>
      <td>581411326.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ORLANDO</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2301</td>
      <td>2368</td>
      <td>2349</td>
      <td>1</td>
      <td>60</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2383</th>
      <td>581411327.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ORLANDO</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2343</td>
      <td>2411</td>
      <td>2390</td>
      <td>0</td>
      <td>20</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2384</th>
      <td>581411328.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>NEW YORK</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2220</td>
      <td>2368</td>
      <td>2337</td>
      <td>1</td>
      <td>80</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2385</th>
      <td>581411329.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2195</td>
      <td>2411</td>
      <td>2381</td>
      <td>0</td>
      <td>20</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2386</th>
      <td>581411330.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2210</td>
      <td>2426</td>
      <td>2303</td>
      <td>0</td>
      <td>20</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2387</th>
      <td>581411331.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>NEW YORK</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2220</td>
      <td>2368</td>
      <td>2244</td>
      <td>1</td>
      <td>80</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2408</th>
      <td>581411352.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>351</td>
      <td>256</td>
      <td>290</td>
      <td>0</td>
      <td>60</td>
      <td>3895</td>
      <td>-6.707317</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2411</th>
      <td>581411355.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1282</td>
      <td>1342</td>
      <td>1369</td>
      <td>0</td>
      <td>20</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2412</th>
      <td>581411356.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>15</td>
      <td>5104</td>
      <td>5164</td>
      <td>5191</td>
      <td>0</td>
      <td>40</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2413</th>
      <td>581411357.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1261</td>
      <td>1321</td>
      <td>1348</td>
      <td>0</td>
      <td>20</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2415</th>
      <td>581411359.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>4497</td>
      <td>4528</td>
      <td>4573</td>
      <td>0</td>
      <td>40</td>
      <td>9461</td>
      <td>2.437538</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2436</th>
      <td>581411380.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>TEXAS</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>19</td>
      <td>4715</td>
      <td>4569</td>
      <td>4658</td>
      <td>0</td>
      <td>20</td>
      <td>5327</td>
      <td>-6.064073</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2475</th>
      <td>581411415.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>16</td>
      <td>6331</td>
      <td>6483</td>
      <td>6345</td>
      <td>0</td>
      <td>10</td>
      <td>11927</td>
      <td>1.317790</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2476</th>
      <td>581411416.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>16</td>
      <td>6316</td>
      <td>6468</td>
      <td>6330</td>
      <td>0</td>
      <td>10</td>
      <td>11927</td>
      <td>1.317790</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2508</th>
      <td>581411441.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ARIZONA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>82</td>
      <td>329</td>
      <td>259</td>
      <td>1</td>
      <td>60</td>
      <td>1269</td>
      <td>-7.359307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2509</th>
      <td>581411442.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ARIZONA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>82</td>
      <td>368</td>
      <td>300</td>
      <td>0</td>
      <td>40</td>
      <td>1269</td>
      <td>-7.359307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2514</th>
      <td>581411447.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>KANSAS CITY</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>5</td>
      <td>185</td>
      <td>139</td>
      <td>1</td>
      <td>100</td>
      <td>2619</td>
      <td>-1.869159</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2536</th>
      <td>581411461.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>20</td>
      <td>4118</td>
      <td>3970</td>
      <td>4134</td>
      <td>0</td>
      <td>10</td>
      <td>7468</td>
      <td>-2.489960</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2589</th>
      <td>581411513.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>NEW YORK</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>3071</td>
      <td>3173</td>
      <td>3058</td>
      <td>1</td>
      <td>30</td>
      <td>9235</td>
      <td>-3.241491</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2590</th>
      <td>581411514.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>115</td>
      <td>129</td>
      <td>242</td>
      <td>0</td>
      <td>20</td>
      <td>10235</td>
      <td>-2.095460</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2605</th>
      <td>581411527.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ATLANTA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>8</td>
      <td>2091</td>
      <td>2071</td>
      <td>2048</td>
      <td>0</td>
      <td>20</td>
      <td>2168</td>
      <td>-5.817175</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2615</th>
      <td>581411537.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2619</td>
      <td>-1</td>
      <td>2591</td>
      <td>0</td>
      <td>40</td>
      <td>5249</td>
      <td>-7.407407</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2616</th>
      <td>581411538.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>PHILADELPHIA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>79</td>
      <td>-1</td>
      <td>99</td>
      <td>1</td>
      <td>80</td>
      <td>3247</td>
      <td>-8.436214</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2617</th>
      <td>581411539.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>105</td>
      <td>295</td>
      <td>223</td>
      <td>0</td>
      <td>20</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2618</th>
      <td>581411540.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>105</td>
      <td>247</td>
      <td>181</td>
      <td>1</td>
      <td>60</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2619</th>
      <td>581411541.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>105</td>
      <td>295</td>
      <td>223</td>
      <td>0</td>
      <td>20</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2620</th>
      <td>581411542.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>105</td>
      <td>247</td>
      <td>232</td>
      <td>1</td>
      <td>100</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2622</th>
      <td>581411544.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2639</td>
      <td>2705</td>
      <td>2591</td>
      <td>0</td>
      <td>20</td>
      <td>5249</td>
      <td>-7.407407</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2623</th>
      <td>581411545.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2639</td>
      <td>2687</td>
      <td>2591</td>
      <td>0</td>
      <td>20</td>
      <td>5249</td>
      <td>-7.407407</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2634</th>
      <td>581411556.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAEDU</td>
      <td>MARYLAND</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>620</td>
      <td>-1</td>
      <td>534</td>
      <td>1</td>
      <td>50</td>
      <td>4949</td>
      <td>1.210654</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2639</th>
      <td>581411561.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAEDU</td>
      <td>CALIFORNIA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1283</td>
      <td>1302</td>
      <td>1330</td>
      <td>1</td>
      <td>60</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2640</th>
      <td>581411562.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAEDU</td>
      <td>CALIFORNIA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>15</td>
      <td>5126</td>
      <td>5145</td>
      <td>5173</td>
      <td>1</td>
      <td>60</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2662</th>
      <td>581411584.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>NASA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>215</td>
      <td>-1</td>
      <td>64</td>
      <td>1</td>
      <td>50</td>
      <td>2110</td>
      <td>-1.162791</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2663</th>
      <td>581411585.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>128</td>
      <td>-1</td>
      <td>240</td>
      <td>1</td>
      <td>30</td>
      <td>10235</td>
      <td>-2.095460</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2664</th>
      <td>581411586.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>209</td>
      <td>-1</td>
      <td>190</td>
      <td>1</td>
      <td>100</td>
      <td>532</td>
      <td>-1.754386</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2669</th>
      <td>581411591.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>46</td>
      <td>191</td>
      <td>82</td>
      <td>1</td>
      <td>30</td>
      <td>11363</td>
      <td>-6.850054</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2670</th>
      <td>581411592.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>46</td>
      <td>191</td>
      <td>82</td>
      <td>0</td>
      <td>10</td>
      <td>11363</td>
      <td>-6.850054</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2671</th>
      <td>581411593.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>46</td>
      <td>191</td>
      <td>82</td>
      <td>0</td>
      <td>10</td>
      <td>11363</td>
      <td>-6.850054</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2683</th>
      <td>581411605.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>8</td>
      <td>1758</td>
      <td>1799</td>
      <td>1768</td>
      <td>1</td>
      <td>100</td>
      <td>6609</td>
      <td>-1.092896</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2684</th>
      <td>581411606.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>22</td>
      <td>5499</td>
      <td>5557</td>
      <td>5545</td>
      <td>0</td>
      <td>20</td>
      <td>18076</td>
      <td>-4.946012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2685</th>
      <td>581411606.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>22</td>
      <td>5499</td>
      <td>5557</td>
      <td>5545</td>
      <td>0</td>
      <td>20</td>
      <td>18076</td>
      <td>-4.946012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2686</th>
      <td>581411607.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>22</td>
      <td>5499</td>
      <td>5557</td>
      <td>5545</td>
      <td>1</td>
      <td>80</td>
      <td>18076</td>
      <td>-4.946012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2687</th>
      <td>581411607.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>22</td>
      <td>5499</td>
      <td>5557</td>
      <td>5545</td>
      <td>1</td>
      <td>80</td>
      <td>18076</td>
      <td>-4.946012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2699</th>
      <td>581411618.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2583</td>
      <td>2672</td>
      <td>2629</td>
      <td>0</td>
      <td>20</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2700</th>
      <td>581411619.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2583</td>
      <td>2672</td>
      <td>2629</td>
      <td>1</td>
      <td>60</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2701</th>
      <td>581411620.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2583</td>
      <td>2672</td>
      <td>2629</td>
      <td>0</td>
      <td>20</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2706</th>
      <td>581411625.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOVHLH</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>178</td>
      <td>-1</td>
      <td>256</td>
      <td>0</td>
      <td>20</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2711</th>
      <td>581411629.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAJUD</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2682</td>
      <td>-1</td>
      <td>2811</td>
      <td>0</td>
      <td>20</td>
      <td>3247</td>
      <td>-8.436214</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2740</th>
      <td>581411653.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAPTY</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>24</td>
      <td>5224</td>
      <td>5339</td>
      <td>5291</td>
      <td>0</td>
      <td>10</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2751</th>
      <td>581411664.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1510</td>
      <td>-1</td>
      <td>1495</td>
      <td>1</td>
      <td>80</td>
      <td>5442</td>
      <td>-4.434590</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2752</th>
      <td>581411665.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1510</td>
      <td>-1</td>
      <td>1495</td>
      <td>0</td>
      <td>20</td>
      <td>5442</td>
      <td>-4.434590</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2753</th>
      <td>581411666.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>9</td>
      <td>2875</td>
      <td>2927</td>
      <td>2922</td>
      <td>0</td>
      <td>40</td>
      <td>3994</td>
      <td>-3.698225</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2755</th>
      <td>581411668.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>bte</td>
      <td>BETI</td>
      <td></td>
      <td></td>
      <td>bte</td>
      <td>...</td>
      <td>8</td>
      <td>2303</td>
      <td>-1</td>
      <td>2422</td>
      <td>0</td>
      <td>20</td>
      <td>3971</td>
      <td>-1.401051</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2756</th>
      <td>581411669.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>bte</td>
      <td>BETI</td>
      <td></td>
      <td></td>
      <td>bte</td>
      <td>...</td>
      <td>8</td>
      <td>2303</td>
      <td>-1</td>
      <td>2433</td>
      <td>0</td>
      <td>20</td>
      <td>3971</td>
      <td>-1.401051</td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>308 rows × 76 columns</p>
</div>



# Early Pipeline to Write out R Dataframe


Ways to install
```python
pip install feather-format
```

```bash
conda install feather-format -c conda-forge
```


###  **IT WORKS!!!**


```python

```


```python
import feather
path = 'my_data.feather'
feather.api.write_dataframe(testdf, path)
newtestdf = feather.api.read_dataframe(path)
```

# Leftovers; Junkyard below here


```python
results = masterListdf[masterListdf[2].str.contains(gdelt_timeString(dateInputCheck(date)))==True]
```


```python
results[2].reset_index().ix[0][2]
```


```python
results[results[2].str.contains('gkg')]
```


```python
gdelt_timeString(dateInputCheck(date))
```


```python
import re
from dateutil.parser import parse
re.search('(([\d]{4,}).*)',clean[20][-1]).group()
```


```python
if bool(4>3):
    print "Hello"
```


```python
(datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)) == parse("2016 09 18" )
```


```python
b = dateutil.parser.parse(re.search('([\d]{4,})',clean[20][-1]).group())
```


```python
matchDate = re.search('([\d]{4,})',clean[20][-1]).group()
```


```python
def time_change(current,diff):
    date = current.replace(minute=0, second=0) + timedelta(minutes=diff)
    return date.strftime("%Y%m%d%H%M%S")
    
```


```python
# pulling most current daily report

import numpy as np
import datetime
from datetime import timedelta

currentTime = datetime.datetime.now()
timeDiff = currentTime.minute / 15 

query = np.where(timeDiff == 1,time_change(currentTime,diff=15),
        np.where(timeDiff == 2, time_change(currentTime,diff=30),
                 np.where(timeDiff == 3, time_change(currentTime,diff=45),
                          time_change(currentTime,diff=0))))

baseUrl = 'http://data.gdeltproject.org/gdeltv2/' + str(query) + '.export.CSV.zip'
```


```python
data
```


```python
myzipfile.namelist()
```


```python

import zipfile


r = requests.get(baseUrl, stream=True)

# with open('gdelt.zip', 'wb') as f:
#     f.write(r.content)
# fh = open('gdelt.zip')
# g = zipfile.ZipFile(fh)
# g.extractall()

from StringIO import StringIO
zipdata = StringIO()
zipdata.write(r.content)
myzipfile = zipfile.ZipFile(zipdata,'r')
data = myzipfile.read(str(query) + '.export.CSV')
gdeltdf = pd.read_csv(StringIO(data),delimiter='\t',header=None)

```


```python
gdeltdf.columns=headers.tableId.tolist()
```


```python
gdeltdf.SOURCEURL[((gdeltdf.ActionGeo_CountryCode =='SY')|(gdeltdf.ActionGeo_CountryCode =='IZ')) & (gdeltdf.GoldsteinScale < -4)]
```


```python
text = '''
GLOBALEVENTID	INTEGER	NULLABLE	This is the ID of the event that was mentioned in the article.
EventTimeDate	INTEGER	NULLABLE	This is the 15-minute timestamp (YYYYMMDDHHMMSS) when the event being mentioned was first recorded by GDELT (the DATEADDED field of the original event record).  This field can be compared against the next one to identify events being mentioned for the first time (their first mentions) or to identify events of a particular vintage being mentioned now (such as filtering for mentions of events at least one week old).
MentionTimeDate	INTEGER	NULLABLE	This is the 15-minute timestamp (YYYYMMDDHHMMSS) of the current update.  This is identical for all entries in the update file but is included to make it easier to load the Mentions table into a database.
MentionType	INTEGER	NULLABLE	This is a numeric identifier that refers to the source collection the document came from and is used to interpret the MentionIdentifier in the next column.  In essence, it specifies how to interpret the MentionIdentifier to locate the actual document.  At present, it can hold one of the following values:o 1 = WEB (The document originates from the open web and the MentionIdentifier is a fully-qualified URL that can be used to access the document on the web).o 2 = CITATIONONLY (The document originates from a broadcast, print, or other offline source in which only a textual citation is available for the document.  In this case the MentionIdentifier contains the textual citation for the document).o 3 = CORE (The document originates from the CORE archive and the MentionIdentifier contains its DOI, suitable for accessing the original document through the CORE website).o 4 = DTIC (The document originates from the DTIC archive and the MentionIdentifier contains its DOI, suitable for accessing the original document through the DTIC website).o 5 = JSTOR (The document originates from the JSTOR archive and the MentionIdentifier contains its DOI, suitable for accessing the original document through your JSTOR subscription if your institution subscribes to it).o 6 = NONTEXTUALSOURCE (The document originates from a textual proxy (such as closed captioning) of a non-textual information source (such as a video) available via a URL and the MentionIdentifier provides the URL of the non-textual original source.  At present, this Collection Identifier is used for processing of the closed captioning streams of the Internet Archive Television News Archive in which each broadcast is available via a URL, but the URL offers access only to the video of the broadcast and does not provide any access to the textual closed captioning used to generate the metadata.  This code is used in order to draw a distinction between URL-based textual material (Collection Identifier 1 (WEB) and URL-based non-textual material like the Television News Archive).
MentionSourceName	STRING	NULLABLE	This is a human-friendly identifier of the source of the document.  For material originating from the open web with a URL this field will contain the top-level domain the page was from.  For BBC Monitoring material it will contain “BBC Monitoring” and for JSTOR material it will contain “JSTOR.”  This field is intended for human display of major sources as well as for network analysis of information flows by source, obviating the requirement to perform domain or other parsing of the MentionIdentifier field.
MentionIdentifier	STRING	NULLABLE	This is the unique external identifier for the source document.  It can be used to uniquely identify the document and access it if you have the necessary subscriptions or authorizations and/or the document is public access.  This field can contain a range of values, from URLs of open web resources to textual citations of print or broadcast material to DOI identifiers for various document repositories.  For example, if MentionType is equal to 1, this field will contain a fully-qualified URL suitable for direct access.  If MentionType is equal to 2, this field will contain a textual citation akin to what would appear in an academic journal article referencing that document (NOTE that the actual citation format will vary (usually between APA, Chicago, Harvard, or MLA) depending on a number of factors and no assumptions should be made on its precise format at this time due to the way in which this data is currently provided to GDELT – future efforts will focus on normalization of this field to a standard citation format).  If MentionType is 3, the field will contain a numeric or alpha-numeric DOI that can be typed into JSTOR’s search engine to access the document if your institution has a JSTOR subscription.
SentenceID	INTEGER	NULLABLE	The sentence within the article where the event was mentioned (starting with the first sentence as 1, the second sentence as 2, the third sentence as 3, and so on).  This can be used similarly to the CharOffset fields below, but reports the event’s location in the article in terms of sentences instead of characters, which is more amenable to certain measures of the “importance” of an event’s positioning within an article.
Actor1CharOffset	INTEGER	NULLABLE	The location within the article (in terms of English characters) where Actor1 was found.  This can be used in combination with the GKG or other analysis to identify further characteristics and attributes of the actor.  NOTE: due to processing performed on each article, this may be slightly offset from the position seen when the article is rendered in a web browser.
Actor2CharOffset	INTEGER	NULLABLE	The location within the article (in terms of English characters) where Actor2 was found.  This can be used in combination with the GKG or other analysis to identify further characteristics and attributes of the actor.  NOTE: due to processing performed on each article, this may be slightly offset from the position seen when the article is rendered in a web browser.
ActionCharOffset	INTEGER	NULLABLE	The location within the article (in terms of English characters) where the core Action description was found.  This can be used in combination with the GKG or other analysis to identify further characteristics and attributes of the actor.  NOTE: due to processing performed on each article, this may be slightly offset from the position seen when the article is rendered in a web browser.
InRawText	INTEGER	NULLABLE	This records whether the event was found in the original unaltered raw article text (a value of 1) or whether advanced natural language processing algorithms were required to synthesize and rewrite the article text to identify the event (a value of 0).  See the discussion on the Confidence field below for more details.  Mentions with a value of “1” in this field likely represent strong detail-rich references to an event.
Confidence	INTEGER	NULLABLE	Percent confidence in the extraction of this event from this article.  See the discussion in the codebook at http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf
MentionDocLen	INTEGER	NULLABLE	The length in English characters of the source document (making it possible to filter for short articles focusing on a particular event versus long summary articles that casually mention an event in passing).
MentionDocTone	FLOAT	NULLABLE	The same contents as the AvgTone field in the Events table, but computed for this particular article.  NOTE: users interested in emotional measures should use the MentionIdentifier field above to merge the Mentions table with the GKG table to access the complete set of 2,300 emotions and themes from the GCAM system.
MentionDocTranslationInfo	STRING	NULLABLE	This field is internally delimited by semicolons and is used to record provenance information for machine translated documents indicating the original source language and the citation of the translation system used to translate the document for processing.  It will be blank for documents originally in English.  At this time the field will also be blank for documents translated by a human translator and provided to GDELT in English (such as BBC Monitoring materials) – in future this field may be expanded to include information on human translation pipelines, but at present it only captures information on machine translated materials.  An example of the contents of this field might be “srclc:fra; eng:Moses 2.1.1 / MosesCore Europarl fr-en / GT-FRA 1.0”.  NOTE:  Machine translation is often not as accurate as human translation and users requiring the highest possible confidence levels may wish to exclude events whose only mentions are in translated reports, while those needing the highest-possible coverage of the non-Western world will find that these events often offer the earliest glimmers of breaking events or smaller-bore events of less interest to Western media.o SRCLC. This is the Source Language Code, representing the three-letter ISO639-2 code of the language of the original source material. o ENG.  This is a textual citation string that indicates the engine(s) and model(s) used to translate the text.  The format of this field will vary across engines and over time and no expectations should be made on the ordering or formatting of this field.  In the example above, the string “Moses 2.1.1 / MosesCore Europarl fr-en / GT-FRA 1.0” indicates that the document was translated using version 2.1.1 of the Moses   SMT platform, using the “MosesCore Europarl fr-en” translation and language models, with the final translation enhanced via GDELT Translingual’s own version 1.0 French translation and language models.  A value of “GT-ARA 1.0” indicates that GDELT Translingual’s version 1.0 Arabic translation and language models were the sole resources used for translation.  Additional language systems used in the translation pipeline such as word segmentation systems are also captured in this field such that a value of “GT-ZHO 1.0 / Stanford PKU” indicates that the Stanford Chinese Word Segmenter   was used to segment the text into individual words and sentences, which were then translated by GDELT Translingual’s own version 1.0 Chinese (Traditional or Simplified) translation and language models.
Extras	STRING	NULLABLE	This field is currently blank, but is reserved for future use to encode special additional measurements for selected material.
'''
```


```python
from StringIO import StringIO
eventMentions = pd.read_csv(StringIO(text),delimiter='\t',header=None)
```


```python
eventMentions.columns=['tableId', 'dataType','Empty', 'Description']
```


```python
eventMentions.to_csv('../../gdelt2HeaderRows/schema_csvs/GDELT_2.0_eventMentions_Column_Labels_Header_Row_Sep2016.tsv',encoding='utf-8',sep='\t')
```


```python
eventMentions
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tableId</th>
      <th>dataType</th>
      <th>Empty</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GLOBALEVENTID</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This is the ID of the event that was mentioned...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>EventTimeDate</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This is the 15-minute timestamp (YYYYMMDDHHMMS...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MentionTimeDate</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This is the 15-minute timestamp (YYYYMMDDHHMMS...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MentionType</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This is a numeric identifier that refers to th...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MentionSourceName</td>
      <td>STRING</td>
      <td>NULLABLE</td>
      <td>This is a human-friendly identifier of the sou...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>MentionIdentifier</td>
      <td>STRING</td>
      <td>NULLABLE</td>
      <td>This is the unique external identifier for the...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SentenceID</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The sentence within the article where the even...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Actor1CharOffset</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The location within the article (in terms of E...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Actor2CharOffset</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The location within the article (in terms of E...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ActionCharOffset</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The location within the article (in terms of E...</td>
    </tr>
    <tr>
      <th>10</th>
      <td>InRawText</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This records whether the event was found in th...</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Confidence</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>Percent confidence in the extraction of this e...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>MentionDocLen</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The length in English characters of the source...</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MentionDocTone</td>
      <td>FLOAT</td>
      <td>NULLABLE</td>
      <td>The same contents as the AvgTone field in the ...</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MentionDocTranslationInfo</td>
      <td>STRING</td>
      <td>NULLABLE</td>
      <td>This field is internally delimited by semicolo...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Extras</td>
      <td>STRING</td>
      <td>NULLABLE</td>
      <td>This field is currently blank, but is reserved...</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Add New Fields</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
gkgdf.to_csv('../../gdelt2HeaderRows/schema_csvs/GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv',encoding='utf-8',sep='\t')
```


```python
gkgdf.to_csv('GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.csv',sep='\t',index=False,encoding='utf-8')
```


```python
headers.to_csv('GDELT_2.0_Events_Column_Labels_Header_Row_Sep2016.csv', index=False,encoding='utf-8')
```


```python
import pandas as pd
mentionsdf = pd.read_csv(StringIO(text),delimiter='\t',header=None)
mentionsdf.columns=headers.columns.tolist()
```


```python

```
