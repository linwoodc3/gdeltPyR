[![Build Status](https://travis-ci.org/linwoodc3/gdeltPyR.svg?branch=master)](https://travis-ci.org/linwoodc3/gdeltPyR)

# gdeltPyR
gdeltPyR is a Python-based framework to access and analyze [Global Database of Events, Language, and Tone (GDELT) 1.0 or 2.0 data](http://gdeltproject.org/data.html) for analysis in Python Pandas or R dataframes. A user can enter a date, date range (two strings), or individual dates and return a [tidy data set ready for scientific or data-driven exploration](http://vita.had.co.nz/papers/tidy-data.pdf).  

`gdeltPyR` retrieves [Global Database of Events, Language, and Tone (GDELT) data (version 1.0 or version 2.0) ](http://gdeltproject.org/data.html#intro) via [parallel HTTP GET requests](http://docs.python-requests.org/en/v0.10.6/user/advanced/#asynchronous-requests) and is an alternative to [accessing GDELT data via Google BigQuery ](http://gdeltproject.org/data.html#googlebigquery). Therefore, the more cores you have, the less time it takes to pull more data.  Moreover, the more RAM you have, the more data you can pull.  And finally, for RAM-limited workflows, create a pipeline that pulls data, writes to disk, and flushes.  

The GDELT Project is the largest, most comprehensive, and highest resolution open database of human society ever created. It monitors print, broadcast, and web news media in over 100 languages from across every country in the world to keep continually updated on breaking developments anywhere on the planet. Its historical archives stretch back to January 1, 1979 and accesses the world’s breaking events and reaction in near-realtime as both the GDELT Event and Global Knowledge Graph update every 15 minutes.  Visit the [GDELT website to learn more about the project](http://gdeltproject.org/#intro).

<p align="center">
  <img src="https://twistedsifter.files.wordpress.com/2015/06/people-tweeting-about-sunrises-over-a-24-hour-period.gif?w=700&h=453">
</p>


### Installation


`gdeltPyR` can be installed via pip

```bash
pip install gdelt
```

### Basic Examples

**GDELT 1.0 Queries**
```python
import gdelt

# Version 1 queries
gd1 = gdelt.gdelt(version=1)

# pull single day, gkg table
results= gd1.Search('2016 Nov 01',table='gkg')
print(len(results))

# pull events table, range, output to json format
results = gd1.Search(['2016 Oct 31','2016 Nov 2'],coverage=True,table='events')
print(len(results))
```
**GDELT 2.0 Queries**
```python
# Version 2 queries
gd2 = gdelt.gdelt(version=2)

# Single 15 minute interval pull, output to json format with mentions table
results = gd2.Search('2016 Nov 1',table='mentions',output='json')
print(len(results))

# Full day pull, output to pandas dataframe, events table
results = gd2.Search(['2016 11 01'],table='events',coverage=True)
print(len(results))


```
## Output Options

`gdeltPyR` can output results directly into several formats which include:
*  pandas dataframe
*  csv
*  json
*  geopandas dataframe *(as of version 0.1.10)*
*  GeoJSON *(coming soon version 0.1.11)*
*  Shapefile *(coming soon version 0.1.11)*



Performance on 4 core, MacOS Sierra 10.12 with 16GB of RAM:
* 900,000 by 61 (rows x columns) pandas dataframe returned in 36 seconds
    * data is a merged pandas dataframe of GDELT 2.0 events database data

## `gdeltPyR` Parameters
`gdeltPyR` provides access to 1.0 and 2.0 data.  Four basic parameters guide the query syntax:

| **Name** | Description                                                                                                                                                                                                                                                       | Input Possibilities/Examples    |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| version  | (integer)  - Selects the version of GDELT data to query; defaults to version 2.                                                                                                                                                                                   | 1 or 2                          |
| date     | (string or list of strings) - Dates to query                                                                                                                                                                                                                      | "2016 10 23" or "2016 Oct 23"   |
| coverage | (bool) - For GDELT 2.0, pulls every 15 minute interval in the dates passed in the 'date' parameter. Default coverage is False or None.  `gdeltPyR` will pull the latest 15 minute interval for the current day or the last 15 minute interval for a historic day. | True or False or None           |
| tables   | (string) - The specific GDELT table to pull.  The default table is the 'events' table.  See the [GDELT documentation page for more information](http://gdeltproject.org/data.html#documentation)                                                                  | 'events' or 'mentions' or 'gkg' |

These parameter values can be mixed and matched to return the data you want.  the `coverage` parameter is used with GDELT version 2; when set to "True", the `gdeltPyR` will query all available 15 minute intervals for the dates passed.  For the current day, the query will return the most recent 15 minute interval. 
  
*Facts*
* GDELT 1.0 is a daily dataset 
     *  1.0 only has 'events' and 'gkg' tables
     *  1.0 posts the previous day's data at 6AM EST of next day (i.e. Monday's data will be available 6AM Tuesday EST)
* GDELT 2.0 is updated every 15 minutes  
     *  2.0 has 'events','gkg', and 'mentions' tables
     *  2.0 has more columns


## Known Issues

*  None

## Coming Soon

* Adding a query for [GDELT Visual Knowledge Graph (VGKG)](http://blog.gdeltproject.org/gdelt-visual-knowledge-graph-vgkg-v1-0-available/)
* Adding a query for [GDELT American Television Global Knowledge Graph (TV-GKG)](http://blog.gdeltproject.org/announcing-the-american-television-global-knowledge-graph-tv-gkg/)