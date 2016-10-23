import datetime
from functools import partial
from multiprocessing import Pool, cpu_count

import pandas as pd

from gdelt.dateFuncs import (dateRanger, gdeltRangeString)
from gdelt.getHeaders import events1Heads, events2Heads, mentionsHeads, gkgHeads
from gdelt.inputChecks import (dateInputCheck)
from gdelt.parallel import mp_worker
from gdelt.vectorizingFuncs import urlBuilder


# import os
# this_dir, this_filename = os.path.split(__file__)
# CSV_PATH = os.path.join(this_dir, "utils","schema_csvs",
# "GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv")
# print(CSV_PATH)

# print HEADER_PATH = os.path.join(this_dir,"utils","schema_csvs",
# "GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv")

# header = pd.read_csv(HEADER_PATH,delimiter='\t',usecols=['tableId','dataType','Description'])

# print header

##############################
# Core GDELT class
##############################


class gdelt(object):
    """Placeholder string"""

    def __init__(self,
                 gdelt2MasterUrl='http://data.gdeltproject.org/gdeltv2/',
                 gdelt1MasterUrl='http://data.gdeltproject.org/events/',  # index.html, events/20160930.export.CSV.zip
                 version=2.0,
                 cores=cpu_count(),
                 pool=Pool(processes=cpu_count())

                 ):

        self.version = version
        self.cores = cores
        self.pool = pool
        if int(version) == 2:
            self.baseUrl = gdelt2MasterUrl
        elif int(version) == 1:
            self.baseUrl = gdelt1MasterUrl

    ###############################
    # Searcher function for GDELT
    ###############################

    def Search(self,
               date,
               table='events',
               headers=None,
               coverage=None,
               queryTime=datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
               ):
        dateInputCheck(date, self.version)
        self.coverage = coverage
        self.date = date
        version = self.version
        baseUrl = self.baseUrl
        self.table = table
        self.datesString = gdeltRangeString(dateRanger(self.date), version=version, coverage=self.coverage)

        ##################################
        # Partial Functions
        #################################

        v1RangerCoverage = partial(gdeltRangeString, version=1, coverage=True)
        v2RangerCoverage = partial(gdeltRangeString, version=2, coverage=True)
        v1RangerNoCoverage = partial(gdeltRangeString, version=1, coverage=False)
        v2RangerNoCoverage = partial(gdeltRangeString, version=2, coverage=False)

        urlsv2mentions = partial(urlBuilder, version=2, table='mentions')
        urlsv2events = partial(urlBuilder, version=2, table='events')
        urlsv1events = partial(urlBuilder, version=1, table='events')
        urlsv2gkg = partial(urlBuilder, version=2, table='gkg')

        #####################################
        # GDELT Version 2.0 Headers
        #####################################

        if int(self.version) == 2:
            ###################################
            # Download 2.0 Headers
            ###################################

            self.events_columns = events2Heads()
            self.mentions_columns = mentionsHeads()
            self.gkg_columns = gkgHeads()

        #####################################
        # GDELT Version 1.0 Analytics, Header, Downloads
        #####################################


        if int(self.version) == 1:
            if self.table is "mentions":
                raise ('GDELT 1.0 does not have the "mentions" table. Use "events" or "gkg".')
            else:
                pass

            self.events_columns = events1Heads()
            columns = self.events_columns

            if self.table == 'events':

                if self.coverage is True:
                    self.download_list = (urlsv1events(v1RangerCoverage(dateRanger(self.date))))

                # print ("1 events", urlsv1events(self.datesString))
                # print (urlsv2events(v2RangerNoCoverage(dateRanger(self.date))))
                else:
                    self.download_list = (urlsv1events(v1RangerNoCoverage(dateRanger(self.date))))

        #####################################
        # GDELT Version 2.0 Analytics and Download
        #####################################
        elif self.version == 2:

            if self.table == 'events':
                columns = self.events_columns
                if self.coverage is True:
                    print('in coverage')
                    self.download_list = (urlsv2events(v2RangerCoverage(dateRanger(self.date))))
                else:
                    self.download_list = (urlsv2events(v2RangerNoCoverage(dateRanger(self.date))))

            if self.table == 'gkg':
                columns = self.gkg_columns
                if self.coverage is True:
                    print('in coverage')
                    self.download_list = (urlsv2gkg(v2RangerCoverage(dateRanger(self.date))))
                else:
                    self.download_list = (urlsv2gkg(v2RangerNoCoverage(dateRanger(self.date))))
                    # print ("2 gkg", urlsv2gkg(self.datesString))

            if self.table == 'mentions':
                columns = self.mentions_columns
                if self.coverage is True:
                    print('in coverage')
                    self.download_list = (urlsv2mentions(v2RangerCoverage(dateRanger(self.date))))
                else:
                    self.download_list = (urlsv2mentions(v2RangerNoCoverage(dateRanger(self.date))))

                    # print ("2 mentions", urlsv2mentions(self.datesString))

        pool = Pool(processes=cpu_count())

        downloaded_dfs = list(pool.imap_unordered(mp_worker, self.download_list))
        pool.close()
        pool.terminate()
        pool.join()
        results = pd.concat(downloaded_dfs)
        results.reset_index(drop=True, inplace=True)

        results.columns = columns

        self.final = results

        #########################
        # DEBUG Print
        #########################
        # print (self.version, self.table, self.coverage, self.datesString)

        #########################
        # Return the result
        #########################
        return self.final
