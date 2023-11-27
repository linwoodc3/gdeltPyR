.. -*- mode: rst -*-


.. image:: https://ci.appveyor.com/api/projects/status/yc6u8v6uvg212dcm/branch/master?svg=true
    :target: https://ci.appveyor.com/project/linwoodc3/gdeltpyr/history

.. image:: https://badge.fury.io/py/gdelt.svg
    :target: https://pypi.python.org/pypi/gdelt

.. image:: https://coveralls.io/repos/github/linwoodc3/gdeltPyR/badge.svg?branch=master
    :target: https://coveralls.io/github/linwoodc3/gdeltPyR?branch=master

.. image:: https://pepy.tech/badge/gdelt
    :target: https://pepy.tech/project/gdelt

What is gdeltPyR?
=================

``gdeltPyR`` is a Python-based framework to access and analyze `Global Database of Events, Language, and Tone (GDELT) 1.0 and 2.0 <http://gdeltproject.org/data.html>`__ data in a Python Pandas or R dataframe. A user can enter a single date, date range (list of two strings), or individual dates (more than two in a list) and return a `tidy data set ready for scientific or data-driven exploration <http://vita.had.co.nz/papers/tidy-data.pdf>`_.

``gdeltPyR`` retrieves `GDELT, 1.0 and 2.0 data, <http://gdeltproject.org/data.html>`_  via `parallel HTTP GET requests <http://docs.python-requests.org/en/v0.10.6/user/advanced/#asynchronous-requests>`_ and will also include a method to  `access GDELT data via Google BigQuery  <http://gdeltproject.org/data.html#googlebigquery>`_. Therefore, the more CPUs or cores you have, the less time it takes to pull more data.  Moreover, the more RAM you have, the more data you can pull.  And finally, for RAM-limited workflows, create a pipeline that pulls data, writes to disc, and flushes.  The only limitation with data pulls ``gdeltPyR`` is you hardware.

::

 Notice : A word of caution for users of this library, not to discourage use but mainly
 to raise awareness. Researchers and practitioners should consider pros and cons of using
 auto-coded conflict data like GDELT.

 Pros. GDELT excels in breadth and speed. It churns out coded conflict data every 15
 minutes for events across the globe. GDELT codes news articles from global websites
 in multiple languages and provides the source URLs for fact-checking.

 Cons. These benefits introduce risks as well. GDELT’s preference for breadth creates
 a dichotomy of sourcing. It contains data from reliable sources, as well as articles
 from questionable or lesser-known websites.

 Solution. Be careful and think critically when using automatically-coded conflict data
 to support research claims. Watch for duplicate reports, circular reporting, erroneous
 reports, and significant events that rely on a single report from a largely unknown,
 obscure source. This library has a method—the `_rooturl` method in helpers—that can find
 the root url/source for every url in the results; use it wisely! For more reading on the
 advantages and disadvantages of using GDELT, read the following as a start:

     - `The Empirical Use of GDELT Big Data in Academic Research
     - `Political instability patterns are obscured by conflict dataset scope conditions, sources, and coding choices



The GDELT creator claims the project is the largest, most comprehensive, and highest resolution open database of human society ever created. It monitors print, broadcast, and web news media in over 100 languages from across every country in the world to keep continually updated on breaking developments anywhere on the planet. Its historical archives stretch back to January 1, 1979 and accesses the world’s breaking events and reaction in near-realtime as both the GDELT Event and Global Knowledge Graph update every 15 minutes.  Visit the `GDELT website to learn more about the project <(http://gdeltproject.org/#intro)>`_.

GDELT Facts
-----------
* GDELT 1.0 is a daily dataset
     *  Version 1.0 only has 'events' and 'gkg' tables
     *  Version 1.0 posts the previous day's data at 6AM EST of next day (i.e. Monday's data will be available 6AM Tuesday EST)
* GDELT 2.0 is updated every 15 minutes
     *  Some time intervals in GDELT 2.0 are missing; ``gdeltPyR`` provides a warning message when data is missing
     *  Version 2.0 has 'events','gkg', and 'mentions' tables
     *  Version 2.0 has a distinction between native english and translated-to-english


Project Concept and Evolution Plan
----------------------------------

This project will evolve in `two phases <https://github.com/linwoodc3/gdeltPyR/projects>`_. Moreover, if you want to contribute to the project, this section can help prioritize where to put efforts.

* Phase 1 focuses on providing consistent, stable, and reliable access to GDELT data.

Therefore, most `issues <https://github.com/linwoodc3/gdeltPyR/issues>`__ in this phase will build out the main ``Search`` class to return `GDELT data, version 1.0 or version 2.0 <http://gdeltproject.org/data.html#intro>`_, or equally important, give a relevant error message when no data is returned.  This also means the project will focus on building documentation, a unit testing framework (shooting for 90% coverage), and creating a helper class that provides helpful information on column names/table descriptions.

* Phase 2 brings analytics to ``gdeltPyR`` to expand the library beyond a simple data retrieval functionality

This phase is what will make ``gdeltPyR`` useful to a wider audience. The major addition will be an ``Analysis`` class.  For the data-literate users (data scientists, researchers, students, data journalists, etc), enhancements in this phase will save time by providing summary statistics and extraction methods of GDELT data, and as a result reduce the time a user would spend writing code to perform routine data cleanup/analysis.  For the non-technical audience (students, journalists, business managers, etc.), enhancesments in this phase will provide outputs that summarize GDELT data, which can in turn be used in reports, articles, etc.  Areas of focus include descriptive statistics (mean, split-apply-combine stats, etc), spatial analysis, and time series.

Basic Usage of New Schema Query
-------------------------------

.. code-block:: python

    #############################
    # Import gdeltPyR; instantiate
    #############################

    import gdelt

    gd = gdelt.gdelt()

    gd.schema('events')

Coming Next (in version 0.2, as of Oct 2023)
-----------------------------------------------

* Output/store ``gdeltPyR`` results in `parquet format <http://wesmckinney.com/blog/python-parquet-update/>`_ ; efficient columnar storage to reduce memory footprint and optimize loading
* Query Google's BigQuery directly from ``gdeltPyR`` using the `pandas.io.gbq` interface; requires authentication and Google Compute account
* Adding a query for `GDELT Visual Knowledge Graph (VGKG) <http://blog.gdeltproject.org/gdelt-visual-knowledge-graph-vgkg-v1-0-available/>`_
* Adding a query for `GDELT American Television Global Knowledge Graph (TV-GKG) <http://blog.gdeltproject.org/announcing-the-american-television-global-knowledge-graph-tv-gkg/>`_

Installation
------------

Latest release installs from PyPi::

    pip install gdelt

You can also install using ``conda``::

    conda install gdelt



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

If you are simply looking to start working with the ``gdeltPyR`` codebase, navigate to the `Issues <(https://github.com/linwoodc3/gdeltPyR/issues)>`__ tab and start looking through interesting issues. There are a number of issues listed where you could start out.

Or maybe through using ``gdeltPyR`` you have an idea of your own or are looking for something in the documentation and thinking ``this can be improved``...you can do something about it!

gdeltPyR Dev Environment
------------------------

We follow the `pandas <https://pandas.pydata.org/pandas-docs/stable/contributing.html#getting-started-with-git>`__ instructions as a guide to build a ``gdeltPyR`` development environment. Windows users should try the `Windows Dev Environment`_ section below.

An easy way to create a ``gdeltPyR`` development environment is as follows.

* Install either `Anaconda <https://www.continuum.io/downloads>`_ or `miniconda <https://conda.io/miniconda.html>`_
* Make sure that you have `cloned the repository <https://github.com/linwoodc3/gdeltPyR/>`_
* cd to the ``gdeltPyR`` source directory

After completing all steps above, tell conda to create a new environment, named ``gdelt_dev``, or any other name you would like for this environment, by running:


* For Python 3.8

.. code-block:: bash

    conda create -n gdelt_dev python=3.8 -c conda-forge --file travis/requirements_all36.txt


Windows Dev Environment
-----------------------

For Windows, we will again follow the ``pandas`` documentation (let me know if this doesn't work for ``gdeltPyR``).  To build on Windows, you need to have compilers installed to build the extensions. You will need to install the appropriate Visual Studio compilers, VS 2008 for Python 2.7, VS 2010 for 3.4, and VS 2015 for Python 3.5 and 3.6.

or use the Microsoft Visual Studio VC++ compiler for Python. Note that you have to check the x64 box to install the x64 extension building capability as this is not installed by default.

For Python 3.4, you can download and install the Windows 7.1 SDK. Read the references below as there may be various gotchas during the installation.

For Python 3.5 and 3.6, you can download and install the Visual Studio 2015 Community Edition.

Here are some references and blogs:

* https://blogs.msdn.microsoft.com/pythonengineering/2016/04/11/unable-to-find-vcvarsall-bat/
* https://github.com/conda/conda-recipes/wiki/Building-from-Source-on-Windows-32-bit-and-64-bit
* https://cowboyprogrammer.org/building-python-wheels-for-windows/
* https://blog.ionelmc.ro/2014/12/21/compiling-python-extensions-on-windows/
* https://support.enthought.com/hc/en-us/articles/204469260-Building-Python-extensions-with-Canopy

This will create the new environment, and not touch any of your existing environments, **nor any existing Python installation**. It will install all of the basic dependencies of `gdeltPyR`, as well as the development and testing tools. To enter this new environment:

* On Windows

.. code-block:: bash

    activate gdelt_dev


* On Linux/Mac OS

.. code-block:: bash

    source activate gdelt_dev


You will then see a confirmation message to indicate you are in the new development environment.

To view your environments:

.. code-block:: bash

    conda info -e


To return to your home root environment in Windows:

.. code-block:: bash

    deactivate


To return to your home root environment in OSX / Linux:

.. code-block:: bash

    source deactivate


Building gdeltPyR
-------------------

See the `full conda docs here <http://conda.pydata.org/docs>`_.

The last step is installing the gdelt development source into this new directory. First, make sure that you cd into the gdeltPyR source directory using the instructions above.  You have two options to build the code:

*  The best way to develop 'gdeltPyR' is to build the extensions in-place by running:

.. code-block:: bash

    python setup.py build_ext --inplace

If you startup the Python interpreter in the pandas source directory you will call the built C extensions

*  Another very common option is to do a develop install of pandas:

.. code-block:: bash

    python setup.py develop


This makes a symbolic link that tells the Python interpreter to import pandas from your development directory. Thus, you can always be using the development version on your system without being inside the clone directory.

You should have a fully functional development environment!

Continuous Integration
----------------------

``pandas`` has a fantastic write up on Continuous Integration (CI).  Because ``gdeltPyR`` embraces the same CI concepts, please `read pandas introduction and explanation of CI if you have issues <https://pandas.pydata.org/pandas-docs/stable/contributing.html#testing-with-continuous-integration>`__. All builds of your branch or Pull Request should pass with `greens` before it can be merged with the master branch.

.. image:: data/allgreensci.png
    :alt: CI Greens



Committing Your Code
--------------------

There's no point in reinventing the wheel; `read the pandas documentation on committing code for instructions <https://pandas.pydata.org/pandas-docs/stable/contributing.html#contributing-your-changes-to-pandas>`__ on how to contribute to `gdeltPyR`.


Styles for Submitting Issues/Pull Requests
------------------------------------------
We follow the `pandas <https://pandas.pydata.org/pandas-docs/stable/contributing.html#contributing-your-changes-to-pandas>`__  coding style for issues and pull requests.  Use the following style:

* ENH: Enhancement, new functionality
* BUG: Bug fix
* DOC: Additions/updates to documentation
* TST: Additions/updates to tests
* BLD: Updates to the build process/scripts
* PERF: Performance improvement
* CLN: Code cleanup

See `this issue as an example <https://github.com/linwoodc3/gdeltPyR/issues/8>`__
