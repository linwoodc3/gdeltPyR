
# Basic `gdeltPyR` Usage

`gdeltPyR` retrieves [Global Database of Events, Language, and Tone (GDELT) data (version 1.0 or version 2.0) ](http://gdeltproject.org/data.html#intro) via [parallel HTTP GET requests](http://docs.python-requests.org/en/v0.10.6/user/advanced/#asynchronous-requests) and is an alternative to [accessing GDELT data via Google BigQuery ](http://gdeltproject.org/data.html#googlebigquery). 

 Performance will vary based on the number of available cores (i.e. CPUs), internet connection speed, and available RAM.  For systems with limited RAM, Later iterations of `gdeltPyR` will include an option to store the output directly to disc.  

### Memory Considerations

Take your systems specifications into consideration when running large or complex queries.  While `gdeltPyR` loads each temporary file long enough only to convert it into a `pandas` dataframe (15 minutes each for 2.0, full day for 1.0 events tables), GDELT data can be especially large and exhaust a computers RAM.  For example, Global Knowledge Graph (gkg) table queries can eat up large amounts of RAM when pulling data for only a few days.  Before trying month long queries, try single day queries or create a pipeline that pulls several days worth of data, writes to discs, flushes globals, and continues to pull more data.  

### Recommended RAM

It's best to use a system with at least 8 GB of RAM.

# Installation

```bash
pip install gdeltPyR
```

You can also install directly from www.github.com

```bash
pip install git+https://github.com/linwoodc3/gdeltPyR
```

# Basic Usage

[`gdeltPyR`](https://github.com/linwoodc3/gdeltPyR) queries revolve around 4 concepts:



| **Name**    | Description                                                                                                                                                                                                                                                       | Input Possibilities/Examples    |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| version     | (integer)  - Selects the version of GDELT data to query; defaults to version 2.                                                                                                                                                                                   | 1 or 2                          |
| date        | (string or list of strings) - Dates to query                                                                                                                                                                                                                      | "2016 10 23" or "2016 Oct 23"   |
| coverage    | (bool) - For GDELT 2.0, pulls every 15 minute interval in the dates passed in the 'date' parameter. Default coverage is False or None.  `gdeltPyR` will pull the latest 15 minute interval for the current day or the last 15 minute interval for a historic day. | True or False or None           |
| translation | (bool) - For GDELT 2.0, if the english or translated-to-english dataset should be downloaded                                                                                                                                                                      | True or False                   |
| tables      | (string) - The specific GDELT table to pull.  The default table is the 'events' table.  See the [GDELT documentation page for more information](http://gdeltproject.org/data.html#documentation)                                                                  | 'events' or 'mentions' or 'gkg' |
| output      | (string) - The output type for the results                                                                 | 'json' or 'csv' or 'gpd' |


With these basic concepts, you can run any number of GDELT queries.


```python
##############################
# Import the package
##############################
import gdelt
```


```python
###############################
# Instantiate the gdelt object
##############################

gd = gdelt.gdelt(version=2)
```

To launch your query, pass in your dates.  When passing multiple dates, pass as a list of strings.  We will time the multi-day query.  

## Important Date Details for GDELT 1.0 and 2.0
For **GDELT 2.0**, every 15 minute interval is a zipped CSV file, and `gdeltPyR` makes concurrent HTTP GET requests to each file. When the `coverage` parameter is set to *True*, each full day of data has 96 15 minute interval files to pull.  If you are pulling the current day and coverage is set to *True*, `gdeltPyR` all the intervals leading up to the latest 15 minute interval.  When `coverage` is *False*, the package pulls the last 15 minute interval when querying a historical date and the latest 15 minute interval when querying the current date. Additinally, GDELT 2.0 data only goes back as far as Feb 2015.  The [additional features of GDELT 2.0 are discussed here](http://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/). 

**GDELT 1.0** releases the previous day's query at 6AM EST of the next day (if today's current date is 23 Oct, the 22 Oct results would be available at 6AM Eastern on 23 Oct).

# The Query

To launch your query, just pass in dates.  When passing multiple dates, pass as a list of strings.  First, some information on my OS.


```python

import platform
import multiprocessing

print (platform.platform())

print (multiprocessing.cpu_count())
```

    Darwin-16.0.0-x86_64-i386-64bit
    4


And now the query.


```python
%time results = gd.Search(['2016 10 19','2016 10 22'],table='events',coverage=True)
```

    CPU times: user 6.6 s, sys: 2.1 s, total: 8.7 s
    Wall time: 36.8 s


Let's get an idea for the number of results we returned.  


```python
results.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 875062 entries, 0 to 875061
    Data columns (total 61 columns):
    GLOBALEVENTID            875062 non-null int64
    SQLDATE                  875062 non-null int64
    MonthYear                875062 non-null int64
    Year                     875062 non-null int64
    FractionDate             875062 non-null float64
    Actor1Code               795372 non-null object
    Actor1Name               795376 non-null object
    Actor1CountryCode        497655 non-null object
    Actor1KnownGroupCode     12252 non-null object
    Actor1EthnicCode         5780 non-null object
    Actor1Religion1Code      13439 non-null object
    Actor1Religion2Code      3529 non-null object
    Actor1Type1Code          381709 non-null object
    Actor1Type2Code          27289 non-null object
    Actor1Type3Code          674 non-null object
    Actor2Code               637834 non-null object
    Actor2Name               637835 non-null object
    Actor2CountryCode        396044 non-null object
    Actor2KnownGroupCode     10342 non-null object
    Actor2EthnicCode         4950 non-null object
    Actor2Religion1Code      12687 non-null object
    Actor2Religion2Code      3110 non-null object
    Actor2Type1Code          307573 non-null object
    Actor2Type2Code          19698 non-null object
    Actor2Type3Code          471 non-null object
    IsRootEvent              875062 non-null int64
    EventCode                875062 non-null object
    EventBaseCode            875062 non-null object
    EventRootCode            875062 non-null object
    QuadClass                875062 non-null int64
    GoldsteinScale           875051 non-null float64
    NumMentions              875062 non-null int64
    NumSources               875062 non-null int64
    NumArticles              875062 non-null int64
    AvgTone                  875062 non-null float64
    Actor1Geo_Type           875062 non-null int64
    Actor1Geo_FullName       775810 non-null object
    Actor1Geo_CountryCode    776064 non-null object
    Actor1Geo_ADM1Code       776064 non-null object
    Actor1Geo_ADM2Code       474037 non-null object
    Actor1Geo_Lat            775810 non-null float64
    Actor1Geo_Long           775896 non-null float64
    Actor1Geo_FeatureID      776064 non-null object
    Actor2Geo_Type           875062 non-null int64
    Actor2Geo_FullName       622384 non-null object
    Actor2Geo_CountryCode    622564 non-null object
    Actor2Geo_ADM1Code       622564 non-null object
    Actor2Geo_ADM2Code       330724 non-null object
    Actor2Geo_Lat            622384 non-null float64
    Actor2Geo_Long           622447 non-null float64
    Actor2Geo_FeatureID      622564 non-null object
    ActionGeo_Type           875062 non-null int64
    ActionGeo_FullName       853617 non-null object
    ActionGeo_CountryCode    853905 non-null object
    ActionGeo_ADM1Code       853905 non-null object
    ActionGeo_ADM2Code       452205 non-null object
    ActionGeo_Lat            853617 non-null float64
    ActionGeo_Long           853723 non-null float64
    ActionGeo_FeatureID      853905 non-null object
    DATEADDED                875062 non-null int64
    SOURCEURL                875062 non-null object
    dtypes: float64(9), int64(13), object(39)
    memory usage: 407.2+ MB


In ~36 seconds, `gdeltPyR` returned nearly a 900,000 by 61 (rows x columns) Pandas dataframe that only consumes 407.2 MBs of memory.  With the data in a tidy format, GDELT data can be analyzed with any number of [`pandas` data analysis pipelines and techniques](http://pandas.pydata.org/pandas-docs/stable/cookbook.html).
