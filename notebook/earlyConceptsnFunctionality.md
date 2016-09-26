
# GDELT 1.0 Code (skip)

Will have to integrate this into GDELT 2.0.  Headers are different.  GDELT 1.0 goes back to 1979.  2.0 only goes back to Feb 2015

![](http://data.gdeltproject.org/dailymaps_noaasos/spinningglobe.gif)


```python
from IPython.display import Image
Image(url='../utils/images/spinningglobe.gif')
```




<img src="../utils/images/spinningglobe.gif"/>




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
import pandas as pd
import numpy as np
import re
from dateutil.parser import parse
```

# Logic for GDELT module

Enter a date or date range.  GDELT 2.0 only goes to Feb 18 2015.  GDELT 1.0 goes back to 1979.  

Convert the entered date or date range to string, search for string in the master df list.  Use the tblType parameter to pull the correct table(s).  

* default is take current time and most recent file
* enter historical date; defaults to last record of day
    * parse
    * add feature to enter time for historical and pull closest 15 minute file
    * date range will pull last file for each day and concatenate into single dataframe
    
choose a database
*  Select between events, event mentions or gkg

return it as a python or R dataframe
*  use the feather library for Python

*********************


# URLS

The main urls that we need to hit to return data.


```python
masterListUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
baseUrl = 'http://data.gdeltproject.org/gdeltv2/'
```

# Parameters and Global Variables

Section contains variables that will be `self.` objects in the classes.


```python

'''
Listing of all GDELT 15 minute dumps. Code retrieves the list,
splits it on the new line character, and then splits on the space. 
We delete the last entry because it's empty.  
'''
directory = requests.get(masterListUrl)
clean = directory.content.split('\n')
clean = map(lambda x: x.split(' '),clean)
del clean[-1]

"""
Setting up the master list as dataframe for querying
this will be inside the class
"""
masterdf = pd.DataFrame(clean)
masterdf.fillna('',inplace=True)
```


```python
# table type = tblType
graph = 'gkg'
events = 'events' # includes new GDELT 2.0 mentions table; merged on globaleventid

tblType = events  # default to events db
```


## Date Parameters that will be entered

Location to hold testing spot for all the different type of parameters that can be entered.


```python
defaultDateEntry = "" # string
stringDateEntry = " 2016 09 18" # string
historicalDateEntry = "2015 02 25" #string
errorDate = "What in the heck" # error string
listOfdates = ['Sep 1 2016','2016 09 24'] # list, len 2
moreThanTwo= ['Sept 20 2016','June 3 2011','January 1, 2013'] # list, len greater than 2d

date = defaultDateEntry
time = ""
```


```python
date
```




    ['Sep 1 2016', '2016 09 24']



## Setting the values for the headers

Headers are set based on `tblType` value passed in.  Will default to the events DB headers.  


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

**************************


# Checking Inputs of functions and parameters

We need to see how many dates are passed into the function.  Use the logic above. 


```python
import traceback,sys
import datetime
from dateutil.parser import parse
import numpy as np

def dateInputCheck(date):
    if isinstance(date,str):
        if date != "":
            if parse(date) > datetime.datetime.now():
                raise ValueError('Your date is greater than the current date.  Please enter a relevant date.')
            elif parse(date)<parse('Feb 18 2015'):
                raise ValueError('GDELT 2.0 only supports \'Feb 18 2015 - Present\' queries currently. Try another date.')

    elif isinstance(date,list):
        if len(date)==1:
            try:
                if parse("".join(date)) > datetime.datetime.now():
                    raise ValueError('Your date is greater than the current date.  Please enter a relevant date.')
                elif parse("".join(date)) < parse('Feb 18 2015'):
                    raise ValueError('GDELT 2.0 only supports \'Feb 18 2015 - Present\' queries currently. Try another date.')
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError("One or more of your input date strings does not parse to a date format. Check input.")

        
        elif len(date)==2:
            try:
                map(parse,date)
            except Exception as exc:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError("One or more of your input date strings does not parse to a date format. Check input.")

            if bool(parse(date[0])<parse(date[1])) == False:
                raise ValueError('Start date greater than end date. Check date strings.')
                
            if np.all(np.logical_not(np.array(map(parse,date))> datetime.datetime.now())) == False:
                raise ValueError("One of your dates is greater than the current date. Check input date strings.")

            
        elif len(date)>2:

            try:
                map(parse,date)
            except Exception as exc:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                raise ValueError("One or more of your input date strings does not parse to a date format. Check input.")
                
            if np.all(np.logical_not(np.array(map(parse,date))> datetime.datetime.now())) == False:
                raise ValueError("One or more of your input date strings does not parse to a date format. Check input.")

        
```


```python
date=['2016 9 12']
dateInputCheck(date)
```

### Checking the tblType input


```python

# gets the urls from array
# resultMaster = vectorizedUrlFinder(UrlFinder,datesToPull)


def tblCheck(tbl):
    '''Checking the input of tblType.'''
    if tbl == 'events' or tbl == '' or tbl == 'mentions':
        resultsUrlList = resultMaster[2][resultMaster[2].str.contains('export|mentions')]
    elif tbl == 'gkg':
        resultsUrlList = resultMaster[2][resultMaster[2].str.contains('gkg')]
    else:
        raise ValueError ("Incorrect parameter \'{0}\' entered.  Did you mean to use \'{0}\' as the parameter?\nPlease check your \'tblType\' parameters.".format(tblType))
    return resultsUrlList
```

*************

# Date Functionality (Date ranges)

Use the numpy date range functionality to create strings of dates between ranges in a list.  Then, use the dateutil tool to parse those strings into the correct format.  Then run a query for each date, return the dataframe, and concatenate into a single one.

* Logic
    * If length of passed in date less than zero, raise error
    * If length is equal to one, find that one date's table or graph
    * If length equal to two:
        * if dates are chronological, covert to numpy range and pull all tables or graphs, but raise warning for long ranges
        * if dates are not chronological, get individual dates
    * If length greater than two, get the individual dates
        * initially, return the latest time
        * add option to return closest 15 minute interval to passed in time

## Code Pieces and Functions


```python
# numpy example of ranging the date
np.arange('2016-08-01', '2016-09-16', dtype='datetime64[D]');
```


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


# def gdelt_timeString(dateInputVar):
#     """Convert date to GDELT string file format for query."""
    
#     multiplier = dateInputVar.tolist().minute / 15
#     multiple = 15 * multiplier
#     queryDate = np.where(
#             multiplier > 1,dateInputVar.tolist().replace(
#             minute=0, second=0) + datetime.timedelta(
#             minutes=multiple),
#             dateInputVar.tolist().replace(
#             minute=0, second=0,microsecond=0000)
#             )
    
#     # Check for date equality on historical query
#     modifierTip = datetime.datetime.now().replace(
#         hour=0,minute=0,second=0,microsecond=0
#         ) == queryDate.tolist().replace(
#         hour=0,minute=0,second=0,microsecond=0
#         )
    
#     # Based on modifier, get oldest file for historical query
#     queryDate = np.where(
#         modifierTip==False,
#         queryDate.tolist().replace(
#             hour=23,
#             minute=45,
#             second=00,
#             microsecond=0000
#             ),queryDate
#         )
    
# #     print modifierTip
#     return queryDate.tolist().strftime("%Y%m%d%H%M%S")

#############################################
# Match parsed date to GDELT master list
#############################################

# def match_date(dateString):
#     """Return dataframe with GDELT data for matching date"""
    
#     masterListUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
#     directory = requests.get(masterListUrl)
#     results = directory.content.split('\n')
#     results = map(lambda x: x.split(' '),results)
#     masterListdf = pd.DataFrame(results)
#     return masterListdf[
#         masterListdf[2].str.contains(
#             dateString
#             )==True
#         ]
    
def dateformatter(datearray):
    """Function to format strings for numpy arange"""
    return parse(datearray).strftime("%Y-%m-%d")
    
def dateRanger(originalArray):
    """Function to vectorize date formatting function.
    Creates datetime.date objects for each day in the range
    and stores in a numpy array.
    
    Example
    
    Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Input data, where ``n_samples`` is the number of samples and
            ``n_features`` is the number of features.
    Returns
    -------
    self : object
        Returns self.
    """
    if isinstance(originalArray,str):
        """Check user input to retrieve date query."""
    
        return np.where(len(originalArray)==0,np.array(datetime.datetime.now()),
                 parse_date(originalArray))
    
    elif isinstance(originalArray,list):
        if len(originalArray)==1:
            return np.array(parse("".join(originalArray)))
        elif len(originalArray)>2:
            return np.array(map(parse,originalArray),dtype='datetime64[D]')
        else:
            cleaner = np.vectorize(dateformatter)
            converted = cleaner(originalArray).tolist()
            dates = np.arange(converted[0],converted[1],dtype='datetime64[D]')
            dates = np.append(dates,np.datetime64(datetime.date.today())) # numpy range is not endpoint inclusive
            return dates

def gdeltRangeString(element):
    if element == datetime.date.today():
        multiplier = datetime.datetime.now().minute / 15
        multiple = 15 * multiplier
        converted = datetime.datetime.now().replace(minute=multiple,second=0)
    else:
        converted = (datetime.datetime.combine(element,datetime.time.min) + 
            datetime.timedelta(
                                minutes=45,hours=23
                                )
                               )
    return converted.strftime('%Y%m%d%H%M%S')



def vectorizer(function,dateArray):
    helper = np.vectorize(function)
    return helper(dateArray.tolist()).tolist()

# Finds the urls from an array of dates

def UrlFinder(targetDate):
    return masterdf[masterdf[2].str.contains(targetDate)]

def vectorizedUrlFinder(function,urlList):
    helper=np.vectorize(function)
    return pd.concat(helper(urlList).tolist())

def downloadVectorizer(function,urlList):
    '''
    test2 = downloadVectorizer(downloadAndExtract,b)
    test2.columns=gkgHeaders.tableId.tolist()
    '''
    helper=np.vectorize(function)
    return pd.concat(helper(urlList).tolist())

```

### Working Examples for Single Date Functionality


```python
date = '2016 9 12'

vectorizer(gdeltRangeString,dateRanger(date))
```




    '20160912234500'



### Working Examples of Date Range Functionality


```python
date=['2016 09 01','2016 09 24']
(dateRanger(date))
```




    array(['2016-09-01', '2016-09-02', '2016-09-03', '2016-09-04',
           '2016-09-05', '2016-09-06', '2016-09-07', '2016-09-08',
           '2016-09-09', '2016-09-10', '2016-09-11', '2016-09-12',
           '2016-09-13', '2016-09-14', '2016-09-15', '2016-09-16',
           '2016-09-17', '2016-09-18', '2016-09-19', '2016-09-20',
           '2016-09-21', '2016-09-22', '2016-09-23', '2016-09-25'], dtype='datetime64[D]')




```python
# converts to gd
datesToPull = vectorizer(gdeltRangeString,dateRanger(date))
```


```python
# gets the urls from array
resultMaster = vectorizedUrlFinder(UrlFinder,datesToPull)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-84-19c02f5f54e7> in <module>()
          1 # gets the urls from array
    ----> 2 resultMaster = vectorizedUrlFinder(UrlFinder,datesToPull)
    

    <ipython-input-76-d6b90032dcea> in vectorizedUrlFinder(function, urlList)
        139 def vectorizedUrlFinder(function,urlList):
        140     helper=np.vectorize(function)
    --> 141     return pd.concat(helper(urlList).tolist())
        142 
        143 def downloadVectorizer(function,urlList):


    /Users/linwood/anaconda/envs/gdelt/lib/python2.7/site-packages/numpy/lib/function_base.pyc in __call__(self, *args, **kwargs)
       2216             vargs.extend([kwargs[_n] for _n in names])
       2217 
    -> 2218         return self._vectorize_call(func=func, args=vargs)
       2219 
       2220     def _get_ufunc_and_otypes(self, func, args):


    /Users/linwood/anaconda/envs/gdelt/lib/python2.7/site-packages/numpy/lib/function_base.pyc in _vectorize_call(self, func, args)
       2279             _res = func()
       2280         else:
    -> 2281             ufunc, otypes = self._get_ufunc_and_otypes(func=func, args=args)
       2282 
       2283             # Convert args to object arrays first


    /Users/linwood/anaconda/envs/gdelt/lib/python2.7/site-packages/numpy/lib/function_base.pyc in _get_ufunc_and_otypes(self, func, args)
       2241             # arrays (the input values are not checked to ensure this)
       2242             inputs = [asarray(_a).flat[0] for _a in args]
    -> 2243             outputs = func(*inputs)
       2244 
       2245             # Performance note: profiling indicates that -- for simple


    <ipython-input-76-d6b90032dcea> in UrlFinder(targetDate)
        135 
        136 def UrlFinder(targetDate):
    --> 137     return masterdf[masterdf[2].str.contains(targetDate)]
        138 
        139 def vectorizedUrlFinder(function,urlList):


    NameError: global name 'masterdf' is not defined



```python
resultMaster
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-81-afe18af84056> in <module>()
    ----> 1 resultMaster
    

    NameError: name 'resultMaster' is not defined


## Testing Area for Dates; Above is good, below is experimental


```python
tblCheck('gkg')
```




    160895    http://data.gdeltproject.org/gdeltv2/201609012...
    161183    http://data.gdeltproject.org/gdeltv2/201609022...
    161471    http://data.gdeltproject.org/gdeltv2/201609032...
    161756    http://data.gdeltproject.org/gdeltv2/201609042...
    162044    http://data.gdeltproject.org/gdeltv2/201609052...
    162332    http://data.gdeltproject.org/gdeltv2/201609062...
    162620    http://data.gdeltproject.org/gdeltv2/201609072...
    162908    http://data.gdeltproject.org/gdeltv2/201609082...
    163196    http://data.gdeltproject.org/gdeltv2/201609092...
    163484    http://data.gdeltproject.org/gdeltv2/201609102...
    163772    http://data.gdeltproject.org/gdeltv2/201609112...
    164060    http://data.gdeltproject.org/gdeltv2/201609122...
    164348    http://data.gdeltproject.org/gdeltv2/201609132...
    164639    http://data.gdeltproject.org/gdeltv2/201609142...
    164924    http://data.gdeltproject.org/gdeltv2/201609152...
    165212    http://data.gdeltproject.org/gdeltv2/201609162...
    165500    http://data.gdeltproject.org/gdeltv2/201609172...
    165788    http://data.gdeltproject.org/gdeltv2/201609182...
    166076    http://data.gdeltproject.org/gdeltv2/201609192...
    166364    http://data.gdeltproject.org/gdeltv2/201609202...
    166652    http://data.gdeltproject.org/gdeltv2/201609212...
    166937    http://data.gdeltproject.org/gdeltv2/201609222...
    167222    http://data.gdeltproject.org/gdeltv2/201609232...
    167423    http://data.gdeltproject.org/gdeltv2/201609241...
    Name: 2, dtype: object




```python
for l in masterdf[2][masterdf[2].str.contains(datesToPull[20])]:
    print l
```

    http://data.gdeltproject.org/gdeltv2/20160921234500.export.CSV.zip
    http://data.gdeltproject.org/gdeltv2/20160921234500.mentions.CSV.zip
    http://data.gdeltproject.org/gdeltv2/20160921234500.gkg.csv.zip



```python

    
```


```python

```


```python
test2.reset_index(drop=True,inplace=True)
```


```python
test2
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GKGRECORDID</th>
      <th>DATE</th>
      <th>SourceCollectionIdentifier</th>
      <th>SourceCommonName</th>
      <th>DocumentIdentifier</th>
      <th>Counts</th>
      <th>V2Counts</th>
      <th>Themes</th>
      <th>V2Themes</th>
      <th>Locations</th>
      <th>...</th>
      <th>GCAM</th>
      <th>SharingImage</th>
      <th>RelatedImages</th>
      <th>SocialImageEmbeds</th>
      <th>SocialVideoEmbeds</th>
      <th>Quotations</th>
      <th>AllNames</th>
      <th>Amounts</th>
      <th>TranslationInfo</th>
      <th>Extras</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20160901234500-0</td>
      <td>20160901234500</td>
      <td>2</td>
      <td>BBC Monitoring</td>
      <td>Facebook in Russian and Uzbek /BBC Monitoring/...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MEDIA_SOCIAL;GENERAL_HEALTH;MEDICAL;TAX_ETHNIC...</td>
      <td>GENERAL_HEALTH,30;MEDICAL,30;MEDIA_SOCIAL,10;M...</td>
      <td>1#Uzbekistan#UZ#UZ#41#64#UZ</td>
      <td>...</td>
      <td>wc:289,c12.1:32,c12.10:13,c12.12:7,c12.13:1,c1...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>487|265||Dear friends , I sincerely apologise ...</td>
      <td>Uzbek President Islam Karimov,130;Islam Karimo...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20160901234500-1</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>nigeriasun.com</td>
      <td>http://www.nigeriasun.com/index.php/sid/247252977</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>4#Mumbai, Maharashtra, India#IN#IN16#18.975#72...</td>
      <td>...</td>
      <td>wc:1024,c1.1:2,c1.3:1,c12.1:52,c12.10:103,c12....</td>
      <td>http://www.nigeriasun.comhttp://cdn.bignewsnet...</td>
      <td>http://cdn.bignewsnetwork.com/ani1472717432.jpg</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Hewlett Packard Enterprise,232;Country Directo...</td>
      <td>8,introduces a unified architecture,267;8,prov...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20160901234500-2</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>ecigintelligenceinfo.com</td>
      <td>http://ecigintelligenceinfo.com/2016/09/01/how...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ENV_SOLAR;WB_678_DIGITAL_GOVERNMENT;WB_694_BRO...</td>
      <td>GENERAL_GOVERNMENT,1765;TAX_ETHNICITY_INDIAN,1...</td>
      <td>1#United States#US#US#38#-97#US;1#Madagascar#M...</td>
      <td>...</td>
      <td>wc:301,c1.1:2,c12.1:16,c12.10:23,c12.12:7,c12....</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://youtube.com/watch?v=mIBTg7q9oNc;</td>
      <td>1406|136||The annular eclipse is expected to o...</td>
      <td>South Africam Madagascar,129;South Atlantic Oc...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://live.slooh.com/stadium/live...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20160901234500-3</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>961theeagle.com</td>
      <td>http://961theeagle.com/tags/geico/</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>WB_135_TRANSPORT;WB_1973_FINANCIAL_RISK_REDUCT...</td>
      <td>WB_1973_FINANCIAL_RISK_REDUCTION,83;WB_1973_FI...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:165,c1.2:3,c12.1:16,c12.10:9,c12.12:4,c12.1...</td>
      <td>http://961wodz.com/files/2015/01/wodzfmlogov2....</td>
      <td>http://961theeagle.com/files/2013/02/pig-e1361...</td>
      <td>NaN</td>
      <td>https://youtube.com/subscribe_embed?bsv&amp;usegap...</td>
      <td>NaN</td>
      <td>New York State Department,32;Text Stop,111;New...</td>
      <td>1000000,Moms,694;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://961wodz.com/tags/geico/;htt...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20160901234500-4</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>financialpost.com</td>
      <td>http://business.financialpost.com/fp-comment/k...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>LEADER;TAX_FNCACT;TAX_FNCACT_POLITICIANS;MANMA...</td>
      <td>ECON_FOREIGNINVEST,1166;ECON_FOREIGNINVEST,550...</td>
      <td>1#United States#US#US#38#-97#US;1#India#IN#IN#...</td>
      <td>...</td>
      <td>wc:944,c1.2:10,c1.3:2,c12.1:78,c12.10:138,c12....</td>
      <td>http://wpmedia.business.financialpost.com/2014...</td>
      <td>http://wpmedia.business.financialpost.com/2014...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5283|32||base erosion and profit shifting</td>
      <td>Kevin Libin,12;Elon Musk,169;Silicon Valley,32...</td>
      <td>13000000000,euros,814;19000000000,dollars ,835...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://business.financialpost.com/...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20160901234500-5</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>nvi.com.au</td>
      <td>http://www.nvi.com.au/story/4137790/mel-gibson...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_ETHNICITY;TAX_ETHNICITY_AUSTRALIAN;TAX_FNC...</td>
      <td>TAX_ETHNICITY_ENGLISH,543;TAX_WORLDLANGUAGES_E...</td>
      <td>3#Hollywood, California, United States#US#USCA...</td>
      <td>...</td>
      <td>wc:400,c1.1:1,c1.2:1,c1.4:1,c12.1:31,c12.10:29...</td>
      <td>http://nnimgt-a.akamaihd.net/transform/v1/crop...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2415|85||a common practice of the Holy Father ...</td>
      <td>Mel Gibson,41;Lethal Weapon,216;Jesus Christ I...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.hollywoodreporter.com/n...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20160901234500-6</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>wsbtradio.com</td>
      <td>http://wsbtradio.com/sting-wants-people-to-be-...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>SECURITY_SERVICES;TAX_FNCACT;TAX_FNCACT_POLICE...</td>
      <td>TAX_FNCACT_WOMAN,698;SECURITY_SERVICES,456;SEC...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:225,c1.1:2,c1.4:1,c12.1:26,c12.10:19,c12.12...</td>
      <td>http://i2.wp.com/wsbtradio.com/wp-content/uplo...</td>
      <td>http://i2.wp.com/wsbtradio.com/wp-content/uplo...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Wants People,21;His New,51;Stop Thinking About...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.sting.com/news/title/ho...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20160901234500-7</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>iheart.com</td>
      <td>http://wnok.iheart.com/articles/trending-10465...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_FNCACT;TAX_FNCACT_SINGER;USPEC_POLITICS_GE...</td>
      <td>TAX_RELIGION_CHRISTIAN,319;TAX_ETHNICITY_CHRIS...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:189,c12.1:12,c12.10:13,c12.12:4,c12.13:1,c1...</td>
      <td>http://i.iheart.com/v3/url/aHR0cDovL2kuaWhlYXJ...</td>
      <td>http://i.iheart.com/v3/re/new_assets/57c7469d0...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Chris Brown,35;Baylee Curran,65;Harvey Levin,796</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.iheart.com/artist/chris...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20160901234500-8</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>wvalways.com</td>
      <td>http://www.wvalways.com/story/32964796/law-enf...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>CRIME_ILLEGAL_DRUGS;DRUG_TRADE;WB_1331_HEALTH_...</td>
      <td>TAX_DISEASE_EPIDEMIC,1648;WB_635_PUBLIC_HEALTH...</td>
      <td>3#Harrison County, West Virginia, United State...</td>
      <td>...</td>
      <td>wc:328,c12.1:21,c12.10:28,c12.11:1,c12.12:12,c...</td>
      <td>http://WBOY.images.worldnow.com/images/1165234...</td>
      <td>http://WBOY.images.worldnow.com/images/1165234...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Chief Deputy Jeff McAtee,311;Harrison County S...</td>
      <td>300,cases reported,1012;</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Marisa Matyola;Harrison County R...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20160901234500-9</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>schoolloop.com</td>
      <td>http://anhs-capousd-ca.schoolloop.com/news/vie...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_FNCACT;TAX_FNCACT_PRINCIPAL;EDUCATION;SOC_...</td>
      <td>TAX_FNCACT_EXECUTIVE_DIRECTOR,2383;TAX_FNCACT_...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:396,c12.1:29,c12.10:35,c12.12:9,c12.13:11,c...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://youtube.com/user/anhsasb;</td>
      <td>NaN</td>
      <td>About Aliso,12;Media Activities,140;Aliso Athl...</td>
      <td>33122,Valle Road,2079;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://anhs-capousd-ca.schoolloop....</td>
    </tr>
    <tr>
      <th>10</th>
      <td>20160901234500-10</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>iheart.com</td>
      <td>http://thebreakfastclub.iheart.com/articles/en...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_FNCACT;TAX_FNCACT_CHILDREN;TAX_FNCACT_BABY;</td>
      <td>TAX_FNCACT_CHILDREN,209;TAX_FNCACT_BABY,473;</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:120,c1.1:1,c12.1:15,c12.10:12,c12.12:2,c12....</td>
      <td>http://i.iheart.com/v3/url/aHR0cDovL2kuaWhlYXJ...</td>
      <td>http://i.iheart.com/v3/re/new_assets/57c89e110...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>New Saint West Pics Emerged,28;Want To Adopt H...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.iheart.com/artist/kanye...</td>
    </tr>
    <tr>
      <th>11</th>
      <td>20160901234500-11</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>galesburg.com</td>
      <td>http://www.galesburg.com/entertainment/2016090...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>DELAY;TAX_FNCACT;TAX_FNCACT_MAIDS;</td>
      <td>TAX_FNCACT_MAIDS,83;TAX_FNCACT_MAIDS,212;TAX_F...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:165,c12.1:13,c12.10:16,c12.12:7,c12.14:11,c...</td>
      <td>http://www.galesburg.com/storyimage/ZZ/2016090...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Devious Maids,86;Desperate Housewive,170;Marc ...</td>
      <td>4,finale now series finale,417;3,rating,449;2,...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://TVGuide.com;http://deadline...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>20160901234500-12</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>latimes.com</td>
      <td>http://www.latimes.com/local/lanow/la-me-holly...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_FNCACT;TAX_FNCACT_ARSONIST;CRM_ARSON;CRISI...</td>
      <td>TAX_FNCACT_DEPUTY,706;TAX_FNCACT_DEPUTY,1618;T...</td>
      <td>1#United States#US#US#38#-97#US;3#Hollywood, C...</td>
      <td>...</td>
      <td>wc:289,c12.1:17,c12.10:16,c12.12:9,c12.13:5,c1...</td>
      <td>http://www.trbimg.com/img-56fd643a/turbine/la-...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>306|39||to harm and terrorize as many resident...</td>
      <td>Harry Burkhart,186;Los Angeles,266;San Fernand...</td>
      <td>47,counts,289;50,fires,321;3000000,dollars ,53...</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Los Angeles Times;Richard Winton...</td>
    </tr>
    <tr>
      <th>13</th>
      <td>20160901234500-13</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>dailydemocrat.com</td>
      <td>http://www.dailydemocrat.com/government-and-po...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_POLITICAL_PARTY;TAX_POLITICAL_PARTY_DEMOCR...</td>
      <td>ECON_HOUSING_PRICES,3886;TAX_POLITICAL_PARTY_R...</td>
      <td>2#California, United States#US#USCA#36.17#-119...</td>
      <td>...</td>
      <td>wc:1023,c1.2:2,c1.3:10,c12.1:56,c12.10:97,c12....</td>
      <td>http://local.dailydemocrat.com/common/dfm/asse...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Jerry Brown,236;Assembly Bill,2951;California ...</td>
      <td>25,secs ago SACRAMENTO &gt;&gt;,48;1000000000,dollar...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>14</th>
      <td>20160901234500-14</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>northerndailyleader.com.au</td>
      <td>http://www.northerndailyleader.com.au/story/41...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>4#Sydney, New South Wales, Australia#AS#AS02#-...</td>
      <td>...</td>
      <td>wc:246,c1.2:1,c12.1:18,c12.10:17,c12.12:7,c12....</td>
      <td>http://nnimgt-a.akamaihd.net/transform/v1/crop...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Tamworth Basketball,20;State Championship,59;N...</td>
      <td>3,qualified through their participation,282;8,...</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Australian Community Media - Fai...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>20160901234500-15</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>ktep.org</td>
      <td>http://ktep.org/post/making-clinton-and-trump</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_FNCACT;TAX_FNCACT_SUPPORTERS;TAX_FNCACT_CA...</td>
      <td>TAX_FNCACT_CANDIDATES,216;TAX_FNCACT_CANDIDATE...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:122,c1.4:1,c12.1:11,c12.10:11,c12.12:3,c12....</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Rachel Martin,17;Hillary Clinton,173;Donald Tr...</td>
      <td>2,candidates also inspire some,178;2,most unpo...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://ktep.org/people/rachel-mart...</td>
    </tr>
    <tr>
      <th>16</th>
      <td>20160901234500-16</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>iheart.com</td>
      <td>http://640wgst.iheart.com/articles/national-ne...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>GENERAL_GOVERNMENT;TAX_WORLDLANGUAGES;TAX_WORL...</td>
      <td>TAX_WORLDLANGUAGES_MASSACHUSETTS,425;GENERAL_G...</td>
      <td>2#New York, United States#US#USNY#42.1497#-74....</td>
      <td>...</td>
      <td>wc:95,c12.1:2,c12.10:3,c12.12:3,c12.14:1,c12.3...</td>
      <td>http://i.iheart.com/v3/url/aHR0cDovL2kuaWhlYXJ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maribel Martinez,156;Andy Martinez Mercado,204...</td>
      <td>200,miles away,287;</td>
      <td>NaN</td>
      <td>&lt;PAGE_ALTURL_MOBILE&gt;http://m.640wgst.iheart.co...</td>
    </tr>
    <tr>
      <th>17</th>
      <td>20160901234500-17</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>iheart.com</td>
      <td>http://thebull1017.iheart.com/onair/colton-bra...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>EPU_CATS_MIGRATION_FEAR_FEAR;EPU_CATS_NATIONAL...</td>
      <td>WB_2937_SILVER,707;WB_507_ENERGY_AND_EXTRACTIV...</td>
      <td>2#California, United States#US#USCA#36.17#-119...</td>
      <td>...</td>
      <td>wc:121,c1.1:2,c12.1:13,c12.10:9,c12.12:1,c12.1...</td>
      <td>http://i.iheart.com/v3/url/aHR0cDovL2NvbnRlbnQ...</td>
      <td>http://content.clearchannel.com/cc-common/mlib...</td>
      <td>NaN</td>
      <td>https://youtube.com/coltonbradfordTV/;</td>
      <td>NaN</td>
      <td>Getty Images,95;Twilight Zone Tower,165;Califo...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_ALTURL_MOBILE&gt;http://m.thebull1017.ihear...</td>
    </tr>
    <tr>
      <th>18</th>
      <td>20160901234500-18</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>asiaone.com</td>
      <td>http://forums.asiaone.com/showthread.php?s=9ee...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>EPU_CATS_REGULATION;WB_678_DIGITAL_GOVERNMENT;...</td>
      <td>EPU_CATS_REGULATION,1112;CRISISLEX_CRISISLEXRE...</td>
      <td>1#Singapore#SN#SN#1.3667#103.8#SN</td>
      <td>...</td>
      <td>wc:215,c12.1:47,c12.10:23,c12.12:3,c12.13:4,c1...</td>
      <td>http://forums.asiaone.com/images/asiaone2011/a...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Press Holdings Ltd,1501;Data Protection,1549</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://forums.asiaone.com/;http://...</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20160901234500-19</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>961theeagle.com</td>
      <td>http://961theeagle.com/save-a-life-take-a-moha...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_WORLDLANGUAGES;TAX_WORLDLANGUAGES_MOHAWK;T...</td>
      <td>TAX_WORLDLANGUAGES_MOHAWK,33;TAX_WORLDLANGUAGE...</td>
      <td>1#United States#US#US#38#-97#US;2#New York, Un...</td>
      <td>...</td>
      <td>wc:110,c12.1:8,c12.10:12,c12.12:3,c12.13:6,c12...</td>
      <td>http://lite987.com/files/2016/09/Red-Cross.jpg...</td>
      <td>http://lite987.com/files/2016/09/Red-Cross.jpg</td>
      <td>NaN</td>
      <td>https://youtube.com/subscribe_embed?bsv&amp;usegap...</td>
      <td>NaN</td>
      <td>Mohawk Valley Red Cross,51;Mohawk Valley Chapt...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.redcross.org/take-a-cla...</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20160901234500-20</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>wfsb.com</td>
      <td>http://www.wfsb.com/story/32958618/strong-link...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_DISEASE;TAX_DISEASE_ZIKA;TAX_DISEASE_OUTBR...</td>
      <td>TAX_POLITICAL_PARTY_REPUBLICANS,2721;UNGP_FORE...</td>
      <td>3#Miami, Florida, United States#US#USFL#25.774...</td>
      <td>...</td>
      <td>wc:720,c12.1:24,c12.10:71,c12.12:34,c12.13:28,...</td>
      <td>http://wncontent.images.worldnow.com/images/74...</td>
      <td>http://images.worldnow.com/Revenue/images/2755...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>HealthDay News,73;Latin America,668;Dominican ...</td>
      <td>500,cases of the Guillain,842;194000000,dollar...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.cdc.gov/niosh/topics/ou...</td>
    </tr>
    <tr>
      <th>21</th>
      <td>20160901234500-21</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>silive.com</td>
      <td>http://www.silive.com/news/index.ssf/2016/09/p...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>SECURITY_SERVICES;TAX_FNCACT;TAX_FNCACT_POLICE...</td>
      <td>CRISISLEX_C08_TELECOM,1675;TAX_FNCACT_DEPUTY,6...</td>
      <td>1#Spain#SP#SP#40#-4#SP</td>
      <td>...</td>
      <td>wc:302,c1.2:1,c1.3:1,c12.1:8,c12.10:12,c12.11:...</td>
      <td>http://image.silive.com/home/silive-media/widt...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://youtube.com/channel/UC1KF4bZvT5iAbAHVv...</td>
      <td>NaN</td>
      <td>Curtis Hill Deli,469;Low Terrace,507;Deputy Co...</td>
      <td>2,robberies,233;10,Daniel Low Terrace,395;579,...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.silive.com/news/index.s...</td>
    </tr>
    <tr>
      <th>22</th>
      <td>20160901234500-22</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>sfchronicle.com</td>
      <td>http://www.sfchronicle.com/bayarea/article/Cal...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2#California, United States#US#USCA#36.17#-119...</td>
      <td>...</td>
      <td>wc:64,c12.1:2,c12.10:3,c12.12:2,c12.13:1,c12.1...</td>
      <td>http://ww4.hdnux.com/photos/51/33/25/10859887/...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Obdulia Salinas,158</td>
      <td>58000000,When Obdulia Salinas is,100;35,grandc...</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Kurtis Alexander&lt;/PAGE_AUTHORS&gt;&lt;...</td>
    </tr>
    <tr>
      <th>23</th>
      <td>20160901234500-23</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>medgadget.com</td>
      <td>http://www.medgadget.com/2016/09/medtronics-en...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>WB_1156_MONITORING_AND_EVALUATION_SYSTEMS;WB_6...</td>
      <td>WB_1156_MONITORING_AND_EVALUATION_SYSTEMS,89;W...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:132,c12.1:4,c12.10:18,c12.12:7,c12.13:6,c12...</td>
      <td>http://www.medgadget.com/wp-content/uploads/20...</td>
      <td>https://2nznub4x5d61ra4q12fyu67t-wpengine.netd...</td>
      <td>NaN</td>
      <td>https://youtube.com/embed/pL3BnwCHw_8?feature=...</td>
      <td>NaN</td>
      <td>Enlite Sensor Approved,43;Glucose Monitoring,84</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;https://www.facebook.com/Medgadg...</td>
    </tr>
    <tr>
      <th>24</th>
      <td>20160901234500-24</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>ruidosonews.com</td>
      <td>http://www.ruidosonews.com/story/news/2016/09/...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MEDIA_SOCIAL;TRIAL;RAPE;TAX_FNCACT;TAX_FNCACT_...</td>
      <td>TAX_FNCACT_PROVOST,5311;TAX_FNCACT_WOMAN,113;M...</td>
      <td>1#United States#US#US#38#-97#US;2#Ohio, United...</td>
      <td>...</td>
      <td>wc:853,c1.3:1,c12.1:84,c12.10:92,c12.12:37,c12...</td>
      <td>http://www.gannett-cdn.com/-mm-/cdeb01ccaa11ff...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5263|122||We definitely need to be doing some ...</td>
      <td>Santa Clara County,423;Assemblymember Bill Dod...</td>
      <td>48,CONNECT TWEET LINKEDIN 19,2;19,COMMENTEMAIL...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.retainjudgepersky.com/&lt;...</td>
    </tr>
    <tr>
      <th>25</th>
      <td>20160901234500-25</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>630wpro.com</td>
      <td>http://www.630wpro.com/news/zika-found-in-mosq...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_DISEASE;TAX_DISEASE_ZIKA;TAX_DISEASE_ZIKA_...</td>
      <td>TAX_DISEASE_ZIKA,41;TAX_FNCACT_COMMISSIONER,58...</td>
      <td>1#United States#US#US#38#-97#US;2#Florida, Uni...</td>
      <td>...</td>
      <td>wc:97,c12.1:4,c12.10:2,c12.12:1,c12.14:1,c12.3...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Miami Beach,89;Florida Department,117;Consumer...</td>
      <td>3,mosquito samples,225;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>26</th>
      <td>20160901234500-26</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>newyorkstatesman.com</td>
      <td>http://www.newyorkstatesman.com/index.php/sid/...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>SCANDAL;TAX_FNCACT;TAX_FNCACT_STATESMAN;LEADER...</td>
      <td>SCANDAL,52;SCANDAL,126;SCANDAL,198;LEADER,145;...</td>
      <td>2#New York, United States#US#USNY#42.1497#-74....</td>
      <td>...</td>
      <td>wc:152,c1.1:1,c12.1:11,c12.10:9,c12.12:6,c12.1...</td>
      <td>http://static.midwestradionetwork.com/story_lo...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Anthony Weiner,38;Anthony Weiner,114;Anthony W...</td>
      <td>28,at the UB Center,656;1,performances by the ...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>27</th>
      <td>20160901234500-27</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>timesofisrael.com</td>
      <td>http://jewishstandard.timesofisrael.com/israel...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>WB_286_TELECOMMUNICATIONS_AND_BROADBAND_ACCESS...</td>
      <td>MEDIA_SOCIAL,834;MEDIA_SOCIAL,957;MEDIA_SOCIAL...</td>
      <td>2#Florida, United States#US#USFL#27.8333#-81.7...</td>
      <td>...</td>
      <td>wc:282,c12.1:10,c12.10:15,c12.12:6,c12.13:7,c1...</td>
      <td>http://cdn.timesofisrael.com/uploads/2016/09/r...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Cape Canaveral,130;Associated Press,416;Israel...</td>
      <td>6,satellite,532;300000000,dollars ,987;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.jta.org/2015/10/06/news...</td>
    </tr>
    <tr>
      <th>28</th>
      <td>20160901234500-28</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>newsbusters.org</td>
      <td>http://www.newsbusters.org/blogs/nb/matthew-ba...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>LEGALIZE;LGBT;UNGP_FREEDOM_FROM_DISCRIMINATION...</td>
      <td>CRISISLEX_CRISISLEXREC,1066;LEGALIZE,214;TAX_E...</td>
      <td>1#United States#US#US#38#-97#US</td>
      <td>...</td>
      <td>wc:252,c12.1:31,c12.10:14,c12.13:3,c12.14:11,c...</td>
      <td>http://cdn.newsbusters.org/images/2016-09-01-m...</td>
      <td>http://cdn.newsbusters.org/styles/author/s3/pi...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Supreme Court,219;Supreme Court,540;Tamron Hal...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.msnbc.com/msnbc/watch/t...</td>
    </tr>
    <tr>
      <th>29</th>
      <td>20160901234500-29</td>
      <td>20160901234500</td>
      <td>1</td>
      <td>irishsun.com</td>
      <td>http://www.irishsun.com/index.php/sid/247281507</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_FNCACT;TAX_FNCACT_BOXER;GENERAL_GOVERNMENT...</td>
      <td>GENERAL_GOVERNMENT,54;GENERAL_GOVERNMENT,164;G...</td>
      <td>1#Ireland#EI#EI#53#-8#EI;4#Dublin, Dublin, Ire...</td>
      <td>...</td>
      <td>wc:154,c12.1:10,c12.10:22,c12.12:4,c12.13:4,c1...</td>
      <td>http://static.midwestradionetwork.com/story_lo...</td>
      <td>NaN</td>
      <td>http://pic.twitter.com/FWG3xVeVYc;</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Boxer' Moran,20;Boxer' Moran,135;Independent A...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
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
      <th>76917</th>
      <td>20160924163000-2278</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>philstar.com</td>
      <td>http://www.philstar.com/cebu-lifestyle/2016/09...</td>
      <td>AFFECT#4000000##1#Philippines#RP#RP#13#122#RP;...</td>
      <td>AFFECT#4000000##1#Philippines#RP#RP#13#122#RP#...</td>
      <td>TAX_WORLDMAMMALS;TAX_WORLDMAMMALS_HUMAN;AFFECT...</td>
      <td>MEDIA_SOCIAL,1813;TAX_AIDGROUPS_HABITAT_FOR_HU...</td>
      <td>4#Bantayan Island, Cebu, Philippines#RP#RP21#1...</td>
      <td>...</td>
      <td>wc:287,c1.3:6,c12.1:21,c12.10:35,c12.12:9,c12....</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Saison Dampios,58;Updated September,106;Bantay...</td>
      <td>1000000,living,289;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.facebook.com/habitatphi...</td>
    </tr>
    <tr>
      <th>76918</th>
      <td>20160924163000-2279</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>wltx.com</td>
      <td>http://www.wltx.com/news/crime/police-charge-o...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_FNCACT;TAX_FNCACT_OFFICER;SECURITY_SERVICE...</td>
      <td>GENERAL_GOVERNMENT,627;EPU_POLICY_GOVERNMENT,6...</td>
      <td>2#Georgia, United States#US#USGA#32.9866#-83.6...</td>
      <td>...</td>
      <td>wc:279,c12.1:15,c12.10:18,c12.12:10,c12.13:6,c...</td>
      <td>http://content.11alive.com/photo/2016/09/13/Z_...</td>
      <td>http://content.11alive.com/photo/2016/09/13/Z_...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Sherry Hall,249;Georgia Bureau,509;Scott Dutto...</td>
      <td>600,work hours were spent,723;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.11alive.com/news/local/...</td>
    </tr>
    <tr>
      <th>76919</th>
      <td>20160924163000-2280</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>muscatinejournal.com</td>
      <td>http://muscatinejournal.com/news/state-and-reg...</td>
      <td>KILL#2000000#bees#2#South Carolina, United Sta...</td>
      <td>KILL#2000000#bees#2#South Carolina, United Sta...</td>
      <td>AGRICULTURE;TAX_WORLDINSECTS;TAX_WORLDINSECTS_...</td>
      <td>WB_178_PEST_MANAGEMENT,1038;WB_174_CROP_PRODUC...</td>
      <td>3#Willow Creek, Wisconsin, United States#US#US...</td>
      <td>...</td>
      <td>wc:805,c12.1:50,c12.10:95,c12.11:1,c12.12:30,c...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Bill Johnson,123;Johnson Honey Farm,188;Telegr...</td>
      <td>1000000,of bees,1021;60,pounds of surplus hone...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://bit.ly/2dexRBK;http://www.t...</td>
    </tr>
    <tr>
      <th>76920</th>
      <td>20160924163000-2281</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>edp24.co.uk</td>
      <td>http://www.edp24.co.uk:80/news/politics/jeremy...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>USPEC_POLITICS_GENERAL1;TAX_FNCACT;TAX_FNCACT_...</td>
      <td>GENERAL_GOVERNMENT,1750;GENERAL_GOVERNMENT,203...</td>
      <td>4#Islington, Islington, United Kingdom#UK#UKG3...</td>
      <td>...</td>
      <td>wc:882,c1.1:1,c1.3:1,c12.1:72,c12.10:71,c12.12...</td>
      <td>http://www.edp24.co.uk:80/polopoly_fs/1.471008...</td>
      <td>http://edition.pagesuite-professional.co.uk/ge...</td>
      <td>NaN</td>
      <td>https://youtube.com/user/EDP24TV;</td>
      <td>855|29||passionate and often partisan#996|104|...</td>
      <td>Jeremy Corbyn,14;Owen Smith,211;Jeremy Corbyn,...</td>
      <td>1000000,votes cast,419;209,votes was more than...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.edp24.co.uk:80/topic/Or...</td>
    </tr>
    <tr>
      <th>76921</th>
      <td>20160924163000-2282</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>durangoherald.com</td>
      <td>http://www.durangoherald.com/article/20160920/...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>PUBLIC_TRANSPORT;TAX_FNCACT;TAX_FNCACT_RAILROA...</td>
      <td>WB_2937_SILVER,300;WB_507_ENERGY_AND_EXTRACTIV...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:111,c12.1:7,c12.10:9,c12.12:5,c12.13:1,c12....</td>
      <td>http://durangoherald.com/storyimage/DU/2016092...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Article Last Updated,21;Silver San Juan Divisi...</td>
      <td>1000000,A sound decoder,50;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>76922</th>
      <td>20160924163000-2283</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>boorowanewsonline.com.au</td>
      <td>http://www.boorowanewsonline.com.au/story/4186...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_RELIGION;TAX_RELIGION_CHRISTIAN;TAX_ETHNIC...</td>
      <td>BAN,1992;WB_2386_BROADCASTING_POLICY_AND_STRAT...</td>
      <td>4#Perth, Western Australia, Australia#AS#AS08#...</td>
      <td>...</td>
      <td>wc:402,c1.1:1,c1.3:1,c12.1:18,c12.10:35,c12.12...</td>
      <td>http://nnimgt-a.akamaihd.net/transform/v1/crop...</td>
      <td>NaN</td>
      <td>http://instagram.com/p/BKW7XCmj3_l;</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Channel Nine,44;Christian Wilkins,91;Kara Wils...</td>
      <td>9,Willoughby bunker,37;7,rival #xC2,727;9,tale...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;https://www.instagram.com/channel9...</td>
    </tr>
    <tr>
      <th>76923</th>
      <td>20160924163000-2284</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>centralwesterndaily.com.au</td>
      <td>http://www.centralwesterndaily.com.au/story/41...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_ETHNICITY;TAX_ETHNICITY_ITALIAN;TAX_WORLDL...</td>
      <td>GENERAL_GOVERNMENT,1852;EPU_POLICY_GOVERNMENT,...</td>
      <td>1#Australia#AS#AS#-27#133#AS;4#Leichhardt, New...</td>
      <td>...</td>
      <td>wc:722,c1.2:2,c12.1:47,c12.10:66,c12.11:1,c12....</td>
      <td>http://nnimgt-a.akamaihd.net/transform/v1/crop...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3943|169||what we refer to as the push down ef...</td>
      <td>Nicholas Quaratiello,61;Italian Forum,132;Viol...</td>
      <td>9000000,on Friday,7;2,Potato,478;2000000,stude...</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Eryk Bagshaw;Kelsey Munro;Austra...</td>
    </tr>
    <tr>
      <th>76924</th>
      <td>20160924163000-2285</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>khak.com</td>
      <td>http://khak.com/tags/ole-lena-win-a-cruise/</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MEDIA_SOCIAL;</td>
      <td>MEDIA_SOCIAL,423;MEDIA_SOCIAL,1113;</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:213,c1.2:2,c12.1:14,c12.10:16,c12.12:3,c12....</td>
      <td>http://wac.450F.edgecastcdn.net/80450F/khak.co...</td>
      <td>http://kdat.com/files/2015/01/usdxkyxtmegsdxjr...</td>
      <td>NaN</td>
      <td>https://youtube.com/channel/;https://youtube.c...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://khak.com;http://khak.com/ta...</td>
    </tr>
    <tr>
      <th>76925</th>
      <td>20160924163000-2286</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>icenews.is</td>
      <td>http://www.icenews.is/2011/06/21/icelandic-lan...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_WORLDLANGUAGES;TAX_WORLDLANGUAGES_ICELANDI...</td>
      <td>GENERAL_GOVERNMENT,554;EPU_POLICY_GOVERNMENT,5...</td>
      <td>4#Hverfjall, NorðAnd Eystra, Iceland#IC#IC40#6...</td>
      <td>...</td>
      <td>wc:99,c1.4:1,c12.1:8,c12.10:6,c12.13:2,c12.14:...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://youtube.com/watch?v=dw_T9pJ728U&lt;/a;htt...</td>
      <td>NaN</td>
      <td>Famous Icelandic,18;Lake Myvatn,497</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Alex&lt;/PAGE_AUTHORS&gt;</td>
    </tr>
    <tr>
      <th>76926</th>
      <td>20160924163000-2287</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>stuff.co.nz</td>
      <td>http://www.stuff.co.nz/world/americas/84592131...</td>
      <td>KILL#1##1#United States#US#US#38#-97#US;CRISIS...</td>
      <td>KILL#1##1#United States#US#US#38#-97#US#118;CR...</td>
      <td>AFFECT;REFUGEES;EPU_CATS_MIGRATION_FEAR_MIGRAT...</td>
      <td>WB_2467_TERRORISM,1876;WB_2433_CONFLICT_AND_VI...</td>
      <td>1#United States#US#US#38#-97#US;1#Australia#AS...</td>
      <td>...</td>
      <td>wc:508,c1.2:1,c1.3:1,c12.1:62,c12.10:57,c12.12...</td>
      <td>http://www.stuff.co.nz/content/dam/images/1/e/...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Cato Institute,143;Donald Trump,1456;Pauline H...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.stuff.co.nz/world/ameri...</td>
    </tr>
    <tr>
      <th>76927</th>
      <td>20160924163000-2288</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>bereamail.co.za</td>
      <td>http://bereamail.co.za/93570/zulus-celebrate-r...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_ETHNICITY;TAX_ETHNICITY_ZULUS;TAX_ETHNICIT...</td>
      <td>TAX_ETHNICITY_ZULUS,6;UNGP_FORESTS_RIVERS_OCEA...</td>
      <td>4#Berea, ?Alab, Syria#SY#SY09#36.2028#37.1586#...</td>
      <td>...</td>
      <td>wc:270,c1.4:7,c12.1:25,c12.10:9,c12.12:2,c12.1...</td>
      <td>http://bereamail.co.za/wp-content/uploads/site...</td>
      <td>http://bereamail.co.za/wp-content/themes/caxto...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>South Africa,35;Umkhosi WeLembe,90;South Afric...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Lorna Charles;Springs Advertiser...</td>
    </tr>
    <tr>
      <th>76928</th>
      <td>20160924163000-2289</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>turnto10.com</td>
      <td>http://turnto10.com/news/local/new-bedford-fir...</td>
      <td>AFFECT#14##0######;POVERTY#14##0######;CRISISL...</td>
      <td>AFFECT#14##0#######0;POVERTY#14##0#######0;CRI...</td>
      <td>AFFECT;POVERTY;CRISISLEX_C05_NEED_OF_SHELTERS;...</td>
      <td>DISASTER_FIRE,62;CRISISLEX_T01_CAUTION_ADVICE,...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:85,c12.1:2,c12.10:9,c12.12:7,c12.13:2,c12.3...</td>
      <td>http://static-24.sinclairstoryline.com/resourc...</td>
      <td>http://static-24.sinclairstoryline.com/resourc...</td>
      <td>NaN</td>
      <td>https://youtube.com/user/wjar10;</td>
      <td>NaN</td>
      <td>New Bedford,385;Rodney French,417</td>
      <td>14,people,9;3,story house,70;29,Salisbury Stre...</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Richard Couto&lt;/PAGE_AUTHORS&gt;&lt;PAG...</td>
    </tr>
    <tr>
      <th>76929</th>
      <td>20160924163000-2290</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>mouthshut.com</td>
      <td>http://www.mouthshut.com/review/Asus-Zenfone-5...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_ECON_PRICE;</td>
      <td>TAX_ECON_PRICE,691;</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:136,c12.1:8,c12.10:11,c12.12:4,c12.13:5,c12...</td>
      <td>http://image3.mouthshut.com/images/imagesp/l/9...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5,is my 2nd android,22;1,prob occer u have,217...</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;imrankhan2151&lt;/PAGE_AUTHORS&gt;&lt;PAG...</td>
    </tr>
    <tr>
      <th>76930</th>
      <td>20160924163000-2291</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>turnto23.com</td>
      <td>http://www.turnto23.com/news/national/terroris...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TRAFFIC;TAX_FNCACT;TAX_FNCACT_MAN;CRISISLEX_CR...</td>
      <td>TAX_FNCACT_GUIDE,3963;BORDER,2142;SOC_SUICIDE,...</td>
      <td>2#Arizona, United States#US#USAZ#33.7712#-111....</td>
      <td>...</td>
      <td>wc:911,c12.1:66,c12.10:93,c12.12:25,c12.13:47,...</td>
      <td>NaN</td>
      <td>http://media2.scrippsnationalnews.com/image/st...</td>
      <td>NaN</td>
      <td>https://youtube.com/23ABCNews;</td>
      <td>NaN</td>
      <td>Ahmad Khan Rahami,790;Associated Press,1846;Bo...</td>
      <td>10,months,4020;2,gunmen who attempted an,4473;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.turnto23.com/news/natio...</td>
    </tr>
    <tr>
      <th>76931</th>
      <td>20160924163000-2292</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>seattletimes.com</td>
      <td>http://www.seattletimes.com/nation-world/the-l...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_FNCACT;TAX_FNCACT_MINISTER;TAX_FNCACT_FORE...</td>
      <td>GENERAL_GOVERNMENT,512;EPU_POLICY_GOVERNMENT,5...</td>
      <td>1#Syria#SY#SY#35#38#SY;1#Lebanon#LE#LE#33.8333...</td>
      <td>...</td>
      <td>wc:140,c12.1:11,c12.10:14,c12.12:8,c12.13:2,c1...</td>
      <td>http://www.seattletimes.com/wp-content/themes/...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>224|52||is making great strides in its war aga...</td>
      <td>President Bashar Assad,510;Islamic State,981</td>
      <td>2,parallel tracks,532;</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;The Associated Press&lt;/PAGE_AUTHO...</td>
    </tr>
    <tr>
      <th>76932</th>
      <td>20160924163000-2293</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>ghanastar.com</td>
      <td>https://www.ghanastar.com/news/dr-mary-grants-...</td>
      <td>KILL#88##1#Ghana#GH#GH#8#-2#GH;CRISISLEX_T03_D...</td>
      <td>KILL#88##1#Ghana#GH#GH#8#-2#GH#394;CRISISLEX_T...</td>
      <td>EPU_POLICY;EPU_POLICY_POLITICAL;GENERAL_HEALTH...</td>
      <td>GENERAL_GOVERNMENT,905;GENERAL_GOVERNMENT,2755...</td>
      <td>1#Ghana#GH#GH#8#-2#GH</td>
      <td>...</td>
      <td>wc:667,c12.1:63,c12.10:61,c12.12:12,c12.13:25,...</td>
      <td>https://www.ghanastar.com/wp-content/uploads/2...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>https://youtube.com/channel/UCRhFrw1P0o5jvd4oa...</td>
      <td>4101|63||wise and forthright counsel as a memb...</td>
      <td>Provisional National Defence Council,318;Newsf...</td>
      <td>2,main political parties,81;37,Military Hospit...</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Victor Owusu-Bediako&lt;/PAGE_AUTHO...</td>
    </tr>
    <tr>
      <th>76933</th>
      <td>20160924163000-2294</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>oigel.com</td>
      <td>http://oigel.com/xiaomi-mi-band-2-specs-featur...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1#China#CH#CH#35#105#CH;1#India#IN#IN#20#77#IN</td>
      <td>...</td>
      <td>wc:244,c12.1:17,c12.10:13,c12.13:4,c12.14:9,c1...</td>
      <td>http://cdn.isvisible.com/2016/09/Xiaomi-Mi-Ban...</td>
      <td>http://cdn.isvisible.com/2016/07/logo-nav.png</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Xiaomi Mi Band,45;Xiaomi Mi Band,1370</td>
      <td>2,Specifications Features,288;2,sports a 0 42-...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://oigel.com/tag/miband2;http:...</td>
    </tr>
    <tr>
      <th>76934</th>
      <td>20160924163000-2295</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>westport-news.com</td>
      <td>http://www.westport-news.com/news/politics/art...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2#New York, United States#US#USNY#42.1497#-74....</td>
      <td>...</td>
      <td>wc:593,c12.1:60,c12.10:56,c12.12:20,c12.13:21,...</td>
      <td>http://ww2.hdnux.com/photos/51/71/12/10982029/...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Donald Trump,88;New York,183;Brett O'Donnell,5...</td>
      <td>16,mock debates,1420;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.westport-news.com/searc...</td>
    </tr>
    <tr>
      <th>76935</th>
      <td>20160924163000-2296</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>ecolocalizer.com</td>
      <td>http://ecolocalizer.com/2016/09/24/green-econo...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>USPEC_POLICY1;EPU_ECONOMY;EPU_ECONOMY_HISTORIC...</td>
      <td>WB_678_DIGITAL_GOVERNMENT,3097;WB_667_ICT_INFR...</td>
      <td>2#Rhode Island, United States#US#USRI#41.6772#...</td>
      <td>...</td>
      <td>wc:543,c1.2:11,c1.3:7,c12.1:20,c12.10:51,c12.1...</td>
      <td>http://ecolocalizer.com/wp-content/uploads/201...</td>
      <td>http://reyr6216d262cozsk3t8r171b6y.wpengine.ne...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Green Economy Bond,167;Green Economy Bond,448;...</td>
      <td>35000000,dollars ,162;25,Rhode Island nonprofi...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://ecolocalizer.com/author/car...</td>
    </tr>
    <tr>
      <th>76936</th>
      <td>20160924163000-2297</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>iheart.com</td>
      <td>http://power107.iheart.com/articles/weird-news...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2#Arizona, United States#US#USAZ#33.7712#-111....</td>
      <td>...</td>
      <td>wc:125,c12.1:8,c12.10:12,c12.12:5,c12.13:6,c12...</td>
      <td>http://i.iheart.com/v3/url/aHR0cDovL2NvbnRlbnQ...</td>
      <td>http://content.clearchannel.com/cc-common/mlib...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Digital Homicide Studios,260;Arizona Republic,...</td>
      <td>100,players for up,337;18000000,dollars for ch...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.azcentral.com/story/mon...</td>
    </tr>
    <tr>
      <th>76937</th>
      <td>20160924163000-2298</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>iheart.com</td>
      <td>http://kix961.iheart.com/onair/bobby-bones-207...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:189,c12.1:9,c12.10:14,c12.12:3,c12.13:6,c12...</td>
      <td>http://i.iheart.com/v3/url/aHR0cDovL2NvbnRlbnQ...</td>
      <td>http://i.iheart.com/v3/url/aHR0cDovL2NvbnRlbnQ...</td>
      <td>http://instagram.com/p/BKuIHQdjKgy;http://inst...</td>
      <td>https://youtube.com/embed/XfUWRSjSPKE;</td>
      <td>NaN</td>
      <td>Billy Idol,140;Sam Hunt,154;Miley Cyrus,171;Bo...</td>
      <td>17,hosting late night,215;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.facebook.com/pages/Bobb...</td>
    </tr>
    <tr>
      <th>76938</th>
      <td>20160924163000-2299</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>kekbfm.com</td>
      <td>http://kekbfm.com/keyes-field-trip-to-the-dino...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:94,c1.1:2,c1.4:2,c12.1:14,c12.10:6,c12.12:1...</td>
      <td>http://wac.450F.edgecastcdn.net/80450F/kekbfm....</td>
      <td>http://wac.450F.edgecastcdn.net/80450F/kekbfm....</td>
      <td>NaN</td>
      <td>https://youtube.com/channel/;https://youtube.c...</td>
      <td>NaN</td>
      <td>Dinosaur Museum,48</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;keyes&lt;/PAGE_AUTHORS&gt;</td>
    </tr>
    <tr>
      <th>76939</th>
      <td>20160924163000-2300</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>iheart.com</td>
      <td>http://power107.iheart.com/articles/trending-1...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ELECTION;MANMADE_DISASTER_IMPLIED;CRISISLEX_T1...</td>
      <td>MANMADE_DISASTER_IMPLIED,328;MANMADE_DISASTER_...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:308,c1.1:1,c12.1:21,c12.10:26,c12.12:5,c12....</td>
      <td>http://i.iheart.com/v3/url/aHR0cDovL2kuaWhlYXJ...</td>
      <td>http://i.iheart.com/v3/re/new_assets/57e61ee33...</td>
      <td>http://pic.twitter.com/X7XcCCb9RY;http://pic.t...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>HeartRadio Music Festival Friday,140;Jamie Fox...</td>
      <td>16,just right at the,63;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://news.iheart.com/features/ih...</td>
    </tr>
    <tr>
      <th>76940</th>
      <td>20160924163000-2301</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>ausbt.com.au</td>
      <td>http://www.ausbt.com.au/community/view/18/5214...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>WB_2936_GOLD;WB_507_ENERGY_AND_EXTRACTIVES;WB_...</td>
      <td>SOC_POINTSOFINTEREST_AIRPORTS,671;WB_135_TRANS...</td>
      <td>4#Sao Paulo, SãPaulo, Brazil#BR#BR27#-23.5333#...</td>
      <td>...</td>
      <td>wc:442,c1.2:3,c12.1:30,c12.10:31,c12.12:5,c12....</td>
      <td>http://media.ausbt.com.au/260,210-ausbt.png</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1793|38||I'm VA Gold , do I get lounge access?</td>
      <td>Erin Beck,13;Velocity Gold,84;Singapore AirJoi...</td>
      <td>12,AMLounge access for Velocity,27;32,AMwww au...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.ausbt.com.au/forums/use...</td>
    </tr>
    <tr>
      <th>76941</th>
      <td>20160924163000-2302</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>somersetcountygazette.co.uk</td>
      <td>http://www.somersetcountygazette.co.uk/news/na...</td>
      <td>ARREST#3#suspected migrants#4#English Channel,...</td>
      <td>ARREST#3#suspected migrants#4#English Channel,...</td>
      <td>TAX_ETHNICITY;TAX_ETHNICITY_ENGLISH;TAX_WORLDL...</td>
      <td>SOC_POINTSOFINTEREST_JAIL,632;TAX_ETHNICITY_EN...</td>
      <td>4#English Channel, United Kingdom (General), U...</td>
      <td>...</td>
      <td>wc:202,c12.1:6,c12.10:11,c12.12:4,c12.13:1,c12...</td>
      <td>http://www.somersetcountygazette.co.uk/resourc...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>English Channel,82;Kent Police,241;Kingsdown R...</td>
      <td>3,suspected migrants were detained,78;3,men we...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>76942</th>
      <td>20160924163000-2303</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>yahoo.com</td>
      <td>https://www.yahoo.com/news/17-cats-definitely-...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TAX_WORLDMAMMALS;TAX_WORLDMAMMALS_CATS;GENERAL...</td>
      <td>CRISISLEX_CRISISLEXREC,239;CRISISLEX_CRISISLEX...</td>
      <td>NaN</td>
      <td>...</td>
      <td>wc:62,c12.1:11,c12.10:16,c12.12:8,c12.13:7,c12...</td>
      <td>https://s.yimg.com/uu/api/res/1.2/g3K3P02dX91_...</td>
      <td>https://s.yimg.com/uu/api/res/1.2/g3K3P02dX91_...</td>
      <td>NaN</td>
      <td>https://youtube.com/embed/bi6rKIYYA20?enablejs...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://mashable.com/2016/09/19/hea...</td>
    </tr>
    <tr>
      <th>76943</th>
      <td>20160924163000-2304</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>alltechnews.org</td>
      <td>http://alltechnews.org/2016/09/24/u-s-lifts-my...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1#Myanmar#BM#BM#22#98#BM;2#Arkansas, United St...</td>
      <td>...</td>
      <td>wc:1347,c1.1:2,c1.2:8,c1.3:3,c1.4:1,c12.1:81,c...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>486|63||Domestically , it will also mean more ...</td>
      <td>United Nations,218;Suu Kyi,330;North Korea,592...</td>
      <td>135,ethnic groups,278;2,nations closely,3274;3...</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;;http://abcnews.go.com/topics/news...</td>
    </tr>
    <tr>
      <th>76944</th>
      <td>20160924163000-2305</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>romseyadvertiser.co.uk</td>
      <td>http://www.romseyadvertiser.co.uk/news/nationa...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>TRIAL;SOC_GENERALCRIME;SECURITY_SERVICES;TAX_F...</td>
      <td>TAX_FNCACT_MAGISTRATES,841;TAX_FNCACT_MAGISTRA...</td>
      <td>4#West Midlands, United Kingdom (General), Uni...</td>
      <td>...</td>
      <td>wc:230,c12.1:9,c12.10:8,c12.12:5,c12.13:3,c12....</td>
      <td>http://www.romseyadvertiser.co.uk/resources/im...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>United Kingdom,90;Intu Potteries Shopping,402;...</td>
      <td>5,men have been charged,4;5,men charged,424;5,...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>76945</th>
      <td>20160924163000-2306</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>margaretrivermail.com.au</td>
      <td>http://www.margaretrivermail.com.au/story/4186...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>USPEC_POLITICS_GENERAL1;TAX_POLITICAL_PARTY;TA...</td>
      <td>UNGP_FORESTS_RIVERS_OCEANS,1971;TAX_FNCACT_PRI...</td>
      <td>1#Australia#AS#AS#-27#133#AS;4#Sydney, New Sou...</td>
      <td>...</td>
      <td>wc:490,c1.4:3,c12.1:40,c12.10:64,c12.12:15,c12...</td>
      <td>http://nnimgt-a.akamaihd.net/transform/v1/crop...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>335|55||Children are our greatest treasure. Th...</td>
      <td>Nelson Mandela Foundation,30;Liberal Party,59;...</td>
      <td>3,directors of the group,416;9,of the Bill of,...</td>
      <td>NaN</td>
      <td>&lt;PAGE_AUTHORS&gt;Adam Gartrell;National Political...</td>
    </tr>
    <tr>
      <th>76946</th>
      <td>20160924163000-2307</td>
      <td>20160924163000</td>
      <td>1</td>
      <td>myndnow.com</td>
      <td>http://www.myndnow.com/news/clinton-ally-playi...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>EPU_CATS_REGULATION;WB_678_DIGITAL_GOVERNMENT;...</td>
      <td>TAX_FNCACT_CANDIDATES,1526;TAX_RELIGION_SHAKER...</td>
      <td>2#New York, United States#US#USNY#42.1497#-74....</td>
      <td>...</td>
      <td>wc:323,c12.1:44,c12.10:26,c12.12:10,c12.13:8,c...</td>
      <td>http://static.lakana.com/nxsglobal/feedsite/ph...</td>
      <td>http://s3.amazonaws.com/nxsglobal/myndnow/them...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Jeff Zeleny,134;Eugene Scott,151;Turner Broadc...</td>
      <td>2,people familiar with the,329;</td>
      <td>NaN</td>
      <td>&lt;PAGE_LINKS&gt;http://www.myndnow.com/about-us/me...</td>
    </tr>
  </tbody>
</table>
<p>76947 rows × 27 columns</p>
</div>




```python
datesToPull
```




    ['20160901234500',
     '20160902234500',
     '20160903234500',
     '20160904234500',
     '20160905234500',
     '20160906234500',
     '20160907234500',
     '20160908234500',
     '20160909234500',
     '20160910234500',
     '20160911234500',
     '20160912234500',
     '20160913234500',
     '20160914234500',
     '20160915234500',
     '20160916234500',
     '20160917234500',
     '20160918234500',
     '20160919234500',
     '20160920234500',
     '20160921234500',
     '20160922234500',
     '20160923234500',
     '20160924153000']



*****************

## Munging Data: Extracting Specific Datasets or all of them

Work with the returned GDELT data.  Specific whether we are pulling the `mentions`, `events`, or `gkg` date for the day or all.  


```python
results = match_date(gdelt_timeString(dateInputCheck(date)))
```


```python
target = results[2][results[2].str.contains('export')].reset_index(drop=True).ix[0]
```


```python
target
```




    'http://data.gdeltproject.org/gdeltv2/20160924150000.export.CSV.zip'




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
target
```




    'http://data.gdeltproject.org/gdeltv2/20160924150000.export.CSV.zip'




```python
gdelt_df = downloadAndExtract(target)
gdelt_df.columns = add_header(target)
gdelt_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1362 entries, 0 to 1361
    Data columns (total 61 columns):
    GLOBALEVENTID            1362 non-null int64
    SQLDATE                  1362 non-null int64
    MonthYear                1362 non-null int64
    Year                     1362 non-null int64
    FractionDate             1362 non-null float64
    Actor1Code               1245 non-null object
    Actor1Name               1245 non-null object
    Actor1CountryCode        803 non-null object
    Actor1KnownGroupCode     24 non-null object
    Actor1EthnicCode         4 non-null object
    Actor1Religion1Code      28 non-null object
    Actor1Religion2Code      8 non-null object
    Actor1Type1Code          621 non-null object
    Actor1Type2Code          45 non-null object
    Actor1Type3Code          1 non-null object
    Actor2Code               1016 non-null object
    Actor2Name               1016 non-null object
    Actor2CountryCode        635 non-null object
    Actor2KnownGroupCode     21 non-null object
    Actor2EthnicCode         8 non-null object
    Actor2Religion1Code      56 non-null object
    Actor2Religion2Code      5 non-null object
    Actor2Type1Code          484 non-null object
    Actor2Type2Code          27 non-null object
    Actor2Type3Code          0 non-null float64
    IsRootEvent              1362 non-null int64
    EventCode                1362 non-null int64
    EventBaseCode            1362 non-null int64
    EventRootCode            1362 non-null int64
    QuadClass                1362 non-null int64
    GoldsteinScale           1362 non-null float64
    NumMentions              1362 non-null int64
    NumSources               1362 non-null int64
    NumArticles              1362 non-null int64
    AvgTone                  1362 non-null float64
    Actor1Geo_Type           1362 non-null int64
    Actor1Geo_FullName       1224 non-null object
    Actor1Geo_CountryCode    1224 non-null object
    Actor1Geo_ADM1Code       1224 non-null object
    Actor1Geo_ADM2Code       798 non-null object
    Actor1Geo_Lat            1224 non-null float64
    Actor1Geo_Long           1224 non-null float64
    Actor1Geo_FeatureID      1224 non-null object
    Actor2Geo_Type           1362 non-null int64
    Actor2Geo_FullName       997 non-null object
    Actor2Geo_CountryCode    997 non-null object
    Actor2Geo_ADM1Code       997 non-null object
    Actor2Geo_ADM2Code       594 non-null object
    Actor2Geo_Lat            997 non-null float64
    Actor2Geo_Long           997 non-null float64
    Actor2Geo_FeatureID      997 non-null object
    ActionGeo_Type           1362 non-null int64
    ActionGeo_FullName       1337 non-null object
    ActionGeo_CountryCode    1337 non-null object
    ActionGeo_ADM1Code       1337 non-null object
    ActionGeo_ADM2Code       792 non-null object
    ActionGeo_Lat            1337 non-null float64
    ActionGeo_Long           1337 non-null float64
    ActionGeo_FeatureID      1337 non-null object
    DATEADDED                1362 non-null int64
    SOURCEURL                1362 non-null object
    dtypes: float64(10), int64(16), object(35)
    memory usage: 649.1+ KB



```python
gdelt_df
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
      <th>ActionGeo_Type</th>
      <th>ActionGeo_FullName</th>
      <th>ActionGeo_CountryCode</th>
      <th>ActionGeo_ADM1Code</th>
      <th>ActionGeo_ADM2Code</th>
      <th>ActionGeo_Lat</th>
      <th>ActionGeo_Long</th>
      <th>ActionGeo_FeatureID</th>
      <th>DATEADDED</th>
      <th>SOURCEURL</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>582343584</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Jiquilillo, Chinandega, Nicaragua</td>
      <td>NU</td>
      <td>NU03</td>
      <td>22430</td>
      <td>12.731900</td>
      <td>-87.44170</td>
      <td>-1112100</td>
      <td>20160924150000</td>
      <td>http://azdailysun.com/news/local/community/fla...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>582343585</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>AFR</td>
      <td>AFRICA</td>
      <td>AFR</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Osaka, Osaka, Japan</td>
      <td>JA</td>
      <td>JA32</td>
      <td>35840</td>
      <td>34.666700</td>
      <td>135.50000</td>
      <td>-240905</td>
      <td>20160924150000</td>
      <td>http://www.whio.com/news/world/burundi-thousan...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>582343586</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>BRN</td>
      <td>BRUNEIAN</td>
      <td>BRN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Singapore</td>
      <td>SN</td>
      <td>SN</td>
      <td>NaN</td>
      <td>1.366700</td>
      <td>103.80000</td>
      <td>SN</td>
      <td>20160924150000</td>
      <td>http://health.asiaone.com/health/health-news/s...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>582343587</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>CRM</td>
      <td>TRAFFICKER</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>Indiana, United States</td>
      <td>US</td>
      <td>USIN</td>
      <td>NaN</td>
      <td>39.864700</td>
      <td>-86.26040</td>
      <td>IN</td>
      <td>20160924150000</td>
      <td>https://www.indianagazette.com/news/reg-nation...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>582343588</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>CVL</td>
      <td>COMMUNITY</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Canada</td>
      <td>CA</td>
      <td>CA</td>
      <td>NaN</td>
      <td>60.000000</td>
      <td>-95.00000</td>
      <td>CA</td>
      <td>20160924150000</td>
      <td>http://www.thecarillon.com/local/Community-can...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>582343589</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>DOM</td>
      <td>DOMINICAN REPUBLIC</td>
      <td>DOM</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Loma Miranda, Dominican Republic (general), Do...</td>
      <td>DR</td>
      <td>DR00</td>
      <td>36939</td>
      <td>19.101100</td>
      <td>-70.46460</td>
      <td>-3362810</td>
      <td>20160924150000</td>
      <td>https://www.ncronline.org/preview/mining-our-m...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>582343590</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>DOM</td>
      <td>DOMINICAN REPUBLIC</td>
      <td>DOM</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Vega Real, Duarte, Dominican Republic</td>
      <td>DR</td>
      <td>DR06</td>
      <td>36897</td>
      <td>19.250000</td>
      <td>-70.25000</td>
      <td>-3367035</td>
      <td>20160924150000</td>
      <td>https://www.ncronline.org/preview/mining-our-m...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>582343591</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>FRA</td>
      <td>FRANCE</td>
      <td>FRA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Paris, France (general), France</td>
      <td>FR</td>
      <td>FR00</td>
      <td>16282</td>
      <td>48.866700</td>
      <td>2.33333</td>
      <td>-1456928</td>
      <td>20160924150000</td>
      <td>http://ipolitics.ca/2016/09/24/can-trudeau-kee...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>582343592</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>FRA</td>
      <td>PARIS</td>
      <td>FRA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Ottawa, Ontario, Canada</td>
      <td>CA</td>
      <td>CA08</td>
      <td>12755</td>
      <td>45.416700</td>
      <td>-75.70000</td>
      <td>-570760</td>
      <td>20160924150000</td>
      <td>http://ipolitics.ca/2016/09/24/can-trudeau-kee...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>582343593</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>GOV</td>
      <td>INTERIOR MINIST</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Paris, France (general), France</td>
      <td>FR</td>
      <td>FR00</td>
      <td>16282</td>
      <td>48.866700</td>
      <td>2.33333</td>
      <td>-1456928</td>
      <td>20160924150000</td>
      <td>http://www.mfs-theothernews.com/search?updated...</td>
    </tr>
    <tr>
      <th>10</th>
      <td>582343594</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>IRNCOP</td>
      <td>IRAN</td>
      <td>IRN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Tehran, Tehran, Iran</td>
      <td>IR</td>
      <td>IR26</td>
      <td>41130</td>
      <td>35.750000</td>
      <td>51.51480</td>
      <td>10074674</td>
      <td>20160924150000</td>
      <td>http://theiranproject.com/blog/2016/09/24/iran...</td>
    </tr>
    <tr>
      <th>11</th>
      <td>582343595</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>IRNCOP</td>
      <td>IRAN</td>
      <td>IRN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Saudi Arabia</td>
      <td>SA</td>
      <td>SA</td>
      <td>NaN</td>
      <td>25.000000</td>
      <td>45.00000</td>
      <td>SA</td>
      <td>20160924150000</td>
      <td>http://theiranproject.com/blog/2016/09/24/iran...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>582343596</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>NIC</td>
      <td>NICARAGUA</td>
      <td>NIC</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Jiquilillo, Chinandega, Nicaragua</td>
      <td>NU</td>
      <td>NU03</td>
      <td>22430</td>
      <td>12.731900</td>
      <td>-87.44170</td>
      <td>-1112100</td>
      <td>20160924150000</td>
      <td>http://azdailysun.com/news/local/community/fla...</td>
    </tr>
    <tr>
      <th>13</th>
      <td>582343597</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>SGP</td>
      <td>SINGAPORE</td>
      <td>SGP</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Singapore</td>
      <td>SN</td>
      <td>SN</td>
      <td>NaN</td>
      <td>1.366700</td>
      <td>103.80000</td>
      <td>SN</td>
      <td>20160924150000</td>
      <td>http://health.asiaone.com/health/health-news/s...</td>
    </tr>
    <tr>
      <th>14</th>
      <td>582343598</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>SGP</td>
      <td>SINGAPORE</td>
      <td>SGP</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Singapore</td>
      <td>SN</td>
      <td>SN</td>
      <td>NaN</td>
      <td>1.366700</td>
      <td>103.80000</td>
      <td>SN</td>
      <td>20160924150000</td>
      <td>http://health.asiaone.com/health/health-news/s...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>582343599</td>
      <td>20150925</td>
      <td>201509</td>
      <td>2015</td>
      <td>2015.7260</td>
      <td>SGP</td>
      <td>SINGAPORE</td>
      <td>SGP</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Singapore</td>
      <td>SN</td>
      <td>SN</td>
      <td>NaN</td>
      <td>1.366700</td>
      <td>103.80000</td>
      <td>SN</td>
      <td>20160924150000</td>
      <td>http://health.asiaone.com/health/health-news/s...</td>
    </tr>
    <tr>
      <th>16</th>
      <td>582343600</td>
      <td>20160825</td>
      <td>201608</td>
      <td>2016</td>
      <td>2016.6438</td>
      <td>LEG</td>
      <td>SENATE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>3</td>
      <td>Visalia, California, United States</td>
      <td>US</td>
      <td>USCA</td>
      <td>CA107</td>
      <td>36.330200</td>
      <td>-119.29200</td>
      <td>1652807</td>
      <td>20160924150000</td>
      <td>http://www.sacbee.com/opinion/op-ed/soapbox/ar...</td>
    </tr>
    <tr>
      <th>17</th>
      <td>582343601</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>18</th>
      <td>582343602</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>BWAGOV</td>
      <td>IAN KHAMA</td>
      <td>BWA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Zimbabwe</td>
      <td>ZI</td>
      <td>ZI</td>
      <td>NaN</td>
      <td>-20.000000</td>
      <td>30.00000</td>
      <td>ZI</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/zimbabwe-...</td>
    </tr>
    <tr>
      <th>19</th>
      <td>582343603</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>CAN</td>
      <td>VANCOUVER</td>
      <td>CAN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Rideau Canal, Quebec, Canada</td>
      <td>CA</td>
      <td>CA10</td>
      <td>12755</td>
      <td>45.433300</td>
      <td>-75.70000</td>
      <td>-572256</td>
      <td>20160924150000</td>
      <td>http://ipolitics.ca/2016/09/24/leave-the-lauri...</td>
    </tr>
    <tr>
      <th>20</th>
      <td>582343604</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>COP</td>
      <td>PRISON</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>21</th>
      <td>582343605</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>COP</td>
      <td>PRISON</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>22</th>
      <td>582343606</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>COP</td>
      <td>PRISON</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>23</th>
      <td>582343607</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>COP</td>
      <td>PRISON</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>24</th>
      <td>582343608</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>COP</td>
      <td>PRISON</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>25</th>
      <td>582343609</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>COP</td>
      <td>PRISON</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>26</th>
      <td>582343610</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>GAB</td>
      <td>GABON</td>
      <td>GAB</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>27</th>
      <td>582343611</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>JUD</td>
      <td>STATE SUPREME COURT</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>Arkansas, United States</td>
      <td>US</td>
      <td>USAR</td>
      <td>NaN</td>
      <td>34.951300</td>
      <td>-92.38090</td>
      <td>AR</td>
      <td>20160924150000</td>
      <td>http://www.chron.com/news/article/Analysis-Ark...</td>
    </tr>
    <tr>
      <th>28</th>
      <td>582343612</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>LAB</td>
      <td>WORKER</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
    </tr>
    <tr>
      <th>29</th>
      <td>582343613</td>
      <td>20160917</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7041</td>
      <td>LAB</td>
      <td>WORKER</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Libreville, Estuaire, Gabon</td>
      <td>GB</td>
      <td>GB01</td>
      <td>18585</td>
      <td>0.383333</td>
      <td>9.45000</td>
      <td>-1326612</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/gabon-opp...</td>
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
      <th>1332</th>
      <td>582344916</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>USAMIL</td>
      <td>NORTH CAROLINA</td>
      <td>USA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>3</td>
      <td>Charlotte, North Carolina, United States</td>
      <td>US</td>
      <td>USNC</td>
      <td>NC119</td>
      <td>35.227100</td>
      <td>-80.84310</td>
      <td>1019610</td>
      <td>20160924150000</td>
      <td>http://hosted.ap.org/dynamic/stories/U/US_CHAR...</td>
    </tr>
    <tr>
      <th>1333</th>
      <td>582344917</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>USAMIL</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>North Carolina, United States</td>
      <td>US</td>
      <td>USNC</td>
      <td>NaN</td>
      <td>35.641100</td>
      <td>-79.84310</td>
      <td>NC</td>
      <td>20160924150000</td>
      <td>http://hosted.ap.org/dynamic/stories/U/US_CHAR...</td>
    </tr>
    <tr>
      <th>1334</th>
      <td>582344918</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>USAOPP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>3</td>
      <td>Charlotte, North Carolina, United States</td>
      <td>US</td>
      <td>USNC</td>
      <td>NC119</td>
      <td>35.227100</td>
      <td>-80.84310</td>
      <td>1019610</td>
      <td>20160924150000</td>
      <td>http://hosted.ap.org/dynamic/stories/U/US_CHAR...</td>
    </tr>
    <tr>
      <th>1335</th>
      <td>582344919</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>VAT</td>
      <td>VATICAN</td>
      <td>VAT</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Rome, Lazio, Italy</td>
      <td>IT</td>
      <td>IT07</td>
      <td>18350</td>
      <td>41.900000</td>
      <td>12.48330</td>
      <td>-126693</td>
      <td>20160924150000</td>
      <td>http://www.thetablet.co.uk/news/6169/0/francis...</td>
    </tr>
    <tr>
      <th>1336</th>
      <td>582344920</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>VNM</td>
      <td>VIETNAM</td>
      <td>VNM</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Ho Chi Minh City, H? Chíinh, Vietnam, Republic Of</td>
      <td>VM</td>
      <td>VM20</td>
      <td>74101</td>
      <td>10.750000</td>
      <td>106.66700</td>
      <td>-3730078</td>
      <td>20160924150000</td>
      <td>http://tuoitrenews.vn/post?id=37234&amp;slug=debat...</td>
    </tr>
    <tr>
      <th>1337</th>
      <td>582344921</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>YEM</td>
      <td>ADEN</td>
      <td>YEM</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>20160924150000</td>
      <td>http://www.the-star.co.ke/news/2016/09/24/jubi...</td>
    </tr>
    <tr>
      <th>1338</th>
      <td>582344922</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>YEM</td>
      <td>YEMEN</td>
      <td>YEM</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Syria</td>
      <td>SY</td>
      <td>SY</td>
      <td>NaN</td>
      <td>35.000000</td>
      <td>38.00000</td>
      <td>SY</td>
      <td>20160924150000</td>
      <td>http://www.mfs-theothernews.com/search/label/S...</td>
    </tr>
    <tr>
      <th>1339</th>
      <td>582344923</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>YEM</td>
      <td>YEMEN</td>
      <td>YEM</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Syria</td>
      <td>SY</td>
      <td>SY</td>
      <td>NaN</td>
      <td>35.000000</td>
      <td>38.00000</td>
      <td>SY</td>
      <td>20160924150000</td>
      <td>http://www.mfs-theothernews.com/search/label/S...</td>
    </tr>
    <tr>
      <th>1340</th>
      <td>582344924</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>YEMCVL</td>
      <td>YEMENI</td>
      <td>YEM</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Syria</td>
      <td>SY</td>
      <td>SY</td>
      <td>NaN</td>
      <td>35.000000</td>
      <td>38.00000</td>
      <td>SY</td>
      <td>20160924150000</td>
      <td>http://www.mfs-theothernews.com/search/label/S...</td>
    </tr>
    <tr>
      <th>1341</th>
      <td>582344925</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>YEMCVL</td>
      <td>YEMEN</td>
      <td>YEM</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Syria</td>
      <td>SY</td>
      <td>SY</td>
      <td>NaN</td>
      <td>35.000000</td>
      <td>38.00000</td>
      <td>SY</td>
      <td>20160924150000</td>
      <td>http://www.mfs-theothernews.com/search/label/S...</td>
    </tr>
    <tr>
      <th>1342</th>
      <td>582344926</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZAF</td>
      <td>JOHANNESBURG</td>
      <td>ZAF</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Mabhida, KwaZulu-Natal, South Africa</td>
      <td>SF</td>
      <td>SF02</td>
      <td>77334</td>
      <td>-28.167500</td>
      <td>31.59980</td>
      <td>-1255196</td>
      <td>20160924150000</td>
      <td>http://ewn.co.za/2016/09/24/Zuma-congratulates...</td>
    </tr>
    <tr>
      <th>1343</th>
      <td>582344927</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZAF</td>
      <td>JOHANNESBURG</td>
      <td>ZAF</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Johannesburg, Gauteng, South Africa</td>
      <td>SF</td>
      <td>SF06</td>
      <td>77364</td>
      <td>-26.200000</td>
      <td>28.08330</td>
      <td>-1240261</td>
      <td>20160924150000</td>
      <td>http://www.iol.co.za/weekend-argus/spier-murde...</td>
    </tr>
    <tr>
      <th>1344</th>
      <td>582344928</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZAF</td>
      <td>JOHANNESBURG</td>
      <td>ZAF</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Stellenbosch, Western Cape, South Africa</td>
      <td>SF</td>
      <td>SF11</td>
      <td>77338</td>
      <td>-33.934600</td>
      <td>18.86680</td>
      <td>-1287082</td>
      <td>20160924150000</td>
      <td>http://www.iol.co.za/weekend-argus/spier-murde...</td>
    </tr>
    <tr>
      <th>1345</th>
      <td>582344929</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZAF</td>
      <td>JOHANNESBURG</td>
      <td>ZAF</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Stellenbosch, Western Cape, South Africa</td>
      <td>SF</td>
      <td>SF11</td>
      <td>77338</td>
      <td>-33.934600</td>
      <td>18.86680</td>
      <td>-1287082</td>
      <td>20160924150000</td>
      <td>http://www.iol.co.za/weekend-argus/spier-murde...</td>
    </tr>
    <tr>
      <th>1346</th>
      <td>582344930</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZAF</td>
      <td>JOHANNESBURG</td>
      <td>ZAF</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Johannesburg, Gauteng, South Africa</td>
      <td>SF</td>
      <td>SF06</td>
      <td>77364</td>
      <td>-26.200000</td>
      <td>28.08330</td>
      <td>-1240261</td>
      <td>20160924150000</td>
      <td>http://www.iol.co.za/weekend-argus/spier-murde...</td>
    </tr>
    <tr>
      <th>1347</th>
      <td>582344931</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZAF</td>
      <td>JOHANNESBURG</td>
      <td>ZAF</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Durban, KwaZulu-Natal, South Africa</td>
      <td>SF</td>
      <td>SF02</td>
      <td>77363</td>
      <td>-29.850000</td>
      <td>31.01670</td>
      <td>-1224926</td>
      <td>20160924150000</td>
      <td>http://ewn.co.za/2016/09/24/Zuma-congratulates...</td>
    </tr>
    <tr>
      <th>1348</th>
      <td>582344932</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZAFGOV</td>
      <td>JOHANNESBURG</td>
      <td>ZAF</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Mabhida, KwaZulu-Natal, South Africa</td>
      <td>SF</td>
      <td>SF02</td>
      <td>77334</td>
      <td>-28.167500</td>
      <td>31.59980</td>
      <td>-1255196</td>
      <td>20160924150000</td>
      <td>http://ewn.co.za/2016/09/24/Zuma-congratulates...</td>
    </tr>
    <tr>
      <th>1349</th>
      <td>582344933</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZAFGOV</td>
      <td>JOHANNESBURG</td>
      <td>ZAF</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Durban, KwaZulu-Natal, South Africa</td>
      <td>SF</td>
      <td>SF02</td>
      <td>77363</td>
      <td>-29.850000</td>
      <td>31.01670</td>
      <td>-1224926</td>
      <td>20160924150000</td>
      <td>http://ewn.co.za/2016/09/24/Zuma-congratulates...</td>
    </tr>
    <tr>
      <th>1350</th>
      <td>582344934</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Mapungubwe, Limpopo, South Africa</td>
      <td>SF</td>
      <td>SF09</td>
      <td>77343</td>
      <td>-22.207100</td>
      <td>29.37250</td>
      <td>-1257139</td>
      <td>20160924150000</td>
      <td>http://www.timeslive.co.za/local/2016/09/24/Bu...</td>
    </tr>
    <tr>
      <th>1351</th>
      <td>582344935</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>Mapungubwe, Limpopo, South Africa</td>
      <td>SF</td>
      <td>SF09</td>
      <td>77343</td>
      <td>-22.207100</td>
      <td>29.37250</td>
      <td>-1257139</td>
      <td>20160924150000</td>
      <td>http://www.timeslive.co.za/local/2016/09/24/Bu...</td>
    </tr>
    <tr>
      <th>1352</th>
      <td>582344936</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Zimbabwe</td>
      <td>ZI</td>
      <td>ZI</td>
      <td>NaN</td>
      <td>-20.000000</td>
      <td>30.00000</td>
      <td>ZI</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/zimbabwe-...</td>
    </tr>
    <tr>
      <th>1353</th>
      <td>582344937</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Zimbabwe</td>
      <td>ZI</td>
      <td>ZI</td>
      <td>NaN</td>
      <td>-20.000000</td>
      <td>30.00000</td>
      <td>ZI</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/zimbabwe-...</td>
    </tr>
    <tr>
      <th>1354</th>
      <td>582344938</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Zimbabwe</td>
      <td>ZI</td>
      <td>ZI</td>
      <td>NaN</td>
      <td>-20.000000</td>
      <td>30.00000</td>
      <td>ZI</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/zimbabwe-...</td>
    </tr>
    <tr>
      <th>1355</th>
      <td>582344939</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZWE</td>
      <td>ZIMBABWEAN</td>
      <td>ZWE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Botswana</td>
      <td>BC</td>
      <td>BC</td>
      <td>NaN</td>
      <td>-22.000000</td>
      <td>24.00000</td>
      <td>BC</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/zimbabwe-...</td>
    </tr>
    <tr>
      <th>1356</th>
      <td>582344940</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZWEGOV</td>
      <td>ZIMBABWEAN</td>
      <td>ZWE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Zimbabwe</td>
      <td>ZI</td>
      <td>ZI</td>
      <td>NaN</td>
      <td>-20.000000</td>
      <td>30.00000</td>
      <td>ZI</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/zimbabwe-...</td>
    </tr>
    <tr>
      <th>1357</th>
      <td>582344941</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ZWEGOV</td>
      <td>ZIMBABWEAN</td>
      <td>ZWE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>Botswana</td>
      <td>BC</td>
      <td>BC</td>
      <td>NaN</td>
      <td>-22.000000</td>
      <td>24.00000</td>
      <td>BC</td>
      <td>20160924150000</td>
      <td>http://www.africanews.com/2016/09/24/zimbabwe-...</td>
    </tr>
    <tr>
      <th>1358</th>
      <td>582344942</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ijo</td>
      <td>IJAW</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ijo</td>
      <td>...</td>
      <td>4</td>
      <td>Adua, Jigawa, Nigeria</td>
      <td>NI</td>
      <td>NI39</td>
      <td>190996</td>
      <td>12.478400</td>
      <td>9.63655</td>
      <td>-1997446</td>
      <td>20160924150000</td>
      <td>http://www.ladunliadinews.com/2016/09/patience...</td>
    </tr>
    <tr>
      <th>1359</th>
      <td>582344943</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>ijo</td>
      <td>IJAW</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ijo</td>
      <td>...</td>
      <td>4</td>
      <td>Niger Delta, Nigeria (general), Nigeria</td>
      <td>NI</td>
      <td>NI00</td>
      <td>23074</td>
      <td>4.833330</td>
      <td>6.00000</td>
      <td>-2020890</td>
      <td>20160924150000</td>
      <td>http://www.ladunliadinews.com/2016/09/patience...</td>
    </tr>
    <tr>
      <th>1360</th>
      <td>582344944</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>kas</td>
      <td>KASHMIRI</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>kas</td>
      <td>...</td>
      <td>4</td>
      <td>Beijing, Beijing, China</td>
      <td>CH</td>
      <td>CH22</td>
      <td>13001</td>
      <td>39.928900</td>
      <td>116.38800</td>
      <td>-1898541</td>
      <td>20160924150000</td>
      <td>http://www.thenewsminute.com/article/china-wil...</td>
    </tr>
    <tr>
      <th>1361</th>
      <td>582344945</td>
      <td>20160924</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7233</td>
      <td>tam</td>
      <td>TAMIL</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>tam</td>
      <td>...</td>
      <td>4</td>
      <td>Bakhtiyarpur, Bihar, India</td>
      <td>IN</td>
      <td>IN34</td>
      <td>17619</td>
      <td>25.466700</td>
      <td>85.51670</td>
      <td>-2089823</td>
      <td>20160924150000</td>
      <td>http://indiatoday.intoday.in/story/tamils-stag...</td>
    </tr>
  </tbody>
</table>
<p>1362 rows × 61 columns</p>
</div>




```python
combined = gdelt_df.merge(gdelt_df2,how='outer',on='GLOBALEVENTID')
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
combined.columns
```




    Index([u'GLOBALEVENTID', u'SQLDATE', u'MonthYear', u'Year', u'FractionDate',
           u'Actor1Code', u'Actor1Name', u'Actor1CountryCode',
           u'Actor1KnownGroupCode', u'Actor1EthnicCode', u'Actor1Religion1Code',
           u'Actor1Religion2Code', u'Actor1Type1Code', u'Actor1Type2Code',
           u'Actor1Type3Code', u'Actor2Code', u'Actor2Name', u'Actor2CountryCode',
           u'Actor2KnownGroupCode', u'Actor2EthnicCode', u'Actor2Religion1Code',
           u'Actor2Religion2Code', u'Actor2Type1Code', u'Actor2Type2Code',
           u'Actor2Type3Code', u'IsRootEvent', u'EventCode', u'EventBaseCode',
           u'EventRootCode', u'QuadClass', u'GoldsteinScale', u'NumMentions',
           u'NumSources', u'NumArticles', u'AvgTone', u'Actor1Geo_Type',
           u'Actor1Geo_FullName', u'Actor1Geo_CountryCode', u'Actor1Geo_ADM1Code',
           u'Actor1Geo_ADM2Code', u'Actor1Geo_Lat', u'Actor1Geo_Long',
           u'Actor1Geo_FeatureID', u'Actor2Geo_Type', u'Actor2Geo_FullName',
           u'Actor2Geo_CountryCode', u'Actor2Geo_ADM1Code', u'Actor2Geo_ADM2Code',
           u'Actor2Geo_Lat', u'Actor2Geo_Long', u'Actor2Geo_FeatureID',
           u'ActionGeo_Type', u'ActionGeo_FullName', u'ActionGeo_CountryCode',
           u'ActionGeo_ADM1Code', u'ActionGeo_ADM2Code', u'ActionGeo_Lat',
           u'ActionGeo_Long', u'ActionGeo_FeatureID', u'DATEADDED', u'SOURCEURL',
           u'EventTimeDate', u'MentionTimeDate', u'MentionType',
           u'MentionSourceName', u'MentionIdentifier', u'SentenceID',
           u'Actor1CharOffset', u'Actor2CharOffset', u'ActionCharOffset',
           u'InRawText', u'Confidence', u'MentionDocLen', u'MentionDocTone',
           u'MentionDocTranslationInfo', u'Extras'],
          dtype='object')




```python
# combined.[(combined.Confidence != None) & (combined.MonthYear != None)]
combined[['Actor1Code','Actor1Name']][(combined.GoldsteinScale <= -5.2) & (combined.Actor1Code != "")].fillna('')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Actor1Code</th>
      <th>Actor1Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>36</th>
      <td>LBNGOV</td>
      <td>TYRE</td>
    </tr>
    <tr>
      <th>37</th>
      <td>LBNGOV</td>
      <td>TYRE</td>
    </tr>
    <tr>
      <th>46</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>55</th>
      <td>LBN</td>
      <td>TYRE</td>
    </tr>
    <tr>
      <th>56</th>
      <td>LBN</td>
      <td>TYRE</td>
    </tr>
    <tr>
      <th>67</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>81</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>111</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>137</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>138</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>151</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>152</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>159</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>160</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>206</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>207</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>231</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>232</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>234</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>279</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>281</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>282</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>283</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>284</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>285</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>290</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>291</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>297</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>299</th>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>365</th>
      <td>AUS</td>
      <td>AUSTRALIA</td>
    </tr>
    <tr>
      <th>392</th>
      <td>BRA</td>
      <td>BRAZIL</td>
    </tr>
    <tr>
      <th>448</th>
      <td>BUS</td>
      <td>BANK</td>
    </tr>
    <tr>
      <th>449</th>
      <td>BUS</td>
      <td>BANK</td>
    </tr>
    <tr>
      <th>452</th>
      <td>BUS</td>
      <td>COMPANIES</td>
    </tr>
    <tr>
      <th>458</th>
      <td>BUS</td>
      <td>AIRLINE</td>
    </tr>
    <tr>
      <th>478</th>
      <td>BUS</td>
      <td>COMPANIES</td>
    </tr>
    <tr>
      <th>505</th>
      <td>BUS</td>
      <td>COMPANIES</td>
    </tr>
    <tr>
      <th>524</th>
      <td>CAN</td>
      <td>CANADA</td>
    </tr>
    <tr>
      <th>525</th>
      <td>CAN</td>
      <td>CANADA</td>
    </tr>
    <tr>
      <th>526</th>
      <td>CAN</td>
      <td>CANADA</td>
    </tr>
    <tr>
      <th>527</th>
      <td>CAN</td>
      <td>CANADA</td>
    </tr>
    <tr>
      <th>529</th>
      <td>CAN</td>
      <td>CANADA</td>
    </tr>
    <tr>
      <th>537</th>
      <td>CAN</td>
      <td>CANADA</td>
    </tr>
    <tr>
      <th>539</th>
      <td>CAN</td>
      <td>CANADA</td>
    </tr>
    <tr>
      <th>540</th>
      <td>CAN</td>
      <td>CANADA</td>
    </tr>
    <tr>
      <th>554</th>
      <td>CHN</td>
      <td>CHINA</td>
    </tr>
    <tr>
      <th>555</th>
      <td>CHN</td>
      <td>CHINA</td>
    </tr>
    <tr>
      <th>572</th>
      <td>CHRCTH</td>
      <td>CATHOLIC</td>
    </tr>
    <tr>
      <th>573</th>
      <td>CHRCTH</td>
      <td>CATHOLIC</td>
    </tr>
    <tr>
      <th>584</th>
      <td>COG</td>
      <td>CONGO</td>
    </tr>
    <tr>
      <th>585</th>
      <td>COG</td>
      <td>CONGO</td>
    </tr>
    <tr>
      <th>608</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>609</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>610</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>615</th>
      <td>COP</td>
      <td>SECURITY FORCE</td>
    </tr>
    <tr>
      <th>616</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>617</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>619</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>627</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>640</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>641</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>647</th>
      <td>COP</td>
      <td>SECURITY FORCE</td>
    </tr>
    <tr>
      <th>649</th>
      <td>COP</td>
      <td>SECURITY FORCE</td>
    </tr>
    <tr>
      <th>670</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>671</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>672</th>
      <td>COP</td>
      <td>POLICE OFFICER</td>
    </tr>
    <tr>
      <th>673</th>
      <td>COP</td>
      <td>POLICE OFFICER</td>
    </tr>
    <tr>
      <th>674</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>675</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>676</th>
      <td>COP</td>
      <td>POLICE OFFICER</td>
    </tr>
    <tr>
      <th>677</th>
      <td>COP</td>
      <td>POLICE OFFICER</td>
    </tr>
    <tr>
      <th>678</th>
      <td>COP</td>
      <td>POLICE</td>
    </tr>
    <tr>
      <th>679</th>
      <td>COP</td>
      <td>POLICE OFFICER</td>
    </tr>
    <tr>
      <th>681</th>
      <td>COP</td>
      <td>DEPUTY</td>
    </tr>
    <tr>
      <th>700</th>
      <td>CRM</td>
      <td>CRIMINAL</td>
    </tr>
    <tr>
      <th>744</th>
      <td>CVL</td>
      <td>VILLAGE</td>
    </tr>
    <tr>
      <th>745</th>
      <td>CVL</td>
      <td>COMMUNITY</td>
    </tr>
    <tr>
      <th>765</th>
      <td>CVL</td>
      <td>NEIGHBORHOOD</td>
    </tr>
    <tr>
      <th>816</th>
      <td>EDU</td>
      <td>SCHOOL</td>
    </tr>
    <tr>
      <th>818</th>
      <td>EDU</td>
      <td>STUDENT</td>
    </tr>
    <tr>
      <th>819</th>
      <td>EDU</td>
      <td>STUDENT</td>
    </tr>
    <tr>
      <th>826</th>
      <td>EDU</td>
      <td>UNIVERSITY</td>
    </tr>
    <tr>
      <th>861</th>
      <td>EDU</td>
      <td>STUDENT</td>
    </tr>
    <tr>
      <th>862</th>
      <td>EDU</td>
      <td>STUDENT</td>
    </tr>
    <tr>
      <th>863</th>
      <td>EDU</td>
      <td>STUDENT</td>
    </tr>
    <tr>
      <th>865</th>
      <td>EDUEDU</td>
      <td>SCHOOL</td>
    </tr>
    <tr>
      <th>886</th>
      <td>ESP</td>
      <td>BARCELONA</td>
    </tr>
    <tr>
      <th>887</th>
      <td>ESP</td>
      <td>BARCELONA</td>
    </tr>
    <tr>
      <th>974</th>
      <td>GBR</td>
      <td>BRITAIN</td>
    </tr>
    <tr>
      <th>1030</th>
      <td>GOV</td>
      <td>FIREFIGHTER</td>
    </tr>
    <tr>
      <th>1038</th>
      <td>GOV</td>
      <td>KING</td>
    </tr>
    <tr>
      <th>1039</th>
      <td>GOV</td>
      <td>GOVERNMENT</td>
    </tr>
    <tr>
      <th>1056</th>
      <td>GOV</td>
      <td>PRIME MINISTER</td>
    </tr>
    <tr>
      <th>1057</th>
      <td>GOV</td>
      <td>PRIME MINISTER</td>
    </tr>
    <tr>
      <th>1065</th>
      <td>GOV</td>
      <td>DESPOT</td>
    </tr>
    <tr>
      <th>1066</th>
      <td>GOV</td>
      <td>DESPOT</td>
    </tr>
    <tr>
      <th>1090</th>
      <td>GOV</td>
      <td>GOVERNMENT</td>
    </tr>
    <tr>
      <th>1098</th>
      <td>GOV</td>
      <td>INTERIOR MINIST</td>
    </tr>
    <tr>
      <th>1118</th>
      <td>GOV</td>
      <td>MINIST</td>
    </tr>
    <tr>
      <th>1131</th>
      <td>GOVHLH</td>
      <td>HEALTH DEPARTMENT</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2050</th>
      <td>SYRMIL</td>
      <td>SYRIA</td>
    </tr>
    <tr>
      <th>2057</th>
      <td>TUN</td>
      <td>TUNISIA</td>
    </tr>
    <tr>
      <th>2058</th>
      <td>TUN</td>
      <td>TUNISIA</td>
    </tr>
    <tr>
      <th>2059</th>
      <td>TUN</td>
      <td>TUNISIA</td>
    </tr>
    <tr>
      <th>2061</th>
      <td>TUR</td>
      <td>TURKISH</td>
    </tr>
    <tr>
      <th>2062</th>
      <td>TUR</td>
      <td>ISTANBUL</td>
    </tr>
    <tr>
      <th>2063</th>
      <td>TUR</td>
      <td>ISTANBUL</td>
    </tr>
    <tr>
      <th>2066</th>
      <td>TUR</td>
      <td>TURKISH</td>
    </tr>
    <tr>
      <th>2067</th>
      <td>TUR</td>
      <td>TURKISH</td>
    </tr>
    <tr>
      <th>2072</th>
      <td>TURCOP</td>
      <td>TURKISH</td>
    </tr>
    <tr>
      <th>2086</th>
      <td>UAF</td>
      <td>TERRORIST</td>
    </tr>
    <tr>
      <th>2087</th>
      <td>UAF</td>
      <td>MILITANT</td>
    </tr>
    <tr>
      <th>2088</th>
      <td>UAF</td>
      <td>FIGHTER</td>
    </tr>
    <tr>
      <th>2089</th>
      <td>UAF</td>
      <td>TERRORIST</td>
    </tr>
    <tr>
      <th>2090</th>
      <td>UAF</td>
      <td>TERRORIST</td>
    </tr>
    <tr>
      <th>2091</th>
      <td>UAF</td>
      <td>TERRORIST</td>
    </tr>
    <tr>
      <th>2092</th>
      <td>UAF</td>
      <td>TERRORIST</td>
    </tr>
    <tr>
      <th>2093</th>
      <td>UAF</td>
      <td>FIGHTER</td>
    </tr>
    <tr>
      <th>2094</th>
      <td>UAF</td>
      <td>FIGHTER</td>
    </tr>
    <tr>
      <th>2265</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2266</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2267</th>
      <td>USA</td>
      <td>OHIO</td>
    </tr>
    <tr>
      <th>2268</th>
      <td>USA</td>
      <td>NEW YORK</td>
    </tr>
    <tr>
      <th>2269</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2270</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2276</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2277</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2278</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2279</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2280</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2281</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2282</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2283</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2284</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2285</th>
      <td>USA</td>
      <td>AMERICAN</td>
    </tr>
    <tr>
      <th>2288</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2289</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2350</th>
      <td>USA</td>
      <td>ARKANSAS</td>
    </tr>
    <tr>
      <th>2351</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2352</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2353</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2359</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2364</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2365</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2366</th>
      <td>USA</td>
      <td>TEXAS</td>
    </tr>
    <tr>
      <th>2381</th>
      <td>USA</td>
      <td>ORLANDO</td>
    </tr>
    <tr>
      <th>2382</th>
      <td>USA</td>
      <td>ORLANDO</td>
    </tr>
    <tr>
      <th>2383</th>
      <td>USA</td>
      <td>ORLANDO</td>
    </tr>
    <tr>
      <th>2384</th>
      <td>USA</td>
      <td>NEW YORK</td>
    </tr>
    <tr>
      <th>2385</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2386</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2387</th>
      <td>USA</td>
      <td>NEW YORK</td>
    </tr>
    <tr>
      <th>2408</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2411</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2412</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2413</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2415</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2436</th>
      <td>USA</td>
      <td>TEXAS</td>
    </tr>
    <tr>
      <th>2475</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2476</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2508</th>
      <td>USA</td>
      <td>ARIZONA</td>
    </tr>
    <tr>
      <th>2509</th>
      <td>USA</td>
      <td>ARIZONA</td>
    </tr>
    <tr>
      <th>2514</th>
      <td>USA</td>
      <td>KANSAS CITY</td>
    </tr>
    <tr>
      <th>2536</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2589</th>
      <td>USA</td>
      <td>NEW YORK</td>
    </tr>
    <tr>
      <th>2590</th>
      <td>USA</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2605</th>
      <td>USA</td>
      <td>ATLANTA</td>
    </tr>
    <tr>
      <th>2615</th>
      <td>USACOP</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2616</th>
      <td>USACOP</td>
      <td>PHILADELPHIA</td>
    </tr>
    <tr>
      <th>2617</th>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
    </tr>
    <tr>
      <th>2618</th>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
    </tr>
    <tr>
      <th>2619</th>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
    </tr>
    <tr>
      <th>2620</th>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
    </tr>
    <tr>
      <th>2622</th>
      <td>USACOP</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2623</th>
      <td>USACOP</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2634</th>
      <td>USAEDU</td>
      <td>MARYLAND</td>
    </tr>
    <tr>
      <th>2639</th>
      <td>USAEDU</td>
      <td>CALIFORNIA</td>
    </tr>
    <tr>
      <th>2640</th>
      <td>USAEDU</td>
      <td>CALIFORNIA</td>
    </tr>
    <tr>
      <th>2662</th>
      <td>USAGOV</td>
      <td>NASA</td>
    </tr>
    <tr>
      <th>2663</th>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
    </tr>
    <tr>
      <th>2664</th>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
    </tr>
    <tr>
      <th>2669</th>
      <td>USAGOV</td>
      <td>OBAMA</td>
    </tr>
    <tr>
      <th>2670</th>
      <td>USAGOV</td>
      <td>OBAMA</td>
    </tr>
    <tr>
      <th>2671</th>
      <td>USAGOV</td>
      <td>OBAMA</td>
    </tr>
    <tr>
      <th>2683</th>
      <td>USAGOV</td>
      <td>OBAMA</td>
    </tr>
    <tr>
      <th>2684</th>
      <td>USAGOV</td>
      <td>OBAMA</td>
    </tr>
    <tr>
      <th>2685</th>
      <td>USAGOV</td>
      <td>OBAMA</td>
    </tr>
    <tr>
      <th>2686</th>
      <td>USAGOV</td>
      <td>OBAMA</td>
    </tr>
    <tr>
      <th>2687</th>
      <td>USAGOV</td>
      <td>OBAMA</td>
    </tr>
    <tr>
      <th>2699</th>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
    </tr>
    <tr>
      <th>2700</th>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
    </tr>
    <tr>
      <th>2701</th>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
    </tr>
    <tr>
      <th>2706</th>
      <td>USAGOVHLH</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2711</th>
      <td>USAJUD</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2740</th>
      <td>USAPTY</td>
      <td>UNITED STATES</td>
    </tr>
    <tr>
      <th>2751</th>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
    </tr>
    <tr>
      <th>2752</th>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
    </tr>
    <tr>
      <th>2753</th>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
    </tr>
    <tr>
      <th>2755</th>
      <td>bte</td>
      <td>BETI</td>
    </tr>
    <tr>
      <th>2756</th>
      <td>bte</td>
      <td>BETI</td>
    </tr>
  </tbody>
</table>
<p>308 rows × 2 columns</p>
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
import feather
path = 'my_data.feather'
feather.api.write_dataframe(testdf, path)
newtestdf = feather.api.read_dataframe(path)
```

# Leftovers; Junkyard below (stuff to work on)


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
