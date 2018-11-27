#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com


##################################
# Standard library imports
##################################

import datetime
import json
import multiprocessing.pool
import os
import re
from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd
import requests

##################################
# Local imports
##################################
from gdelt.dateFuncs import (_dateRanger, _gdeltRangeString)
from gdelt.getHeaders import _events1Heads, _events2Heads, _mentionsHeads, \
    _gkgHeads
from gdelt.helpers import _cameos, _tableinfo
from gdelt.inputChecks import (_date_input_check)
from gdelt.parallel import _mp_worker
from gdelt.vectorizingFuncs import _urlBuilder, _geofilter


##################################
# Third party imports
##################################


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    @property
    def _get_daemon(self):  # pragma: no cover
        return False

    def _set_daemon(self, value):  # pragma: no cover
        pass

    daemon = property(_get_daemon, _set_daemon)


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class NoDaemonProcessPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


##############################################
#  Admin to load local files
##############################################


this_dir, this_filename = os.path.split(__file__)
BASE_DIR = os.path.dirname(this_dir)

UTIL_FILES_PATH = os.path.join(BASE_DIR, "gdeltPyR", "utils", "schema_csvs")

try:

    codes = pd.read_json(os.path.join(BASE_DIR, 'data', 'cameoCodes.json'),
                         dtype=dict(cameoCode='str', GoldsteinScale=np.float64))
    codes.set_index('cameoCode', drop=False, inplace=True)

except:  # pragma: no cover
    a = 'https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master' \
        '/utils/' \
        'schema_csvs/cameoCodes.json'
    codes = json.loads((requests.get(a).content.decode('utf-8')))

##############################
# Core GDELT class
##############################


class gdelt(object):
    """GDELT Object
        Read more in the :ref:`User Guide <k_means>`.

        Attributes
        ----------
        version : int, optional, {2,1}
            The version of GDELT services used by gdelt. 1 or 2
        gdelt2url : string,default: http://data.gdeltproject.org/gdeltv2/
            Base url for GDELT 2.0 services.
        gdelt1url : string, default: http://data.gdeltproject.org/events/
            Base url for GDELT 1.0 services.
        cores : int, optional, default: system-generated
            Count of total CPU cores available.
        pool: function
            Standard multiprocessing function to establish Pool workers
        proxies: dict
            Dictionary containing proxy information for the requests module.
            For details on how to set, see
            http://docs.python-requests.org/en/master/user/advanced/#proxies
            Example:
                >>>proxies = {'http': 'http://10.10.1.10:3128',\
                'https': 'http://10.10.1.10:1080'}
                >>> requests.get('http://example.org', proxies=proxies)
                Or with a password or specific schema
                >>>proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
                >>>proxies = {'http://10.20.1.128': 'http://10.10.1.10:5323'}


        # TODO add abiity to pick custom time windows

        Examples
        --------
        >>> from gdelt
        >>> gd = gdelt.gdelt(version=2)
        >>> results = gd.Search(['2016 10 19'],table='events',coverage=True)
        >>> print(len(results))
        244767
        >>> print(results.columns)
        Index(['GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate',
       'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode',
       'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code',
       'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 'Actor2Code',
       'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode',
       'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code',
       'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code', 'IsRootEvent',
       'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass',
       'GoldsteinScale', 'NumMentions', 'NumSources', 'NumArticles', 'AvgTone',
       'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode',
       'Actor1Geo_ADM1Code', 'Actor1Geo_ADM2Code', 'Actor1Geo_Lat',
       'Actor1Geo_Long', 'Actor1Geo_FeatureID', 'Actor2Geo_Type',
       'Actor2Geo_FullName', 'Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code',
       'Actor2Geo_ADM2Code', 'Actor2Geo_Lat', 'Actor2Geo_Long',
       'Actor2Geo_FeatureID', 'ActionGeo_Type', 'ActionGeo_FullName',
       'ActionGeo_CountryCode', 'ActionGeo_ADM1Code', 'ActionGeo_ADM2Code',
       'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID', 'DATEADDED',
       'SOURCEURL'],
       dtype='object')


        Notes
        ------
        gdeltPyR retrieves Global Database of Events, Language, and Tone
        (GDELT) data (version 1.0 or version 2.0) via parallel HTTP GET
        requests and is an alternative to accessing GDELT
        data via Google BigQuery .

        Performance will vary based on the number of available cores
        (i.e. CPUs), internet connection speed, and available RAM. For
        systems with limited RAM, Later iterations of gdeltPyR will include
        an option to store the output directly to disc.
        """

    def __init__(self,
                 gdelt2url='http://data.gdeltproject.org/gdeltv2/',
                 gdelt1url='http://data.gdeltproject.org/events/',
                 version=2.0,
                 cores=cpu_count(),
                 proxies=None

                 ):

        self.codes = codes
        self.translation = None
        self.version = version
        self.cores = cores
        self.proxies = proxies
        if int(version) == 2:
            self.baseUrl = gdelt2url
        elif int(version) == 1:
            self.baseUrl = gdelt1url
        self.proxies = proxies
        if proxies:
            if isinstance(proxies, dict):
                self.proxies = proxies
            else:
                raise TypeError("The proxies parameter must be a dictionary. "
                                "See http://docs.python-requests.org/en/master/"
                                "user/advanced/#proxies for more information.")


    ###############################
    # Searcher function for GDELT
    ###############################

    def Search(self,
               date,
               table='events',
               coverage=False,
               translation=False,
               output=None,
               queryTime=datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
               normcols=False
               ):
        """Core searcher method to set parameters for GDELT data searches

        Keyword arguments
        ----------
        date : str, required
            The string representation of a datetime (single) or date
            range (list of strings) that is (are) the targeted timelines to
            pull GDELT data.

        table : string,{'events','gkg','mentions'}
            Select from the table formats offered by the GDELT service:

                * events (1.0 and 2.0)

                    The biggest difference between 1.0 and 2.0 are the
                    update frequencies.  1.0 data is disseminated daily,
                    and the most recent data will be published at 6AM
                    Eastern Standard time of the next day. So, 21 August 2016
                    results would be available 22 August 2016 at 6AM EST.  2.0
                    data updates every 15 minutes of the current day.


                    Version 1.0  runs from January 1, 1979 through March 31,
                    2013 contains 57 fields for each record. The Daily
                    Updates  collection, which begins April 1, 2013 and runs
                    through present, contains an additional field at the end
                    of each record, for a total of 58 fields for each
                    record. The format is dyadic CAMEO format, capturing two
                    actors and the action performed by Actor1 upon Actor2.

                    Version 2.0 only covers February 19, 2015 onwards,
                    and is stored in an expanded version of the dyadic CAMEO
                    format .  See
                    http://data.gdeltproject.org/documentation/GDELT-Event_
                    Codebook-V2.0.pdf for more information.

                * gkg  (1.0 and 2.0)

                    **Warning** These tables and queries can be extremely
                    large and consume a lot of RAM. Consider running a
                    single days worth of gkg pulls, store to disc,
                    flush RAM, then proceed to the next day.

                    Table that represents all of the latent dimensions,
                    geography, and network structure of the global news. It
                    applies an array of highly sophisticated natural language
                    processing algorithms to each document to compute a range
                    of codified metadata encoding key latent and contextual
                    dimensions of the document.  Version 2.0 includes Global
                    Content Analysis Measures (GCAM) which reportedly
                    provides 24 emotional measurement packages that assess
                    more than 2,300 emotions and themes from every article
                    in realtime, multilingual  dimensions natively assessing
                    the emotions of 15 languages (Arabic, Basque, Catalan,
                    Chinese, French, Galician, German, Hindi, Indonesian,
                    Korean, Pashto, Portuguese, Russian, Spanish,
                    and Urdu).See documentation about GKG
                    1.0 at http://data.gdeltproject.org/documentation/GDELT-
                    Global_Knowledge_Graph_Codebook.pdf, and GKG 2.0 at http://
                    data.gdeltproject.org/documentation/GDELT-Global_Knowledge_
                    Graph_Codebook-V2.1.pdf.

                * mentions  (2.0 only)

                     Mentions table records every mention
                     of an event over time, along with the timestamp the
                     article was published. This allows the progression of
                     an event   through the global media to be tracked,
                     identifying  outlets that tend to break certain kinds
                     of events the  earliest or which may break stories
                     later but are more  accurate in their reporting on
                     those events. Combined  with the 15 minute update
                     resolution and GCAM, this also  allows the emotional
                     reaction and resonance of an event to be assessed as
                     it sweeps through the world’s media.

        coverage : bool, default: False
            When set to 'True' and the GDELT version parameter is set to 2,
            gdeltPyR will pull back every 15 minute interval in the day (
            full results) or, if pulling for the current day, pull all 15
            minute intervals up to the most recent 15 minute interval of the
            current our.  For example, if the current date is 22 August,
            2016 and the current time is 0828 HRs Eastern, our pull would
            get pull every 15 minute interval in the day up to 0815HRs.
            When coverate is set to true and a date range is entered,
            we pull every 15 minute interval for historical days and up to
            the most recent 15 minute interval for the current day, if that
            day is included.
            
        translation : bool, default: False
            Whether or not to pull the translation database available from
            version 2 of GDELT. If translation is True, the translated set
            is downloaded, if set to False the english set is downloaded. 

        queryTime : datetime object, system generated
            This records the system time when gdeltPyR's query was executed,
            which can be used for logging purposes.

        output : string, {None,'df','gpd','shp','shapefile', 'json', 'geojson'
                'r','geodataframe'}
            Select the output format for the returned GDELT data

            Options
            -------

            json - Javascript Object Notation output; returns list of
            dictionaries in Python or a list of json objects

            r - writes the cross language dataframe to the current directory.
            This uses the Feather library found at https://github.com/wesm/
            feather.  This option returns a pandas dataframe but write the R
            dataframe to the current working directory. The filename
            includes all the parameters used to launch the query: version,
            coverage, table name, query dates, and query time.

            csv- Outputs a CSV format; all dates and columns are joined
            
            shp- Writes an ESRI shapefile to current directory or path; output
            is filtered to exclude rows with no latitude or longitude
            
            geojson- 
            
            geodataframe- Returns a geodataframe; output is filtered to exclude
            rows with no latitude or longitude.  This output can be manipulated
            for geoprocessing/geospatial operations such as reprojecting the 
            coordinates, creating a thematic map (choropleth map), merging with
            other geospatial objects, etc.  See http://geopandas.org/ for info.

        normcols : bool
            Applies a generic lambda function to normalize GDELT columns 
            for compatibility with SQL or Shapefile outputs.  
        Examples
        --------
        >>> from gdelt
        >>> gd = gdelt.gdelt(version=1)
        >>> results = gd.Search(['2016 10 19'],table='events',coverage=True)
        >>> print(len(results))
        244767
        >>> gd = gdelt.gdelt(version=2)
        >>> results = gd.Search(['2016 Oct 10'], table='gkg')
        >>> print(len(results))
        2398
        >>> print(results.V2Persons.ix[2])
        Juanita Broaddrick,1202;Monica Lewinsky,1612;Donald Trump,12;Donald
        Trump,244;Wolf Blitzer,1728;Lucianne Goldberg,3712;Linda Tripp,3692;
        Bill Clinton,47;Bill Clinton,382;Bill Clinton,563;Bill Clinton,657;Bill
         Clinton,730;Bill Clinton,1280;Bill Clinton,2896;Bill Clinton,3259;Bill
          Clinton,4142;Bill Clinton,4176;Bill Clinton,4342;Ken Starr,2352;Ken
          Starr,2621;Howard Stern,626;Howard Stern,4286;Robin Quivers,4622;
          Paula Jones,3187;Paula Jones,3808;Gennifer Flowers,1594;Neil Cavuto,
          3362;Alicia Machado,1700;Hillary Clinton,294;Hillary Clinton,538;
          Hillary Clinton,808;Hillary Clinton,1802;Hillary Clinton,2303;Hillary
           Clinton,4226
        >>> results = gd.Search(['2016 Oct 10'], table='gkg',output='r')

        Notes
        ------
        Read more about GDELT data at http://gdeltproject.org/data.html

        gdeltPyR retrieves Global Database of Events, Language, and Tone
        (GDELT) data (version 1.0 or version 2.0) via parallel HTTP GET
        requests and is an alternative to accessing GDELT
        data via Google BigQuery.

        Performance will vary based on the number of available cores
        (i.e. CPUs), internet connection speed, and available RAM. For
        systems with limited RAM, Later iterations of gdeltPyR will include
        an option to store the output directly to disc.

        """

        # check for valid table names; fail early
        valid = ['events', 'gkg', 'vgkg', 'iatv', 'mentions']
        if table not in valid:
            raise ValueError('You entered "{}"; this is not a valid table name.'
                             ' Choose from "events", "mentions", or "gkg".'
                .format(table))

        _date_input_check(date, self.version)
        self.coverage = coverage
        self.date = date
        version = self.version
        baseUrl = self.baseUrl
        self.queryTime = queryTime
        self.table = table
        self.translation = translation
        self.datesString = _gdeltRangeString(_dateRanger(self.date),
                                            version=version,
                                            coverage=self.coverage)


        #################################
        # R dataframe check; fail early
        #################################
        if output == 'r':  # pragma: no cover
            try:
                import feather

            except ImportError:
                raise ImportError(('You need to install `feather` in order '
                                   'to output data as an R dataframe. Keep '
                                   'in mind the function will return a '
                                   'pandas dataframe but write the R '
                                   'dataframe to your current working '
                                   'directory as a `.feather` file.  Install '
                                   'by running\npip install feather\nor if '
                                   'you have Anaconda (preferred)\nconda '
                                   'install feather-format -c conda-forge\nTo '
                                   'learn more about the library visit https:/'
                                   '/github.com/wesm/feather'))

        ##################################
        # Partial Functions
        #################################

        v1RangerCoverage = partial(_gdeltRangeString, version=1,
                                   coverage=True)
        v2RangerCoverage = partial(_gdeltRangeString, version=2,
                                   coverage=True)
        v1RangerNoCoverage = partial(_gdeltRangeString, version=1,
                                     coverage=False)
        v2RangerNoCoverage = partial(_gdeltRangeString, version=2,
                                     coverage=False)
        urlsv1gkg = partial(_urlBuilder, version=1, table='gkg')
        urlsv2mentions = partial(_urlBuilder, version=2, table='mentions', translation=self.translation)
        urlsv2events = partial(_urlBuilder, version=2, table='events', translation=self.translation)
        urlsv1events = partial(_urlBuilder, version=1, table='events')
        urlsv2gkg = partial(_urlBuilder, version=2, table='gkg', translation=self.translation)

        eventWork = partial(_mp_worker, table='events', proxies=self.proxies)
        codeCams = partial(_cameos, codes=codes)

        #####################################
        # GDELT Version 2.0 Headers
        #####################################

        if int(self.version) == 2:
            ###################################
            # Download 2.0 Headers
            ###################################

            if self.table =='events':
                try:
                    self.events_columns = \
                    pd.read_csv(os.path.join(BASE_DIR, "data", 'events2.csv'))[
                        'name'].values.tolist()

                except:  # pragma: no cover
                    self.events_columns = _events2Heads()

            elif self.table == 'mentions':
                try:
                    self.mentions_columns = \
                        pd.read_csv(
                            os.path.join(BASE_DIR, "data", 'mentions.csv'))[
                            'name'].values.tolist()

                except:  # pragma: no cover
                    self.mentions_columns = _mentionsHeads()
            else:
                try:
                    self.gkg_columns = \
                        pd.read_csv(
                            os.path.join(BASE_DIR, "data", 'gkg2.csv'))[
                            'name'].values.tolist()

                except:  # pragma: no cover
                    self.gkg_columns = _gkgHeads()

        #####################################
        # GDELT Version 1.0 Analytics, Header, Downloads
        #####################################

        if int(self.version) == 1:

            if self.table is "mentions":
                raise ValueError('GDELT 1.0 does not have the "mentions"'
                                    ' table. Specify the "events" or "gkg"'
                                    'table.')
            if self.translation:
                raise ValueError('GDELT 1.0 does not have an option to'
                                    ' return translated table data. Switch to '
                                    'version 2 by reinstantiating the gdelt '
                                    'object with <gd = gdelt.gdelt(version=2)>')
            else:
                pass

            try:
                self.events_columns = \
                    pd.read_csv(os.path.join(BASE_DIR, "data", 'events1.csv'))[
                        'name'].values.tolist()

            except:  # pragma: no cover
                self.events_columns = _events1Heads()

            columns = self.events_columns

            if self.table == 'gkg':
                self.download_list = (urlsv1gkg(v1RangerCoverage(
                    _dateRanger(self.date))))

            elif self.table == 'events' or self.table == '':

                if self.coverage is True:  # pragma: no cover

                    self.download_list = (urlsv1events(v1RangerCoverage(
                        _dateRanger(self.date))))

                else:
                    # print("I'm here at line 125")
                    self.download_list = (urlsv1events(v1RangerNoCoverage(
                        _dateRanger(self.date))))

            else:  # pragma: no cover
                raise Exception('You entered an incorrect table type for '
                                'GDELT 1.0.')
        #####################################
        # GDELT Version 2.0 Analytics and Download
        #####################################
        elif self.version == 2:

            if self.table == 'events' or self.table == '':
                columns = self.events_columns
                if self.coverage is True:  # pragma: no cover

                    self.download_list = (urlsv2events(v2RangerCoverage(
                        _dateRanger(self.date))))
                else:

                    self.download_list = (urlsv2events(v2RangerNoCoverage(
                        _dateRanger(self.date))))

            if self.table == 'gkg':
                columns = self.gkg_columns
                if self.coverage is True:  # pragma: no cover

                    self.download_list = (urlsv2gkg(v2RangerCoverage(
                        _dateRanger(self.date))))
                else:
                    self.download_list = (urlsv2gkg(v2RangerNoCoverage(
                        _dateRanger(self.date))))
                    # print ("2 gkg", urlsv2gkg(self.datesString))

            if self.table == 'mentions':
                columns = self.mentions_columns
                if self.coverage is True:  # pragma: no cover

                    self.download_list = (urlsv2mentions(v2RangerCoverage(
                        _dateRanger(self.date))))

                else:

                    self.download_list = (urlsv2mentions(v2RangerNoCoverage(
                        _dateRanger(self.date))))


        #########################
        # DEBUG Print Section
        #########################


        # if isinstance(self.datesString,str):
        #     if parse(self.datesString) < datetime.datetime.now():
        #         self.datesString = (self.datesString[:8]+"234500")
        # elif isinstance(self.datesString,list):
        #     print("it's a list")
        # elif isinstance(self.datesString,np.ndarray):
        #     print("it's an array")
        # else:
        #     print("don't know what it is")
        # print (self.version,self.download_list,self.date, self.table, self.coverage, self.datesString)
        #
        # print (self.download_list)
        # if self.coverage:
        #     coverage = 'True'
        # else:
        #     coverage = 'False'
        # if isinstance(self.date, list):
        #
        #     formattedDates = ["".join(re.split(' |-|;|:', l)) for l in
        #                       self.date]
        #     path = formattedDates
        #     print("gdeltVersion_" + str(self.version) +
        #           "_coverage_" + coverage + "_" +
        #           "_table_" + self.table + '_queryDates_' +
        #           "_".join(path) +
        #           "_queryTime_" +
        #           datetime.datetime.now().strftime('%m-%d-%YT%H%M%S'))
        # else:
        #     print("gdeltVersion_" + str(self.version) +
        #           "_coverage_" + coverage + "_" +
        #           "_table_" + self.table + '_queryDates_' +
        #           "".join(re.split(' |-|;|:', self.date)) +
        #           "_queryTime_" +
        #           datetime.datetime.now().strftime('%m-%d-%YT%H%M%S'))

        #########################
        # Download section
        #########################
        # print(self.download_list,type(self.download_list))

        # from gdelt.extractors import normalpull
        # e=ProcessPoolExecutor()
        # if isinstance(self.download_list,list) and len(self.download_list)==1:
        #     from gdelt.extractors import normalpull
        #
        #     results=normalpull(self.download_list[0],table=self.table)
        # elif isinstance(self.download_list,list):
        #     print(table)
        #     multilist = list(e.map(normalpull,self.download_list))
        #     results = pd.concat(multilist)
        # print(results.head())

        if isinstance(self.datesString, str):
            if self.table == 'events':

                results = eventWork(self.download_list)
            else:
                # if self.table =='gkg':
                #     results = eventWork(self.download_list)
                #
                # else:
                results = _mp_worker(self.download_list, proxies=self.proxies)

        else:

            if self.table == 'events':

                pool = Pool(processes=cpu_count())
                downloaded_dfs = list(pool.imap_unordered(eventWork,
                                                          self.download_list))
            else:

                pool = NoDaemonProcessPool(processes=cpu_count())
                downloaded_dfs = list(pool.imap_unordered(_mp_worker,
                                                          self.download_list,
                                                          ))
            pool.close()
            pool.terminate()
            pool.join()
            # print(downloaded_dfs)
            results = pd.concat(downloaded_dfs)
            del downloaded_dfs
            results.reset_index(drop=True, inplace=True)


        if self.table == 'gkg' and self.version == 1:
            results.columns = results.ix[0].values.tolist()
            results.drop([0], inplace=True)
            columns = results.columns

        # check for empty dataframe
        if results is not None:
            if len(results.columns) == 57:  # pragma: no cover
                results.columns = columns[:-1]

            else:
                results.columns = columns

        # if dataframe is empty, raise error
        elif results is None or len(results) == 0:  # pragma: no cover
            raise ValueError("This GDELT query returned no data. Check "
                             "query parameters and "
                             "retry")

        # Add column of human readable codes; need updated CAMEO
        if self.table == 'events':
            cameoDescripts = results.EventCode.apply(codeCams)

            results.insert(27, 'CAMEOCodeDescription',
                           value=cameoDescripts.values)

        ###############################################
        # Setting the output options
        ###############################################

        # dataframe output
        if output == 'df':
            self.final = results

        # json output
        elif output == 'json':
            self.final = results.to_json(orient='records')

        # csv output
        elif output == 'csv':
            self.final = results.to_csv(encoding='utf-8')

        # geopandas dataframe output
        elif output == 'gpd' or output == 'geodataframe' or output == 'geoframe':
            self.final = _geofilter(results)
            self.final = self.final[self.final.geometry.notnull()]

        # r dataframe output
        elif output == 'r':  # pragma: no cover
            if self.coverage:
                coverage = 'True'
            else:
                coverage = 'False'
            if isinstance(self.date, list):

                formattedDates = ["".join(re.split(' |-|;|:', l)) for l in
                                  self.date]
                path = formattedDates
                outPath = ("gdeltVersion_" + str(self.version) +
                           "_coverage_" + coverage + "_" +
                           "_table_" + self.table + '_queryDates_' +
                           "_".join(path) +
                           "_queryTime_" +
                           datetime.datetime.now().strftime('%m-%d-%YT%H%M%S') +
                           ".feather")
            else:
                outPath = ("gdeltVersion_" + str(self.version) +
                           "_coverage_" + coverage + "_" +
                           "_table_" + self.table + '_queryDates_' +
                           "".join(re.split(' |-|;|:', self.date)) +
                           "_queryTime_" +
                           datetime.datetime.now().strftime('%m-%d-%YT%H%M%S') +
                           ".feather")

            if normcols:
                results.columns = list(map(lambda x: (x.replace('_', "")).lower(), results.columns))

            feather.api.write_dataframe(results, outPath)
            return results

        else:
            self.final = results

        #########################
        # Return the result
        #########################

        # normalized columns
        if normcols:
            self.final.columns = list(map(lambda x: (x.replace('_', "")).lower(), self.final.columns))

        return self.final


    def schema(self,tablename):
        """

        Parameters
        ----------
        :param tablename: str
            Name of table to retrieve desired schema

        Returns
        -------
        :return: dataframe
            pandas dataframe with schema
        """

        return _tableinfo(table=tablename,
                          version=self.version)  # pragma: no cover
