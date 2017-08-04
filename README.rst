.. -*- mode: rst -*-

.. image:: https://travis-ci.org/linwoodc3/gdeltPyR.svg?branch=master
:target: https://travis-ci.org/linwoodc3/gdeltPyR

.. image:: https://ci.appveyor.com/api/projects/status/yc6u8v6uvg212dcm/branch/master?svg=true
:target: https://ci.appveyor.com/project/linwoodc3/gdeltpyr/history

.. image:: https://badge.fury.io/py/gdelt.svg
:target: https://pypi.python.org/pypi/gdelt

GDELT in Python with ``gdeltPyR``
=================================

``gdeltPyR`` is a Python-based framework to access and analyze `Global Database of Events, Language, and Tone (GDELT) 1.0 and 2.0 <http://gdeltproject.org/data.html>`_ data in a Python Pandas or R dataframe. A user can enter a single date, date range (list of two strings), or individual dates (more than two in a list) and return a `tidy data set ready for scientific or data-driven exploration <http://vita.had.co.nz/papers/tidy-data.pdf>`_.


`gdeltPyR` retrieves `GDELT, 1.0 and 2.0 data, <http://gdeltproject.org/data.html>`_  via `parallel HTTP GET requests <http://docs.python-requests.org/en/v0.10.6/user/advanced/#asynchronous-requests>`_ and will also include a method to  `access GDELT data via Google BigQuery  <http://gdeltproject.org/data.html#googlebigquery>`_. Therefore, the more CPUs or cores you have, the less time it takes to pull more data.  Moreover, the more RAM you have, the more data you can pull.  And finally, for RAM-limited workflows, create a pipeline that pulls data, writes to disc, and flushes.  The only limitation with data pulls ``gdeltPyR`` is you hardware.

The GDELT Project advertises as the largest, most comprehensive, and highest resolution open database of human society ever created. It monitors print, broadcast, and web news media in over 100 languages from across every country in the world to keep continually updated on breaking developments anywhere on the planet. Its historical archives stretch back to January 1, 1979 and accesses the world’s breaking events and reaction in near-realtime as both the GDELT Event and Global Knowledge Graph update every 15 minutes.  Visit the `GDELT website to learn more about the project <(http://gdeltproject.org/#intro)>`_.

GDELT Facts
-----------
* **GDELT 1.0 is a daily dataset**
     *  1.0 only has 'events' and 'gkg' tables
     *  1.0 posts the previous day's data at 6AM EST of next day (i.e. Monday's data will be available 6AM Tuesday EST)
* **GDELT 2.0 is updated every 15 minutes**
     *  Some time intervals in GDELT 2.0 are missing; ``gdeltPyR`` provides a warning message when data is missing
     *  2.0 has 'events','gkg', and 'mentions' tables
     *  2.0 has a distinction between native english and translated-to-english


Project Concept and Evolution Plan
----------------------------------

This project will evolve in `two phases <https://github.com/linwoodc3/gdeltPyR/projects>`_. Moreover, if you want to contribute to the project, this section can help prioritize where to put efforts.

* Phase 1 focuses on providing consistent, stable, and reliable access to GDELT data.

Therefore, most `issues <https://github.com/linwoodc3/gdeltPyR/issues>`_ in this phase will build out the main `Search` class to return `GDELT data, version 1.0 or version 2.0 <http://gdeltproject.org/data.html#intro>`_, or equally important, give a relevant error message when no data is returned.  This also means the project will focus on building documentation, a unit testing framework (shooting for 90% coverage), and creating a helper class that provides helpful information on column names/table descriptions.

* Phase 2 brings analytics to `gdeltPyR` to expand the library beyond a simple data retrieval functionality

This phase is what will make `gdeltPyR` useful to a wider audience. The major addition will be an `Analysis` class.  For the data-literate users (data scientists, researchers, students, data journalists, etc), enhancements in this phase will save time by providing summary statistics and extraction methods of GDELT data, and as a result reduce the time a user would spend writing code to perform routine data cleanup/analysis.  For the non-technical audience (students, journalists, business managers, etc.), enhancesments in this phase will provide outputs that summarize GDELT data, which can in turn be used in reports, articles, etc.  Areas of focus include descriptive statistics (mean, split-apply-combine stats, etc), spatial analysis, and time series.

**New Features**
----------------

1.  Added geodataframe output.  This can be easily converted into a shapefile or `choropleth <https://en.wikipedia.org/wiki/Choropleth_map>`_ visualization.
2.  Added continuous integration testing for Windows, OSX, and Linux (Ubuntu)
3.  Normalized columns output; export data with SQL ready columns (no special characters, all lowercase)
4.  Choosing between the native-english or translated-to-english datasets from GDELT v2.

Coming Soon (version 0.1.11, as of 29 May 2017)
-----------------------------------------------

* Query Google's BigQuery directly from ``gdeltPyR`` using the `pandas.io.gbq` interface; requires authentication and Google Compute account
* Adding a query for `GDELT Visual Knowledge Graph (VGKG) <http://blog.gdeltproject.org/gdelt-visual-knowledge-graph-vgkg-v1-0-available/>`_
* Adding a query for `GDELT American Television Global Knowledge Graph (TV-GKG) <http://blog.gdeltproject.org/announcing-the-american-television-global-knowledge-graph-tv-gkg/>`_

Installation
------------

Latest release installs from PyPi::

    pip install gdelt

Latest dev version of ``gdeltPyR`` can be installed from GitHub.com::

    pip install git+https://github.com/linwoodc3/gdeltPyR
    
    


.. image:: https://twistedsifter.files.wordpress.com/2015/06/people-tweeting-about-sunrises-over-a-24-hour-period.gif?w=700&h=453
:alt: GDELT can help you visualize the world's news!!!  Analyze GDELT data with gdeltPyR!!
    
Basic Usage
-----------

.. code-block:: python

    #############################
    # Import gdeltPyR; instantiate
    #############################
    
    import gdelt
    
    gd = gdelt.gdelt(version=2)
    
    results = gd.Search(['2016 10 19','2016 10 22'],table='events',coverage=True,translation=False)

    


Contributing to gdelPyR
-----------------------

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.

A detailed overview on how to contribute is forthcoming.

Our main requirement (and advice) is to make sure you write a unit  test for your enhancement or addition (or write a new unit test to help us reach 90% coverage).  Moreover, we can't accept a commit until existing unittests are passing in Travis CI (OSX and Linux) and Appveyor (Windows).

If you are simply looking to start working with the ``gdeltPyR`` codebase, navigate to the `GitHub issues <(https://github.com/linwoodc3/gdeltPyR/issues)>`_ tab and start looking through interesting issues. There are a number of issues listed where you could start out.

Or maybe through using gdeltPyR you have an idea of your own or are looking for something in the documentation and thinking ``this can be improved``...you can do something about it!

gdelPyR Dev Environment
-----------------------

We advise using the `pandas <https://pandas.pydata.org/pandas-docs/stable/contributing.html#getting-started-with-git>`_ instructions as a guide to build a ``gdeltPyR`` development environment.  Just replace ``gdeltPyR`` project urls with ``pandas`` urls and you should be up and running.


Styles for Submitting Issues/Pull Requests
------------------------------------------
We follow the `pandas <https://pandas.pydata.org/pandas-docs/stable/contributing.html#contributing-your-changes-to-pandas>`_  coding style for issues and pull requests.  Use the following style:

* ENH: Enhancement, new functionality
* BUG: Bug fix
* DOC: Additions/updates to documentation
* TST: Additions/updates to tests
* BLD: Updates to the build process/scripts
* PERF: Performance improvement
* CLN: Code cleanup

See `this issue as an example <https://github.com/linwoodc3/gdeltPyR/issues/8>`_.