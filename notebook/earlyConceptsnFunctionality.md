

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
results
```


```python
pd.options.display.max_rows = 200
```


```python
import pandas as pd

df = pd.DataFrame(data.json())
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


```python
parse("12:45").minute
```


```python
import datetime
answer = (datetime.datetime.now())
isinstance(answer,datetime.datetime)
```

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
            minute=0, second=0) + timedelta(
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
resultsmatch_date(gdelt_timeString(dateInputCheck(date)))
```

## Munging Data: Extracting Specific Datasets or all of them

Work with the returned GDELT dataframe.  Specific whether we are pulling the `mentions`, `events`, or `gkg` date for the day or all.  


```python
results[].ix[2002]
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
    return pd.read_csv(StringIO(data),delimiter='\t',header=None)
    
    
    

```


```python
testdf = downloadAndExtract('http://data.gdeltproject.org/gdeltv2/20150225234500.gkg.csv.zip')
```

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


```python
newtestdf
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>17</th>
      <th>18</th>
      <th>19</th>
      <th>20</th>
      <th>21</th>
      <th>22</th>
      <th>23</th>
      <th>24</th>
      <th>25</th>
      <th>26</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20150225234500-0</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>usatoday.com</td>
      <td>http://www.usatoday.com/story/life/people/2015...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_JUDGE;TAX_FNCACT_ACTRESS...</td>
      <td>TAX_FNCACT_DEPUTY,512;TAX_FNCACT_CHIEF,505;TAX...</td>
      <td>4#London, London, City Of, United Kingdom#US#U...</td>
      <td>...</td>
      <td>wc:170,c1.2:1,c12.1:8,c12.10:8,c12.12:1,c12.13...</td>
      <td>http://www.gannett-cdn.com/-mm-/83c22e7929319e...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Lindsay Lohan,56;Angeles Superior Court Judge ...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20150225234500-1</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>theeagle.com</td>
      <td>http://www.theeagle.com/news/business/what-we-...</td>
      <td>None</td>
      <td>None</td>
      <td>GENERAL_GOVERNMENT;ECON_INTEREST_RATES;GENERAL...</td>
      <td>ECON_WORLDCURRENCIES_DOLLAR,2877;TAX_POLITICAL...</td>
      <td>1#United States#US#US#38#-97#US;3#Washington, ...</td>
      <td>...</td>
      <td>wc:664,c1.2:9,c12.1:54,c12.10:92,c12.12:24,c12...</td>
      <td>http://bloximages.chicago2.vip.townnews.com/th...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Federal Reserve Chair Janet Yellen,121;House F...</td>
      <td>3,things we heard,349;6,months,817;2,meetings,...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20150225234500-2</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>tbnweekly.com</td>
      <td>http://www.tbnweekly.com/editorial/outdoors/co...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_DISEASE;TAX_DISEASE_PATHOGENS;TAX_WORLDMAM...</td>
      <td>EDUCATION,1106;KILL,567;TAX_FNCACT_AGENT,1241;...</td>
      <td>None</td>
      <td>...</td>
      <td>wc:188,c1.3:3,c12.1:12,c12.10:19,c12.12:13,c12...</td>
      <td>http://www.tbnweekly.com/images/fbimg_large.jpg</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Pinellas County,18;National Invasive Species A...</td>
      <td>1000000000,of dollars every year,358;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20150225234500-3</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>journalstar.com</td>
      <td>http://journalstar.com/ap/state/beef-plant-sit...</td>
      <td>None</td>
      <td>None</td>
      <td>EDUCATION;</td>
      <td>EDUCATION,2969;</td>
      <td>2#Wyoming, United States#GM#USWY#42.7475#-107....</td>
      <td>...</td>
      <td>wc:516,c1.2:5,c12.1:10,c12.10:32,c12.11:1,c12....</td>
      <td>http://bloximages.chicago2.vip.townnews.com/jo...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Property Group,209;Josh Berger,552;Leo Hoehn,9...</td>
      <td>2,months away,91;150,people would work at,582;...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20150225234500-4</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>kfbb.com</td>
      <td>http://www.kfbb.com/story/28198804/representat...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_SECRETARY;TAX_FNCACT_SEC...</td>
      <td>TAX_FNCACT_CONGRESSMAN,2172;LEADER,191;TAX_FNC...</td>
      <td>1#Iran#US#IR#32#53#IR;2#California, United Sta...</td>
      <td>...</td>
      <td>wc:571,c12.1:37,c12.10:65,c12.12:15,c12.13:15,...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>State John Kerry,54;Capitol Hill,95;House Fore...</td>
      <td>12,of questions,132;2,sides over how long,1021...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20150225234500-5</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>kyma.com</td>
      <td>http://www.kyma.com/protesters-plan-to-block-poe/</td>
      <td>PROTEST#8##4#Calexico, Nayarit, Mexico#MX#MX18...</td>
      <td>PROTEST#8##4#Calexico, Nayarit, Mexico#MX#MX18...</td>
      <td>TRAFFIC;PROTEST;GENERAL_GOVERNMENT;TAX_ETHNICI...</td>
      <td>BAN,779;BAN,1033;GENERAL_GOVERNMENT,366;GENERA...</td>
      <td>1#Mexico#MX#MX#23#-102#MX;1#United States#MX#U...</td>
      <td>...</td>
      <td>wc:316,c1.2:2,c12.1:17,c12.10:19,c12.12:10,c12...</td>
      <td>http://img.youtube.com/vi/6sqbFndG4SY/0.jpg</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/embed/6sqbFndG4SY;https://...</td>
      <td>609|215||The reason why we are going to close ...</td>
      <td>Leonardo Alvarez,221;Maria Asedas,1488</td>
      <td>6,months,259;2,countries on Thursday,532;50000...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20150225234500-6</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>news8000.com</td>
      <td>http://www.news8000.com/entertainment/well-mis...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_WOMAN;MEDIA_MSM;LEADER;T...</td>
      <td>TAX_FNCACT_SECRETARY_OF_STATE,635;TAX_FNCACT_S...</td>
      <td>None</td>
      <td>...</td>
      <td>wc:445,c1.4:1,c12.1:48,c12.10:39,c12.12:11,c12...</td>
      <td>http://www.news8000.com/image/view/-/31466204/...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/user/wkbttv;</td>
      <td>1151|25||the best day of the year!</td>
      <td>Amy Poehler,107;Leslie Knope,398;Ron Swanson,4...</td>
      <td>2,were made for each,1873;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20150225234500-7</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>counton2.com</td>
      <td>http://www.counton2.com/story/28202992/madonna...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_QUEEN;</td>
      <td>TAX_FNCACT_QUEEN,143;</td>
      <td>4#London, London, City Of, United Kingdom#UK#U...</td>
      <td>...</td>
      <td>wc:119,c12.1:9,c12.10:8,c12.12:4,c12.13:2,c12....</td>
      <td>http://images.worldnow.com/AP/images/6837380_G...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>For Love,230;Taylor Swift,655;Brit Awards,689</td>
      <td>3,steps while her dancers,332;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20150225234500-8</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>myhighplains.com</td>
      <td>http://www.myhighplains.com/story/d/story/laws...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_DISEASE;TAX_DISEASE_SALMONELLA;TAX_DISEASE...</td>
      <td>TAX_DISEASE_SALMONELLA,23;TAX_FOODSTAPLES_MEAT...</td>
      <td>None</td>
      <td>...</td>
      <td>wc:64,c12.1:3,c12.10:6,c12.12:2,c12.13:1,c12.1...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20150225234500-9</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>lacrossetribune.com</td>
      <td>http://lacrossetribune.com/news/national/ohio-...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_MAN;TRIAL;TERROR;ARMEDCO...</td>
      <td>TAX_FNCACT_ATTORNEY,1085;TERROR,127;ARMEDCONFL...</td>
      <td>3#Columbus, Ohio, United States#US#USOH#39.961...</td>
      <td>...</td>
      <td>wc:286,c12.1:18,c12.10:15,c12.12:7,c12.13:7,c1...</td>
      <td>http://bloximages.chicago2.vip.townnews.com/la...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/user/TheLacrosseTribune;</td>
      <td>None</td>
      <td>Sheik Mohamud,284;Middle East,344;Franklin Cou...</td>
      <td>1000000,dollars ,199;18,months,282;5000000,bon...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>20150225234500-10</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>hurriyetdailynews.com</td>
      <td>http://www.hurriyetdailynews.com/between-the-r...</td>
      <td>KIDNAP#49#crisis#1#Syria#SY#SY#35#38#SY;</td>
      <td>KIDNAP#49#crisis#1#Syria#SY#SY#35#38#SY#2603;</td>
      <td>TAX_ETHNICITY;TAX_ETHNICITY_TURKISH;TAX_WORLDL...</td>
      <td>TAX_WORLDLANGUAGES_BASHAR,1794;KIDNAP,2651;ARM...</td>
      <td>1#Saudi Arabia#SY#SA#25#45#SA;1#Iraq#SY#IZ#33#...</td>
      <td>...</td>
      <td>wc:603,c1.3:1,c12.1:49,c12.10:65,c12.11:1,c12....</td>
      <td>http://www.hurriyetdailynews.com/images/NewsCa...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Turkish Armed Forces,77;Ottoman Empire,362;Isl...</td>
      <td>39,tanks,66;44,armored,74;542,soldiers,103;2,A...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11</th>
      <td>20150225234500-11</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>couriermail.com.au</td>
      <td>http://www.couriermail.com.au/news/breaking-ne...</td>
      <td>None</td>
      <td>None</td>
      <td>LEGISLATION;GENERAL_GOVERNMENT;TAX_FNCACT;TAX_...</td>
      <td>TAX_FNCACT_INSIDERS,205;GENERAL_GOVERNMENT,61;...</td>
      <td>None</td>
      <td>...</td>
      <td>wc:173,c1.3:1,c12.1:9,c12.10:17,c12.12:5,c12.1...</td>
      <td>http://resources.news.com.au/cs/couriermail/im...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Michelle Lensink,193;Animal Welfare,554;Greyho...</td>
      <td>10,dollars ,585;50,dollars ,654;20,dollars ,748;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>12</th>
      <td>20150225234500-12</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>caledonianrecord.com</td>
      <td>http://caledonianrecord.com/main.asp?SectionID...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_INSTRUCTOR;TAX_FNCACT_MA...</td>
      <td>TAX_FNCACT_EXECUTIVE_DIRECTOR,2791;TAX_FNCACT_...</td>
      <td>3#Littleton, New Hampshire, United States#US#U...</td>
      <td>...</td>
      <td>wc:889,c1.1:1,c1.4:1,c12.1:37,c12.10:58,c12.12...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Johnsbury Rotarians,105;Lyndon Rescue,226;Bill...</td>
      <td>30,ski patrol members,631;8,full,653;66,on Mar...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>13</th>
      <td>20150225234500-13</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>msnbc.com</td>
      <td>http://www.msnbc.com/politicsnation/chicago-po...</td>
      <td>ARREST#2##3#Chicago, Illinois, United States#U...</td>
      <td>ARREST#2##3#Chicago, Illinois, United States#U...</td>
      <td>SECURITY_SERVICES;TAX_FNCACT;TAX_FNCACT_POLICE...</td>
      <td>TAX_MILITARY_TITLE_OFFICERS,172;TAX_FNCACT_OFF...</td>
      <td>3#Chicago, Illinois, United States#US#USIL#41....</td>
      <td>...</td>
      <td>wc:168,c12.1:15,c12.10:11,c12.12:4,c12.13:2,c1...</td>
      <td>http://www.msnbc.com/sites/msnbc/files/chicago...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Chicago Police,86;Organized Crime,393;Evidence...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>14</th>
      <td>20150225234500-14</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>go.com</td>
      <td>http://abcnews.go.com/Politics/wireStory/envoy...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_ENVOY;ALLIANCE;TAX_RELIG...</td>
      <td>TAX_FNCACT_ENVOY,17;TAX_TERROR_GROUP_ISLAMIC_S...</td>
      <td>1#Iraq#IZ#IZ#33#44#IZ</td>
      <td>...</td>
      <td>wc:104,c1.3:1,c1.4:1,c12.1:8,c12.10:7,c12.12:3...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Islamic State,77;John Allen,201;Senate Foreign...</td>
      <td>500,airstrikes by the U,282;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>15</th>
      <td>20150225234500-15</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>stltoday.com</td>
      <td>http://www.stltoday.com/news/outage-halts-inte...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_SPOKESMAN;AFFECT;TAX_FNC...</td>
      <td>AFFECT,287;TAX_FNCACT_TECHNICIANS,665;TAX_FNCA...</td>
      <td>4#Juarez, MéCo, Mexico#US#MX15#31.7333#-106.48...</td>
      <td>...</td>
      <td>wc:121,c12.1:6,c12.10:5,c12.12:2,c12.13:2,c12....</td>
      <td>http://bloximages.newyork1.vip.townnews.com/st...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Alex Juarez,221</td>
      <td>100,miles away,301;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>16</th>
      <td>20150225234500-16</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>billingsgazette.com</td>
      <td>http://billingsgazette.com/entertainment/music...</td>
      <td>None</td>
      <td>None</td>
      <td>MEDIA_MSM;TAX_FNCACT;TAX_FNCACT_SINGER;TAX_FNC...</td>
      <td>MANMADE_DISASTER_IMPLIED,1906;REBELLION,2674;R...</td>
      <td>1#United Kingdom#SF#UK#54#-2#UK;4#London, Lond...</td>
      <td>...</td>
      <td>wc:657,c1.1:5,c1.2:1,c12.1:60,c12.10:56,c12.12...</td>
      <td>http://bloximages.chicago2.vip.townnews.com/bi...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>3148|38||all the underdogs and all the grafters</td>
      <td>Sam Smith,51;Kanye West,187;Brit Awards,300;Fo...</td>
      <td>12,of dancers,994;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>17</th>
      <td>20150225234500-17</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>radionz.co.nz</td>
      <td>http://www.radionz.co.nz/international/pacific...</td>
      <td>None</td>
      <td>None</td>
      <td>GENERAL_GOVERNMENT;ECON_SUBSIDIES;ENV_FISHERY;...</td>
      <td>ECON_SUBSIDIES,141;ECON_SUBSIDIES,258;ECON_SUB...</td>
      <td>1#United States#BP#US#38#-97#US;1#China#BP#CH#...</td>
      <td>...</td>
      <td>wc:143,c1.3:1,c12.1:3,c12.10:11,c12.12:6,c12.1...</td>
      <td>http://www.radionz.co.nz/x/rnz-general-sq-1d62...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>United States,21;Pacific Island,85;Task Force,...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>18</th>
      <td>20150225234500-18</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>avonadvocate.com.au</td>
      <td>http://www.avonadvocate.com.au/story/2908785/b...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_ETHNICITY;TAX_ETHNICITY_INDONESIAN;TAX_WOR...</td>
      <td>MEDIA_MSM,683;CRIME_ILLEGAL_DRUGS,899;TAX_ETHN...</td>
      <td>4#Kerobokan, Bali, Indonesia#ID#ID02#-8.3259#1...</td>
      <td>...</td>
      <td>wc:210,c12.1:25,c12.10:28,c12.12:8,c12.13:10,c...</td>
      <td>http://transform.fairfaxregional.com.au/transf...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>82|41||carefully considering Indonesia positio...</td>
      <td>President Joko Widodo,35;Prime Minister Tony A...</td>
      <td>2,Australians on death row,85;3,kilos of heroi...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20150225234500-19</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>collegehumor.com</td>
      <td>http://www.collegehumor.com/post/7012859/if-yo...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_WORLDMAMMALS;TAX_WORLDMAMMALS_ASS;</td>
      <td>TAX_WORLDMAMMALS_ASS,151;</td>
      <td>None</td>
      <td>...</td>
      <td>wc:40,c12.1:6,c12.10:3,c12.13:1,c12.14:2,c12.3...</td>
      <td>http://1.media.collegehumor.cvcdn.com/94/47/bf...</td>
      <td>http:/2.media.collegehumor.cvcdn.com/58/21/fbe...</td>
      <td>None</td>
      <td>https://youtube.com/CollegeHumor?sub_confirmat...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20150225234500-20</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>yahoo.com</td>
      <td>https://in.news.yahoo.com/americas-next-top-mo...</td>
      <td>KILL#3##2#North Carolina, United States#US#USN...</td>
      <td>KILL#3##2#North Carolina, United States#US#USN...</td>
      <td>TAX_WORLDFISH;TAX_WORLDFISH_TOP;KILL;SECURITY_...</td>
      <td>TAX_FNCACT_FASHION_MODEL,953;TAX_FNCACT_WOMAN,...</td>
      <td>1#United States#US#US#38#-97#US;3#Winston-Sale...</td>
      <td>...</td>
      <td>wc:183,c12.1:9,c12.10:13,c12.12:3,c12.13:6,c12...</td>
      <td>https://s.yimg.com/bt/api/res/1.2/6rik6AZwuPGC...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Next Top,74;North Carolina,145;Mirjana Puhar,2...</td>
      <td>3,people whose bodies were,205;3,counts of mur...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>21</th>
      <td>20150225234500-21</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>finanznachrichten.de</td>
      <td>http://www.finanznachrichten.de/nachrichten-20...</td>
      <td>None</td>
      <td>None</td>
      <td>ECON_CURRENCY_EXCHANGE_RATE;ECON_TAXATION;ECON...</td>
      <td>TAX_FNCACT_EXECUTIVE_OFFICER,70713;TAX_WORLDMA...</td>
      <td>1#Saudi Arabia#CA#SA#25#45#SA;1#Canada#CA#CA#6...</td>
      <td>...</td>
      <td>wc:10182,c1.2:62,c1.3:16,c12.1:343,c12.10:1091...</td>
      <td>http://fns1.de/g/fb.png</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>61380|25||Revolving Credit Facility</td>
      <td>Well Service,59;International Financial Report...</td>
      <td>3,months ended Twelve months,73;12,months ende...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>22</th>
      <td>20150225234500-22</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>chron.com</td>
      <td>http://www.chron.com/news/article/Madonna-take...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_QUEEN;</td>
      <td>TAX_FNCACT_QUEEN,161;</td>
      <td>4#London, London, City Of, United Kingdom#UK#U...</td>
      <td>...</td>
      <td>wc:115,c12.1:8,c12.10:7,c12.12:4,c12.13:2,c12....</td>
      <td>http://ww1.hdnux.com/photos/34/71/56/7576492/5...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/channel/UCnqTK-gPZiJ7hlT4x...</td>
      <td>None</td>
      <td>For Love,257;Taylor Swift,706;Brit Awards,740</td>
      <td>3,steps while her dancers,348;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>23</th>
      <td>20150225234500-23</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>washingtonpost.com</td>
      <td>http://www.washingtonpost.com/blogs/the-fix/wp...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_WORLDLANGUAGES;TAX_WORLDLANGUAGES_TERRIS;T...</td>
      <td>AFFECT,3145;TAX_FNCACT_DESIGNER,1834;TAX_WORLD...</td>
      <td>1#United States#US#US#38#-97#US</td>
      <td>...</td>
      <td>wc:712,c1.3:1,c12.1:41,c12.10:59,c12.12:25,c12...</td>
      <td>http://img.washingtonpost.com/blogs/the-fix/fi...</td>
      <td>http:/img.washingtonpost.com/blogs/the-fix/fil...</td>
      <td>http://pic.twitter.com/nif6m7GOxC;http://pic.t...</td>
      <td>None</td>
      <td>1004|66||I don't know anything about Photoshop...</td>
      <td>Tim Scott,97;African American,171;Talking Poin...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>24</th>
      <td>20150225234500-24</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>ketv.com</td>
      <td>http://www.ketv.com/news/ndor-cams-catch-part-...</td>
      <td>None</td>
      <td>None</td>
      <td>HATE_SPEECH;</td>
      <td>HATE_SPEECH,392;</td>
      <td>None</td>
      <td>...</td>
      <td>wc:173,c12.1:16,c12.10:19,c12.12:6,c12.13:8,c1...</td>
      <td>http://www.ketv.com/image/view/-/31473914/medR...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>7,offers readers the ability,140;7,newscasts,2...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>25</th>
      <td>20150225234500-25</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>lycos.com</td>
      <td>http://news.lycos.com/technology/nasa-investig...</td>
      <td>None</td>
      <td>None</td>
      <td>MANMADE_DISASTER_IMPLIED;TAX_FNCACT;TAX_FNCACT...</td>
      <td>MANMADE_DISASTER_IMPLIED,155;MANMADE_DISASTER_...</td>
      <td>1#United States#IT#US#38#-97#US;1#Russia#IT#RS...</td>
      <td>...</td>
      <td>wc:384,c1.2:1,c1.3:2,c12.1:8,c12.10:24,c12.12:...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Terry Virts,367;Samantha Cristoforetti,718;Mis...</td>
      <td>2,sites being reconfigured for,1206;2,internat...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>26</th>
      <td>20150225234500-26</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>siouxcityjournal.com</td>
      <td>http://siouxcityjournal.com/business/technolog...</td>
      <td>None</td>
      <td>None</td>
      <td>EDUCATION;SOC_POINTSOFINTEREST;SOC_POINTSOFINT...</td>
      <td>EDUCATION,788;SOC_POINTSOFINTEREST_PRESCHOOL,788;</td>
      <td>None</td>
      <td>...</td>
      <td>wc:140,c12.1:8,c12.10:8,c12.12:1,c12.13:4,c12....</td>
      <td>http://siouxcityjournal.com/app/images/FBlogo.jpg</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>27</th>
      <td>20150225234500-27</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>businesswire.com</td>
      <td>http://www.businesswire.com/news/home/20150225...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_MASON;TAX_FNCACT_CARDINA...</td>
      <td>TAX_FNCACT_CARDINAL,84;TAX_FNCACT_CARDINAL,131...</td>
      <td>3#Tysons Corner, Virginia, United States#US#US...</td>
      <td>...</td>
      <td>wc:348,c12.1:21,c12.10:18,c12.12:4,c12.13:3,c1...</td>
      <td>http://mms.businesswire.com/media/201502250066...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Cardinal Bank,70;Greater Richmond,179;George M...</td>
      <td>5,overall,332;12,months,368;400,families move ...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>28</th>
      <td>20150225234500-28</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>4-traders.com</td>
      <td>http://www.4-traders.com/HYUNDAI-MOTOR-CO-6492...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_EDITOR;MEDIA_MSM;TAX_FNC...</td>
      <td>IDEOLOGY,10044;TAX_FNCACT_CORRESPONDENTS,284;S...</td>
      <td>3#Washington, District Of Columbia, United Sta...</td>
      <td>...</td>
      <td>wc:1807,c12.1:63,c12.10:197,c12.12:55,c12.13:4...</td>
      <td>http://www.4-traders.com/images/strat_N.png</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>News Reporter-Staff News Editor,40;Hyundai Mot...</td>
      <td>2,temperature sensors,2134;1,is a view schemat...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>29</th>
      <td>20150225234500-29</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>abc7news.com</td>
      <td>http://abc7news.com/technology/apple-to-pay-$5...</td>
      <td>None</td>
      <td>None</td>
      <td>TRIAL;TAX_FNCACT;TAX_FNCACT_ATTORNEY;GENERAL_G...</td>
      <td>ECON_STOCKMARKET,2773;ECON_STOCKMARKET,2906;TA...</td>
      <td>2#Nevada, United States#US#USNV#38.4199#-117.1...</td>
      <td>...</td>
      <td>wc:510,c1.2:2,c12.1:32,c12.10:51,c12.12:20,c12...</td>
      <td>http://cdn.abclocal.go.com/content/kgo/images/...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/iframe_api;</td>
      <td>3223|37||We see little impact from the verdict</td>
      <td>Eastern District,1174;Brad Caldwell,1766;Peter...</td>
      <td>533000000,dollars by a federal jury,44;3,paten...</td>
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
      <th>3151</th>
      <td>20150225234500-183</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>counton2.com</td>
      <td>http://www.counton2.com/story/28202319/study-n...</td>
      <td>None</td>
      <td>None</td>
      <td>GENERAL_HEALTH;MEDICAL;TAX_FNCACT;TAX_FNCACT_W...</td>
      <td>SOC_POINTSOFINTEREST_HOSPITALS,1118;SOC_POINTS...</td>
      <td>1#United States#US#US#38#-97#US</td>
      <td>...</td>
      <td>wc:383,c12.1:27,c12.10:42,c12.12:18,c12.13:15,...</td>
      <td>http://images.worldnow.com/AP/images/6836330_G...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Disease Control,655;New England Journal,717</td>
      <td>10,states,980;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3152</th>
      <td>20150225234500-184</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>bangladeshsun.com</td>
      <td>http://www.bangladeshsun.com/index.php/nav/mre...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_DIRECTOR;POVERTY;</td>
      <td>TAX_FNCACT_DIRECTOR,29;TAX_FNCACT_DIRECTOR,136...</td>
      <td>1#Iran#US#IR#32#53#IR;1#United States#US#US#38...</td>
      <td>...</td>
      <td>wc:1017,c1.1:1,c1.2:1,c1.4:3,c12.1:104,c12.10:...</td>
      <td>None</td>
      <td>http:/www.bangladeshsun.com/MoviePosters/House...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Vadim Perelman,55;Vadim Perelman,87;Shawn Lawr...</td>
      <td>2,opposing sides,868;8,months when the county,...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3153</th>
      <td>20150225234500-185</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>fox17.com</td>
      <td>http://www.fox17.com/template/inews_wire/wires...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>...</td>
      <td>wc:144,c1.3:1,c12.1:6,c12.10:18,c12.12:3,c12.1...</td>
      <td>http://www.fox17.com/news/features/top-stories...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>545|39||the most intense period of preparations</td>
      <td>International News,20;Rio Olympics,235;Nawal E...</td>
      <td>24,GMT By STEPHEN WADE,88;40,test events plann...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3154</th>
      <td>20150225234500-186</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>abc7news.com</td>
      <td>http://abc7news.com/news/ex-police-chief-says-...</td>
      <td>AFFECT#911##0######;</td>
      <td>AFFECT#911##0#######414;</td>
      <td>TAX_FNCACT;TAX_FNCACT_ORGANIZER;TAX_MILITARY_T...</td>
      <td>GEN_HOLIDAY,678;TAX_FNCACT_ATTORNEY,1195;TAX_F...</td>
      <td>None</td>
      <td>...</td>
      <td>wc:224,c12.1:8,c12.10:16,c12.12:8,c12.13:4,c12...</td>
      <td>http://cdn.abclocal.go.com/content/creativecon...</td>
      <td>http:/cdn.abclocal.go.com/content/creativeCont...</td>
      <td>None</td>
      <td>https://youtube.com/iframe_api;</td>
      <td>986|101|| ..we faced a situation as I said ear...</td>
      <td>Patsy Ramsey,387;District Attorney,1322;Associ...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3155</th>
      <td>20150225234500-187</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>reuters.com</td>
      <td>http://www.reuters.com/article/2015/02/25/aia-...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1#China#CH#CH#35#105#CH;1#Singapore#CH#SN#1.36...</td>
      <td>...</td>
      <td>wc:393,c1.2:7,c1.3:1,c12.1:10,c12.10:41,c12.11...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/reuters;</td>
      <td>None</td>
      <td>Thomson Reuters,1032;Chief Executive Mark Tuck...</td>
      <td>45000000000,* Insurer reaps rewards,40;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3156</th>
      <td>20150225234500-188</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>columbustelegram.com</td>
      <td>http://columbustelegram.com/news/national/wesl...</td>
      <td>ARREST#4#Wesleyan University students#3#Middle...</td>
      <td>ARREST#4#Wesleyan University students#3#Middle...</td>
      <td>SECURITY_SERVICES;TAX_FNCACT;TAX_FNCACT_POLICE...</td>
      <td>TRIAL,394;EDUCATION,88;SOC_POINTSOFINTEREST_UN...</td>
      <td>2#California, United States#US#USCA#36.17#-119...</td>
      <td>...</td>
      <td>wc:127,c12.1:8,c12.10:2,c12.13:1,c12.14:1,c12....</td>
      <td>http://bloximages.chicago2.vip.townnews.com/co...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Wesleyan University,88;Rio De Janeiro,266;Zach...</td>
      <td>12,people who took the,106;3,were released aft...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3157</th>
      <td>20150225234500-189</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>fox30jax.com</td>
      <td>http://www.fox30jax.com/ap/ap/entertainment/pu...</td>
      <td>KILL#2##2#Washington, United States#US#USWA#47...</td>
      <td>KILL#2##2#Washington, United States#US#USWA#47...</td>
      <td>TAX_WORLDMAMMALS;TAX_WORLDMAMMALS_FOX;KILL;TER...</td>
      <td>TAX_FNCACT_DEPUTY,1760;TAX_FNCACT_PUBLISHER,14...</td>
      <td>1#United States#US#US#38#-97#US;2#Florida, Uni...</td>
      <td>...</td>
      <td>wc:506,c1.3:1,c12.1:25,c12.10:43,c12.12:8,c12....</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Fox News Channel,76;Abraham Lincoln,233;Jesus ...</td>
      <td>1000000,of copies,217;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3158</th>
      <td>20150225234500-190</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>themorningbulletin.com.au</td>
      <td>http://www.themorningbulletin.com.au/news/uh-o...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1#Australia#GH#AS#-27#133#AS;4#Brisbane, Queen...</td>
      <td>...</td>
      <td>wc:94,c12.1:1,c12.10:14,c12.12:6,c12.13:2,c12....</td>
      <td>http://media.apnarm.net.au/img/media/images/20...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Gold Coast Suns,52;Gold Coast Suns,299;News Co...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3159</th>
      <td>20150225234500-191</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>utsandiego.com</td>
      <td>http://www.utsandiego.com/news/2015/feb/25/spe...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_UNION_MEMBERS;LEADER;TAX...</td>
      <td>TAX_POLITICAL_PARTY_REPUBLICANS,528;TAX_POLITI...</td>
      <td>2#Illinois, United States#US#USIL#40.3363#-89....</td>
      <td>...</td>
      <td>wc:472,c1.4:1,c12.1:31,c12.10:42,c12.12:26,c12...</td>
      <td>http://media.utsandiego.com/img/photos/2015/02...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/user/utsandiego;</td>
      <td>None</td>
      <td>Gerry Miller,787;United Steelworkers,853;Perry...</td>
      <td>2,straight days this week,37;10,because minori...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3160</th>
      <td>20150225234500-192</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>theverge.com</td>
      <td>http://www.theverge.com/2015/2/25/8110521/de-b...</td>
      <td>None</td>
      <td>None</td>
      <td>LEADER;TAX_FNCACT;TAX_FNCACT_MAYOR;GOV_LOCALGO...</td>
      <td>TAX_FNCACT_COMMISSIONER,2943;LEGISLATION,2010;...</td>
      <td>2#New York, United States#US#USNY#42.1497#-74....</td>
      <td>...</td>
      <td>wc:481,c1.2:1,c12.1:35,c12.10:61,c12.12:10,c12...</td>
      <td>https://cdn2.vox-cdn.com/thumbor/HmSLyXNT01Ik5...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/subscription_center?add_us...</td>
      <td>None</td>
      <td>York City,17;Bill De Blasio,38;Federal Communi...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3161</th>
      <td>20150225234500-193</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>cnbc.com</td>
      <td>http://www.cnbc.com/id/102453322</td>
      <td>None</td>
      <td>None</td>
      <td>ENV_METALS;TAX_FNCACT;TAX_FNCACT_ANALYST;ECON_...</td>
      <td>GENERAL_GOVERNMENT,1071;GENERAL_GOVERNMENT,136...</td>
      <td>1#Switzerland#SZ#SZ#47#8#SZ;1#Germany#SZ#GM#51...</td>
      <td>...</td>
      <td>wc:495,c1.2:3,c12.1:38,c12.10:68,c12.11:1,c12....</td>
      <td>http://fm.cnbc.com/applications/cnbc.com/resou...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Federal Reserve,92;America Merrill,253;America...</td>
      <td>3,months you,310;1,dollars ,340;100,an ounce i...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3162</th>
      <td>20150225234500-194</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>neoskosmos.com</td>
      <td>http://neoskosmos.com/news/en/Shorten-offers-G...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_LEADER;TAX_ETHNICITY;TAX...</td>
      <td>GENERAL_GOVERNMENT,488;GENERAL_GOVERNMENT,680;...</td>
      <td>1#Australia#GR#AS#-27#133#AS;4#Parthenon, Peri...</td>
      <td>...</td>
      <td>wc:222,c12.1:17,c12.10:24,c12.12:7,c12.13:5,c1...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Parthenon Marbles,77;Lonsdale Street Festival,...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3163</th>
      <td>20150225234500-195</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>sruti.com</td>
      <td>http://www.sruti.com/index.php?main_page=produ...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_FATHER;MEDIA_MSM;</td>
      <td>MEDIA_MSM,1064;TAX_FNCACT_FATHER,293;TAX_FNCAC...</td>
      <td>None</td>
      <td>...</td>
      <td>wc:180,c12.1:8,c12.10:16,c12.12:2,c12.13:6,c12...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Maharajapuram Santhanam,62;Maestros Of Mafiara...</td>
      <td>2,articles by Santhanam fans,812;2,reports,891;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3164</th>
      <td>20150225234500-196</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>augustafreepress.com</td>
      <td>http://augustafreepress.com/virginia-tech-prof...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_ENGINEER;TAX_FNCACT_STRU...</td>
      <td>NATURAL_DISASTER_HURRICANE,1460;NATURAL_DISAST...</td>
      <td>1#United States#US#US#38#-97#US;2#California, ...</td>
      <td>...</td>
      <td>wc:586,c1.1:1,c1.2:5,c1.3:1,c12.1:21,c12.10:63...</td>
      <td>http://augustafreepress.com/wp-content/uploads...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/user/afpchrisgraham;</td>
      <td>None</td>
      <td>Matthew Eatherton,79;Virginia Tech,388;Environ...</td>
      <td>500,dollars ,419;2,civil engineering doctoral ...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3165</th>
      <td>20150225234500-197</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>njherald.com</td>
      <td>http://www.njherald.com/story/28202720/3-sente...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_ETHNICITY;TAX_ETHNICITY_WHITE;TAX_ETHNICIT...</td>
      <td>SOC_POINTSOFINTEREST_PRISON,211;TAX_FNCACT_WOM...</td>
      <td>2#Mississippi, United States#AS#USMS#32.7673#-...</td>
      <td>...</td>
      <td>wc:135,c12.1:8,c12.10:10,c12.12:5,c12.13:1,c12...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Judge Carlton Reeves,240;William Kirk Montgome...</td>
      <td>3,apologized,508;3,men were sentenced Feb,638;...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3166</th>
      <td>20150225234500-198</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>kycir.org</td>
      <td>http://kycir.org/2015/02/25/fired-university-o...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_WORLDFISH;TAX_WORLDFISH_TOP;TAX_FNCACT;TAX...</td>
      <td>TAX_FNCACT_PROVOST,627;TAX_FNCACT_PROVOST,4485...</td>
      <td>3#University Of Louisville, Kentucky, United S...</td>
      <td>...</td>
      <td>wc:754,c12.1:50,c12.10:56,c12.12:18,c12.13:16,...</td>
      <td>http://kycir.org/files/2014/06/u-of-l-web-1170...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>3727|43||most extreme example of race discrimi...</td>
      <td>Jefferson County Circuit Court,336;Sam Connall...</td>
      <td>10000000,dollars gift,752;10000000,dollars ,83...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3167</th>
      <td>20150225234500-199</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>eetimes.com</td>
      <td>http://www.eetimes.com/author.asp?section_id=3...</td>
      <td>None</td>
      <td>None</td>
      <td>GENERAL_GOVERNMENT;SOC_POINTSOFINTEREST;SOC_PO...</td>
      <td>GENERAL_GOVERNMENT,204;GENERAL_GOVERNMENT,3848...</td>
      <td>1#Germany#UK#GM#51#9#GM;1#Netherlands#UK#NL#52...</td>
      <td>...</td>
      <td>wc:1016,c1.1:1,c1.2:1,c12.1:66,c12.10:106,c12....</td>
      <td>http://img.deusm.com/eetimes/2015/02/1325809/H...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>90|40||s internal investigations into last wee...</td>
      <td>Security Agency,184;British Government Communi...</td>
      <td>1000000000,of phone calls,338;2000000000,SIM c...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3168</th>
      <td>20150225234500-200</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>channelnewsasia.com</td>
      <td>http://www.channelnewsasia.com/news/asiapacifi...</td>
      <td>ARREST#216##1#South Korea#KS#KS#37#127.5#KS;</td>
      <td>ARREST#216##1#South Korea#KS#KS#37#127.5#KS#674;</td>
      <td>CONSTITUTIONAL;LEGISLATION;BAN;ARREST;SOC_POIN...</td>
      <td>TAX_FNCACT_ACTRESSES,1868;TAX_ETHNICITY_BENCH,...</td>
      <td>4#Seoul, Soul-T'ukpyolsi, South Korea#KS#KS11#...</td>
      <td>...</td>
      <td>wc:505,c1.4:1,c12.1:49,c12.10:62,c12.12:28,c12...</td>
      <td>http://www.channelnewsasia.com/image/674416/13...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/channelnewsasia;</td>
      <td>None</td>
      <td>South Korea,18;Constitutional Court,40;South K...</td>
      <td>500,people have been formerly,437;216,people w...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3169</th>
      <td>20150225234500-201</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>uppermichiganssource.com</td>
      <td>http://www.uppermichiganssource.com/news/story...</td>
      <td>None</td>
      <td>None</td>
      <td>EDUCATION;</td>
      <td>EDUCATION,55;</td>
      <td>3#Detroit, Michigan, United States#US#USMI#42....</td>
      <td>...</td>
      <td>wc:149,c1.1:1,c12.1:9,c12.10:15,c12.12:4,c12.1...</td>
      <td>http://www.uppermichiganssource.com/uploadedIm...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/subscription_center?add_us...</td>
      <td>None</td>
      <td>High School,24;Dance Team,36;Michigan Kids Can...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3170</th>
      <td>20150225234500-202</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>1230foxsports.com</td>
      <td>http://www.1230foxsports.com/articles/local-ne...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>2#Illinois, United States#US#USIL#40.3363#-89....</td>
      <td>...</td>
      <td>wc:97,c12.1:7,c12.10:7,c12.12:7,c12.3:2,c12.5:...</td>
      <td>http://content.clearchannel.com/cc-common/loca...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Savage Arena,224;Health Education Building,259...</td>
      <td>30000000,Wednesday,302;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3171</th>
      <td>20150225234500-203</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>newsroomamerica.com</td>
      <td>http://www.newsroomamerica.com/story/477679/us...</td>
      <td>None</td>
      <td>None</td>
      <td>NATURAL_DISASTER;NATURAL_DISASTER_NATURAL_DISA...</td>
      <td>TAX_FNCACT_ASSISTANT,2776;RURAL,719;WATER_SECU...</td>
      <td>1#United States#US#US#38#-97#US;2#California, ...</td>
      <td>...</td>
      <td>wc:400,c1.2:1,c12.1:22,c12.10:40,c12.12:10,c12...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Primary Natural Disaster Areas With Assistance...</td>
      <td>9,Counties,15;9,counties,172;8,months,1496;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3172</th>
      <td>20150225234500-204</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>pleasantonexpress.com</td>
      <td>http://www.pleasantonexpress.com/news/2015-02-...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_RELIGION;TAX_RELIGION_CHURCH;CRIME_ILLEGAL...</td>
      <td>TAX_FNCACT_DIRECTOR,3042;MANMADE_DISASTER_IMPL...</td>
      <td>2#Ohio, United States#JN#USOH#40.3736#-82.7755#OH</td>
      <td>...</td>
      <td>wc:795,c1.2:1,c12.1:49,c12.10:43,c12.12:13,c12...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>153|64||s Episcopal Church in Pleas , Hwy. 97 ...</td>
      <td>Episcopal Church,104;Have Any,260;Refuge Paren...</td>
      <td>97,West,98;914,Ohio St,173;914,Ohio St,593;1,p...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3173</th>
      <td>20150225234500-205</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>connectsavannah.com</td>
      <td>http://www.connectsavannah.com/NewsFeed/archiv...</td>
      <td>None</td>
      <td>None</td>
      <td>TRIAL;TAX_FNCACT;TAX_FNCACT_OFFICER;ARREST;TAX...</td>
      <td>TAX_FNCACT_CHIEF,1686;TAX_FNCACT_CHIEF,1818;AR...</td>
      <td>2#Georgia, United States#AS#USGA#0#0#GA</td>
      <td>...</td>
      <td>wc:423,c12.1:31,c12.10:43,c12.12:7,c12.13:12,c...</td>
      <td>http://www.connectsavannah.com/binary/d74b/Con...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/user/connectsavannah/videos;</td>
      <td>None</td>
      <td>Grand Jury,28;Officer David Jannot,96;Charles ...</td>
      <td>23,citizens whose backgrounds represent,577;5,...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3174</th>
      <td>20150225234500-206</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>lasvegassun.com</td>
      <td>http://lasvegassun.com/news/2015/feb/25/jury-g...</td>
      <td>None</td>
      <td>None</td>
      <td>TRIAL;DEATH_PENALTY;SOC_POINTSOFINTEREST;SOC_P...</td>
      <td>SOC_EXPRESSREGRET,1922;KILL,245;KILL,350;KILL,...</td>
      <td>3#Phoenix, Arizona, United States#US#USAZ#33.4...</td>
      <td>...</td>
      <td>wc:458,c12.1:33,c12.10:48,c12.12:27,c12.13:11,...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/iframe_api;</td>
      <td>1095|56||Why did we go from this sexual encoun...</td>
      <td>Jacques Billeaud,23;Jodi Arias,173;Kirk Nurmi,...</td>
      <td>8,women,645;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3175</th>
      <td>20150225234500-207</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>njherald.com</td>
      <td>http://www.njherald.com/story/28195854/smith-a...</td>
      <td>None</td>
      <td>None</td>
      <td>MEDIA_MSM;TAX_FNCACT;TAX_FNCACT_SINGER;TAX_FNC...</td>
      <td>MANMADE_DISASTER_IMPLIED,1886;REBELLION,2614;R...</td>
      <td>1#United Kingdom#SF#UK#54#-2#UK;4#London, Lond...</td>
      <td>...</td>
      <td>wc:574,c1.1:5,c12.1:47,c12.10:47,c12.12:10,c12...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>3088|38||all the underdogs and all the grafters</td>
      <td>Kanye West,134;Brit Awards,249;For Love,335;Ge...</td>
      <td>12,of dancers,988;</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3176</th>
      <td>20150225234500-208</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>ssuchronicle.com</td>
      <td>http://www.ssuchronicle.com/2015/02/25/the-mia...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_WORLDLANGUAGES;TAX_WORLDLANGUAGES_MIAMI;ME...</td>
      <td>TAX_DISEASE_PARKINSON_DISEASE,2354;TAX_WORLDLA...</td>
      <td>3#Miami, Florida, United States#US#USFL#25.774...</td>
      <td>...</td>
      <td>wc:580,c1.2:2,c12.1:26,c12.10:48,c12.12:22,c12...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Florida Adult Stem Cell Lectures,63;Miami Stem...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3177</th>
      <td>20150225234500-209</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>cw33.com</td>
      <td>http://cw33.com/2015/02/25/the-rant-insanity-v...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_ETHNICITY;TAX_ETHNICITY_AMERICAN;ARMEDCONF...</td>
      <td>SOC_POINTSOFINTEREST_PRISON,1146;TRIAL,112;TAX...</td>
      <td>1#United States#US#US#38#-97#US;2#Texas, Unite...</td>
      <td>...</td>
      <td>wc:217,c12.1:29,c12.10:36,c12.12:16,c12.13:9,c...</td>
      <td>https://tribcw33.files.wordpress.com/2015/02/e...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>609|33||not guilty by reason of insanity?</td>
      <td>Insanity Defense,45;American Sniper,72;Eddie R...</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3178</th>
      <td>20150225234500-210</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>nj.com</td>
      <td>http://www.nj.com/mercer/index.ssf/2015/02/tre...</td>
      <td>None</td>
      <td>None</td>
      <td>TAX_FNCACT;TAX_FNCACT_STUDENTS;EDUCATION;SOC_P...</td>
      <td>TAX_FNCACT_DIRECTOR,1848;EDUCATION,72;EDUCATIO...</td>
      <td>None</td>
      <td>...</td>
      <td>wc:449,c12.1:23,c12.10:37,c12.12:6,c12.13:22,c...</td>
      <td>http://imgick.nj.com/home/njo-media/width620/i...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>Jazmin Sanez,21;Rivera Middle School,67;Trento...</td>
      <td>22,students,638;130000000,dollars Trenton Cent...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3179</th>
      <td>20150225234500-211</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>kaaltv.com</td>
      <td>http://www.KAALtv.com/article/stories/S3717138...</td>
      <td>KILL#2#boys#0######;WOUND#2##0######;</td>
      <td>KILL#2#boys#0#######93;WOUND#2##0#######937;</td>
      <td>KILL;NATURAL_DISASTER;NATURAL_DISASTER_LANDSLI...</td>
      <td>KILL,186;KILL,416;SOC_POINTSOFINTEREST_SCHOOLS...</td>
      <td>None</td>
      <td>...</td>
      <td>wc:188,c12.1:10,c12.10:7,c12.12:4,c12.13:2,c12...</td>
      <td>http://www.kaaltv.com/2014/misc/abc6news-16x9....</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/user/abc6videos;</td>
      <td>None</td>
      <td>Jennie Olson,103;Lilydale Regional Park,174;Mi...</td>
      <td>2,boys were killed,147;152,dollars ,474;100000...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3180</th>
      <td>20150225234500-212</td>
      <td>20150225234500</td>
      <td>1</td>
      <td>billingsgazette.com</td>
      <td>http://billingsgazette.com/news/local/ca593770...</td>
      <td>ARREST#185000000##2#Montana, United States#US#...</td>
      <td>ARREST#185000000##2#Montana, United States#US#...</td>
      <td>TAX_FNCACT;TAX_FNCACT_LEADERS;TAX_WORLDMAMMALS...</td>
      <td>TAX_WORLDMAMMALS_HORSE,177;MANMADE_DISASTER_IM...</td>
      <td>2#Montana, United States#US#USMT#46.9048#-110....</td>
      <td>...</td>
      <td>wc:778,c1.2:2,c12.1:64,c12.10:89,c12.12:35,c12...</td>
      <td>http://bloximages.chicago2.vip.townnews.com/bi...</td>
      <td>None</td>
      <td>None</td>
      <td>https://youtube.com/user/BillingsGazette;</td>
      <td>4788|80||talking to you about what has happene...</td>
      <td>Yellowstone County,64;Treasure State,136;Horse...</td>
      <td>75,Montana prosecutors,1147;37000000,dollars E...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>3181 rows × 27 columns</p>
</div>



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
Add New Fields
'''
```


```python
from StringIO import StringIO
eventMentions = pd.read_csv(StringIO(text),delimiter='\t',header=None)
```


```python
eventMentions.to_csv('../../gdelt2HeaderRows/schema_csvs/GDELT_2.0_eventMentions_Column_Labels_Header_Row_Sep2016.tsv',encoding='utf-8',sep='\t')
```


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
