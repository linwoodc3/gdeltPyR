from gdelt.vectorizingFuncs import vectorizer
from dateutil.parser import parse
import numpy as np 
import datetime




def parse_date(var):
    """Return datetime object from string."""
    
    try:
        return np.where(isinstance(parse(var),datetime.datetime),
                 parse(var),"Error")             
    except:
        return "You entered an incorrect date.  Check your date format."


def dateFormatter(datearray):
    """Function to format strings for numpy arange"""
    return parse(datearray).strftime("%Y-%m-%d")
    

def dateRanger(originalArray):
    """Function to vectorize date formatting function.
    Creates datetime.date objects for each day in the range
    and stores in a numpy array.
    
    Example
    
    Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Input data, where ``n_samples`` is the number of samples and
            ``n_features`` is the number of features.
    Returns
    -------
    self : object
        Returns self.
    """
    if isinstance(originalArray,str):
        """Check user input to retrieve date query."""
    
        return np.where(len(originalArray)==0,np.array(datetime.datetime.now()),
                 parse_date(originalArray))
    
    elif isinstance(originalArray,list):
        if len(originalArray)==1:
            return np.array(parse("".join(originalArray)))
        elif len(originalArray)>2:
            return np.array(map(parse,originalArray),dtype='datetime64[D]')
        else:
            cleaner = np.vectorize(dateFormatter)
            converted = cleaner(originalArray).tolist()
            dates = np.arange(converted[0],converted[1],dtype='datetime64[D]')
            dates = np.append(dates,np.datetime64(datetime.date.today())) # numpy range is not endpoint inclusive
            return dates

def gdeltRangeString(element):
    if element == datetime.date.today():
        multiplier = datetime.datetime.now().minute / 15
        multiple = 15 * multiplier
        converted = datetime.datetime.now().replace(minute=multiple,second=0)
    else:
        converted = (datetime.datetime.combine(element,datetime.time.min) + 
            datetime.timedelta(minutes=45,hours=23))
        
    
    converted = np.where((converted >= parse('2013 04 01')),converted.strftime('%Y%m%d%H%M%S')[:8],
                  np.where((converted <parse('2006 01 01')),
                           converted.strftime('%Y%m%d%H%M%S')[:4],converted.strftime('%Y%m%d%H%M%S')[:6]))
    
    
    # try:
    #     print converted.tolist(),"Yes"
    # except:
    #     print converted,"Changed"
        
    if parse(converted.tolist()).date() == datetime.date.today():
        pass
    else:
        return converted

    




def dateMasker(dateString, version):
    mask = (np.where((int(version == 1) and parse(dateString)>=parse('2013 04 01')) or (int(version)==2),
         vectorizer(gdeltRangeString,dateRanger(dateString))[:8],
        np.where(int(version)==1 and parse(dateString)<parse('2006 01'),
                 vectorizer(gdeltRangeString,dateRanger(dateString))[:4],
                 vectorizer(gdeltRangeString,dateRanger(dateString))[:6]))).tolist()
    return mask
