#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Jan Tschada
# Email: gisfromscratch@live.de

from enum import Enum

class location_type(Enum):
    """Location type
        Defines the different location types.
    """
    UNKNOWN = 0
    COUNTRY = 1
    USSTATE = 2
    USCITY = 3
    WORLDCITY = 4
    WORLDSTATE = 5

class gdelt_location:
    """GDELT location
        Defines a GDELT location.
    """
    def __init__(self, location_typeid=0, name=None, country_code=None, admin1_code=None, lat=None, lon=None, feature_id=None):        
        self.location_type = location_type(int(location_typeid))
        self.location_name = name
        self.country_code = country_code
        self.admin1_code = admin1_code
        self.location_lat = lat
        self.location_lon = lon
        self.feature_id = feature_id
        
    def has_location_type(self, location_type):
        return location_type == self.location_type
    
    def location_type_matches(self, location_types):
        return self.location_type in location_types
    
    def __str__(self):
        return self.location_name
    
class location_filter():
    """Location Filter
        Defines different filters which can be applied on the dataframes.
    """
    def filter_by_type(self, gkg_dataframe, location_type):
        return gkg_dataframe.loc[gkg_dataframe.apply(lambda record: record["GDELT_Locations"].has_location_type(location_type), axis=1)]
    
    def filter_by_types(self, gkg_dataframe, location_types):
        return gkg_dataframe.loc[gkg_dataframe.apply(lambda record: record["GDELT_Locations"].location_type_matches(location_types), axis=1)]

def split_location_entries(locations):
    return [gdelt_location(*location) if 7 == len(location) else gdelt_location() for location in locations]

def split_locations(record):
    return split_location_entries([location.split("#") for location in str(record["Locations"]).split(";")])
