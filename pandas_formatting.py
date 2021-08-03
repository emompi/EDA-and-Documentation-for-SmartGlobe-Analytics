import pytz
import pandas as pd
import pymongo
from pymongo import MongoClient
import urllib.parse
from collection_to_pandas import collection_to_pandas                            #collection_to_pandas.py must be included in the working directory

                                                                                 #here we're just entering our login information in order to access the MongoDB servers

username = urllib.parse.quote_plus('redacted')
password = urllib.parse.quote_plus('redacted!')
client = MongoClient('mongodb://%s:%s@redacted' % (username, password))
db = client.redacted

                                                                                 #this is where we format our DataFrame so that we get something that's easier to use

def pandas_formatting():
    
    df = collection_to_pandas((db.record_306).find().sort('time', pymongo.ASCENDING).limit(730))      #We call our function that turns this MOngoDB query into a Pandas DataFrame

    df = df.sort_values(by=['time'])                                             #Sort the DataFrame object by the column named 'time'

    df['time']=(pd.to_datetime(df['time'],unit='ms'))                            #Convert the 'time' column from UTC milliseconds to DateTime format

    df.index = df.time                                                           #Setthe DataFrame's index to the 'time' column

    paris_time = pytz.timezone('Europe/Berlin')                                  

    df.index = df.index.tz_localize(pytz.utc).tz_convert(paris_time)             #converting UTC time to regional Parisian time
    
    df = df.drop(['time'], axis=1)                                               #An index has been created based on DateTime, so the 'time' column is no longer necessary

    df['Temp_Exterieur'] = df.pop('value')                                       #Change the name of the 'value' column to, in this case, 'Temp_Exterieur'

    return df
