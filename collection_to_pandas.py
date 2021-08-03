# We use this function to take a MongoDB search and return a Pandas DataFrame


import pandas as pd

def collection_to_pandas(mongo_query_results):  #take Mongo query as argument

    list_of_values = []                         #create empty list 

    def add_to_list_of_values(data):            #define a recursive function to search through the dictionaries and lists until we find our final dictionary within a list

        for key, value in data.items():         #searching within a dictionary

            if isinstance(value, dict):         #if element is dictionary, 

                add_to_list_of_values(value)    #recursion

            elif type(value)==list:             #when we find an element that is a list

                for p in value:                 #for each element in the list (of which there is only one)

                    list_of_values.append(p)    #the dictionary contained within is added as an element of list_of_values

        return list_of_values

    for doc in mongo_query_results:             #for each dictionary in the Mongo query results

        add_to_list_of_values(doc)              #we run our recursive function
        
    return pd.DataFrame(list_of_values)         #and we return a Pandas DataFrame object created from list_of_values
