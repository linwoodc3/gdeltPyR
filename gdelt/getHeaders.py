
import pandas as pd
import requests
from StringIO import StringIO

def eventHeads():
    
    eventsDbHeaders = pd.read_csv(
        StringIO(
            requests.get(
                'https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/utils/schema_csvs/GDELT_2.0_Events_Column_Labels_Header_Row_Sep2016.csv'
                ).content))
    return eventsDbHeaders.tableId.tolist()


eventsMentionsHeaders = pd.read_csv(
    StringIO(
        requests.get(
            'https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/utils/schema_csvs/GDELT_2.0_eventMentions_Column_Labels_Header_Row_Sep2016.tsv'
            ).content),delimiter='\t',usecols=['tableId','dataType','Description'])


gkgHeaders = pd.read_csv(
    StringIO(
        requests.get(
            'https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/utils/schema_csvs/GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv'
            ).content),delimiter='\t',usecols=['tableId','dataType','Description'])

gkgHeaders = pd.read_csv(
    '../utils/schema_csvs/GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv',
    delimiter='\t',usecols=['tableId','dataType','Description']
    )
gkgHeaders.tableId.tolist();

eventsDbHeaders = pd.read_csv(requests.get('https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/utils/schema_csvs/GDELT_2.0_Events_Column_Labels_Header_Row_Sep2016.csv').content)'../utils/schema_csvs/GDELT_2.0_Events_Column_Labels_Header_Row_Sep2016.csv',
                         delimiter=',',usecols=['tableId','dataType','Description'])
eventsDbHeaders.tableId.tolist();

mentionsHeaders = pd.read_csv('../utils/schema_csvs/GDELT_2.0_eventMentions_Column_Labels_Header_Row_Sep2016.tsv',
                         delimiter='\t',usecols=['tableId','dataType','Description'])
mentionsHeaders.tableId.tolist();