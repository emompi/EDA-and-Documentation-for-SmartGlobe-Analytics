
import pytz
import pandas as pd
import pymongo
from pymongo import MongoClient
import urllib.parse
from collection_to_pandas import collection_to_pandas                            #collection_to_pandas.py must be included in the working directory

                                                                                 #here we're just entering our login information in order to access the MongoDB servers

username = urllib.parse.quote_plus('redacted')
password = urllib.parse.quote_plus('redacted')
client = MongoClient('mongodb://%s:%s@redacted' % (username, password))
db = client.redacted


def collection_selection_and_formatting():

    df = pd.DataFrame()

    df = eval('collection_to_pandas((db.record_'+str(input("Which record would you like to load? "))+').find().sort("time", pymongo.ASCENDING).limit(730))')

    value_name = str(input("What would you like to name your column of values? "))

    def pandas_formatting(df): 
    
        df = df.sort_values(by=['time'])                                           

        df['time']=(pd.to_datetime(df['time'],unit='ms'))                          

        df.index = df.time                                                         

        paris_time = pytz.timezone('Europe/Berlin')                                  
        
        df.index = df.index.tz_localize(pytz.utc).tz_convert(paris_time)           
        
        df = df.drop(['time'], axis=1)                                             
        
        df[value_name] = df.pop('value')                                     
        
        return df

    return pandas_formatting(df)


