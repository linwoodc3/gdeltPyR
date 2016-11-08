
Welcome to gdeltPyR's documentation!
====================================

====
gdeltPyR
====

*gdeltPyR is Python based framework to retreive Global Database of Events, 
Language, and Tone (GDELT) version 1.0 and version 2.0 data.*

``gdeltPyR`` has x (4) concepts that govern it's use:

1.  **GDELT Versions**  - the GDELT project has two major versions; 1.0 
    and 2.0.  These versions also drive the instantiation of the ``gdeltPyR``
    searcher object and the format/content of the data returned.  
    The version is set when the object is created:
    ``gd = gdelt.gdelt(version=1)``
    
2.  **"Big Data" collections** like parallel arrays, dataframes, and lists that
    extend common interfaces like *NumPy, Pandas, or Python iterators* to
    larger-than-memory or distributed environments.  These parallel collections
    run on top of the dynamic task schedulers.

Contents:

.. toctree::
:maxdepth: 2

       intro
       tutorial



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

