import numpy as np
import pandas as pd
import json

import time


#find row that contain searched object in 1 column
def find_one_row_in_DataFrame (
        main_df, #DataFrame that contain our object 
        object_to_search_for, #what we need to find
        item_column #name of column to look into for item 
):
    """
        Finds entety that we are looking for in given DataFrame
    """

    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for: 
            return(main_df.iloc[j])
        
        j = j+1

#slower in small files, but faster in big files    
def find_item_in_DataFrame_without_for (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    column_name #name of column to look into for item 
    ):
    """
        Finds entety that we are looking for in given DataFrame
    """
    #looking for the item
    item = main_df[main_df.loc[:, column_name] == object_to_search_for]  
    return(item)

#find many rows that contain searched object in 1 column
def find_rows_in_DataFrame (
        main_df, #DataFrame that contain our object 
        object_to_search_for, #what we need to find
        item_column #name of column to look into for item
):
    """
        Finds all enteties that we are looking for in given DataFrame
    """
    dict_to_work = {}
    
    #loop to find all lines and add them to the 1 dictionary 
    #after that we can create df from it
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            dict_to_work[len(dict_to_work)] = \
                pd.Series(main_df.iloc[j]).T.to_dict()
        j = j+1

    df_to_return = pd.DataFrame.from_dict(dict_to_work, orient="index")
    return(df_to_return)

def extend_list_by_dict_from_df (
    df_to_add, #df that we transform into records and add to list
    list_to_extend, #list that we need to add dict to
):
    """
        Extend list_to_extend w/ df_to_add content \n
        Returns None, so does this operation inplace
    """
    #structuring DataFrame into dict object
    df_to_add = df_to_add.to_json(orient="records", indent=2)
    
    #add info into list
    list_to_extend.extend(json.loads(df_to_add))
    
    return(None)

