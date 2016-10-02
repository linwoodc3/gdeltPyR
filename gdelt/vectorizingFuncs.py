import pandas as pd
import numpy as np



def vectorizer(function,dateArray):
    helper = np.vectorize(function)
    
    final = helper(dateArray.tolist()).tolist()
    
    if isinstance(final,list):
        
        final = list(set(final))
    elif isinstance(final,str):
        final=final
    else:
        print "Vectorizer"
    
    return final

# Finds the urls from an array of dates


def urlFinder(dataframe,targetDate,col):
    
    return dataframe[col][dataframe[col].str.contains(targetDate)]
    


def vectorizedUrlFinder(function,urlList,frame):
    helper=np.vectorize(function)
    return pd.concat(helper(urlList,frame).tolist())


def downloadVectorizer(function,urlList):
    '''Vectorized function to download urls'''
    helper=np.vectorize(function)
    return pd.concat(helper(urlList).tolist()).reset_index(drop=True)