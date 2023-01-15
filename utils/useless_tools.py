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

def find_many_rows_in_DataFrame_with_for__concat (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    item_column #name of column to look into for item
    ):
    """
        Finds all enteties that we are looking for in given DataFrame
    """
    #start timer
    start_timer = time.perf_counter()

    #declare a variable
    df_to_return = pd.DataFrame(columns=main_df.columns)

    #looking for the item
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            #df_to_return=main_df.iloc[j]
            #df_to_return = df_to_return.transpose()
            s = pd.Series(main_df.iloc[j])
            df_to_return = pd.concat([df_to_return, s.to_frame().T], ignore_index=True) 
        j = j+1
    
    #end_timer
    end_timer = time.perf_counter()
    print(find_many_rows_in_DataFrame_with_for__concat.__name__, " timer =", end_timer-start_timer)
    
    return(df_to_return)

