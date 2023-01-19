import numpy as np
import pandas as pd
import time

def time_the_function (
    function_to_time
):
    start_timer = time.perf_counter()
    result = function_to_time()
    end_timer = time.perf_counter()
    print(function_to_time.__name__, 
          "time =",
          end_timer-start_timer)
    return(result)


def find_1_row_in_DataFrame (
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

def find_many_rows_in_DataFrame (
        main_df, #DataFrame that contain our object 
        object_to_search_for, #what we need to find
        item_column #name of column to look into for item
):
    """
        Finds all enteties that we are looking for in given DataFrame
    """
    dict_to_df = {}
    
    #loop to find all lines and add them to the 1 dictionary 
    #after that we can create df from it
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            dict_to_df[len(dict_to_df)] = pd.Series(main_df.iloc[j]).T.to_dict()
        j = j+1

    df_to_return = pd.DataFrame.from_dict(dict_to_df, orient="index")
    return(df_to_return)

#get data from the different files and write into 1
def from_many_csv_to_one_df (
        files_to_read, #list of files to read from
        set_index_names, #names for columns/indexes for ur dataframe
        csv_separator=None, #separator for csv files (oprional)
    ):
    #dataframe to combine all of the file content in
    main_df = pd.DataFrame(columns=set_index_names)
    #transforming set_index_names for DataFrame.set_index
    set_index_names = [set_index_names]
    
    #cycle to get every csv-file into our main DataFrame
    for i in files_to_read: 
        df_situational = pd.DataFrame()
        df_situational = pd.read_csv(
            i, 
            engine = "python",
            sep = csv_separator, 
            header = None
        )
        df_situational = df_situational.set_index(set_index_names)
        df_situational = df_situational.transpose()
        main_df = pd.concat([main_df,df_situational], ignore_index=True)
        
    return (main_df)
    
"""
static_database = {
    "raid_table" : "Data/Static_database/Wow app - Raid table.csv",
    "boss_table" : "Data/Static_database/Wow app - Bosses table.csv",
    "item_table" : "Data/Static_database/Items.csv"
}

dynamic_database = {
    "guilds_table" : "Data/Dynamic_database/guilds_table.csv",
    "characters_table" : "Data/Dynamic_database/characters_table.csv",
    "runs_table" : "Data/Dynamic_database/runs_of_the_guilds_table.csv",
    "events_table" : "Data/Dynamic_database/events_table.csv"
}

"""