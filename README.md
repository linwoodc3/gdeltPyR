# gdeltPyR
gdeltPyR is a Python-based framework to retrieve [Global Database of Events, Language, and Tone (GDELT) 2.0 data](http://gdeltproject.org/data.html) for analysis in Python Pandas or R dataframes. A user can enter a date, date range (two strings), or individual dates and return a [tidy data set ready for scientific or data-driven exploration](http://vita.had.co.nz/papers/tidy-data.pdf).  

The GDELT Project is the largest, most comprehensive, and highest resolution open database of human society ever created. It monitors print, broadcast, and web news media in over 100 languages from across every country in the world to keep continually updated on breaking developments anywhere on the planet. Its historical archives stretch back to January 1, 1979 and accesses the world’s breaking events and reaction in near-realtime as both the GDELT Event and Global Knowledge Graph update every 15 minutes.  Visit the [GDELT website to learn more about the project](http://gdeltproject.org/#intro).

<p align="center">
  <img src="https://twistedsifter.files.wordpress.com/2015/06/people-tweeting-about-sunrises-over-a-24-hour-period.gif?w=700&h=453">
</p>


### Installation


You can also install directly from www.github.com

```bash
pip install git+https://github.com/linwoodc3/gdeltPyR
```

### Basic Example

```python
import gdelt

gd = gdelt.gdelt(version=2)

%time results = gd.Search(['2016 10 19','2016 10 22'],table='events',coverage=True)
```

Performance on 4 core, MacOS Sierra 10.12 with 16GB of RAM:
* 900,000 by 61 (rows x columns) pandas dataframe returned in 36 seconds
    * data is a merged pandas dataframe of GDELT 2.0 events database data


```bash
git clone git@github.com:linwoodc3/gdeltPyR.git
```


```python
python setup.py install
```

