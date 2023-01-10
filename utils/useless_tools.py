import numpy as np
import pandas as pd
import time

#This is slower, but let it be
def find_item_in_DataFrame_without_for (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    column_name #name of column to look into for item 
    ):
    """
        Finds entety that we are looking for in given DataFrame
    """
    #start timer
    start_timer = time.perf_counter()
    #looking for the item
    item = main_df[main_df.loc[:, column_name] == object_to_search_for]  
    #end_timer
    end_timer = time.perf_counter()
    print("find_item_in_DataFrame_without_for timer =", end_timer-start_timer)
    return(item)