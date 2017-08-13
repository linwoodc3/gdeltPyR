#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##################################
# Standard library imports
##################################
from io import BytesIO

##################################
# Third party imports
##################################
import pandas as pd
import requests


#######################################
# Headers for GDELT 1.0 Events
#######################################



def _events1Heads():
    """

    :rtype: dateframe
    """

    conte = requests.get(
                ("https://raw.githubusercontent.com/linwoodc3/gdeltPyR"
                 "/master/utils/schema_csvs/"
                 "GDELT_1.0_event_Column_Labels_Header_Row_Sep2016.tsv")
            )
    data = BytesIO(conte.content)
    eventsDbHeaders = pd.read_csv(data, delimiter='\t', usecols=['tableId'])

    return eventsDbHeaders['tableId'].tolist()


#######################################
# Headers for GDELT 2.0 Events
#######################################

def _events2Heads():
    conte = requests.get(
        ("https://raw.githubusercontent.com/linwoodc3/gdeltPyR/"
         "master/utils/schema_csvs/"
         "GDELT_2.0_Events_Column_Labels_Header_Row_Sep2016.csv")
    )
    data = BytesIO(conte.content)
    eventsDbHeaders = pd.read_csv(data)

    return eventsDbHeaders['tableId'].tolist()


#######################################
# Headers for GDELT 2.0 Mentions
#######################################

def _mentionsHeads():
    conte = requests.get(
        ("https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/"
         "utils/schema_csvs/"
         "GDELT_2.0_eventMentions_Column_Labels_Header_"
         "Row_Sep2016.tsv")
    )
    data = BytesIO(conte.content)

    eventsDbHeaders = pd.read_csv(data, delimiter='\t',
                                  )
    return eventsDbHeaders['tableId'].tolist()


#######################################
# Headers for GDELT 2.0 GKG
#######################################



def _gkgHeads():

    conte = requests.get(
                ("https://raw.githubusercontent.com/linwoodc3/gdeltPyR/"
                 "master/utils/schema_csvs/"
                 "GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_"
                 "Sep2016.tsv")
            )

    data = BytesIO(conte.content)

    gkgHeaders = pd.read_csv(data
        , delimiter='\t', usecols=['tableId', 'dataType',
                                                 'Description'])
    gkgHeaders.columns = ['tableId', 'dataType',
                               'Description']
    return gkgHeaders.tableId.tolist()
