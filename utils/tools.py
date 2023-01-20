import numpy as np
import pandas as pd
import time

#change separetor from ", " to ","
def rewrite_wowhead_separator(
    file_to_rewrite, #file which separator we want to change
    path_to_ftw, #path to file to write
    new_path, #path to new file
    sep_style = ", ", #by default common sep from wowhead
    rename_pattern = "_not_wowhead" #what to add to file, "_not_wowhead" for default
):
    df_to_rewrite = pd.read_csv(
        path_to_ftw + "/"+ file_to_rewrite, #combinepath + filename 
        engine='python', 
        sep = sep_style, 
        header=None
    )
    split_file_name = file_to_rewrite.split(".")
    new_path = f"{new_path}/{split_file_name[0]}{rename_pattern}.{split_file_name[1]}"
    df_to_rewrite.to_csv(
        new_path,
        index=False,
        index_label=False,
        header=None     
    )

#transform from csv into DataFrame with forward transposing it`s content
#old name: wowhead_inspired_csv_to_df
def vertical_csv_to_df (
    file_to_read, #file to read from
    path_to_ftr, #path to file to read
    dataframe, #dataframe to write into
    set_indexes_names, #names for the indexes (optional)
):
    dataframe = pd.read_csv(
        path_to_ftr +"/"+file_to_read,  
        header=None
    )
    dataframe = dataframe.set_index([set_indexes_names]) 
    dataframe = dataframe.transpose()
    return dataframe

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

def find_rows_in_DataFrame (
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
        path_to_fstr, #path to file to read
        set_index_names, #names for columns/indexes for ur dataframe
    ):
    #dataframe to combine all of the file content in
    main_df = pd.DataFrame(columns=set_index_names)
    
    #cycle to get every csv-file into our main DataFrame
    for i in files_to_read: 
        df_situational = pd.DataFrame()
        df_situational = vertical_csv_to_df(
            i,
            path_to_fstr,
            df_situational,
            set_index_names
        )
        main_df = pd.concat([main_df,df_situational], ignore_index=True)
        
    return (main_df)

#read many csv to create one csv
#has drop duplicantes and sort_value on colomn n1
#write options: index_label=False, header=False, index=False
def from_many_csv_to_one_csv(
    files_to_read, #list of files to read from
    path_to_fstr, #path to file to read
    file_to_write, #file to write
    path_to_ftw, #path to write file
    set_index_names, #names for columns/indexes for ur dataframe
    transpose_grouped_file=True, #check if new file should be transposed
    options_for_tocsv = {   #options for pd.csv
        "index_label":False,
        "header":False,
        "index":False
    }
):
    main_df = from_many_csv_to_one_df(
        files_to_read=files_to_read,
        path_to_fstr=path_to_fstr,
        set_index_names=set_index_names
    )

    main_df = main_df.drop_duplicates(
        set_index_names[0]
    )
    main_df = main_df.sort_values(
        set_index_names[0]
    )
    
    #transpoe df to make it the same orientation as antecedence files
    if transpose_grouped_file:
        main_df = main_df.transpose()

    main_df.to_csv(
        path_to_ftw+"/"+file_to_write, 
        index_label=options_for_tocsv["index_label"], 
        header=options_for_tocsv["header"], 
        index=options_for_tocsv["index"]
    )



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

#time_my_function
# Class to include timer into given functions
class TMF ():
    def __init__(self) -> None:
        pass
    
    def vertical_csv_to_df (
        file_to_read, #file to read from
        dataframe, #dataframe to write into
        set_indexes_names, #names for the indexes (optional)
        separator #separator into csv file (optional)
    ):
        time_the_function(vertical_csv_to_df (
            file_to_read, #file to read from
            dataframe, #dataframe to write into
            set_indexes_names, #names for the indexes (optional)
            separator #separator into csv file (optional)
        ))
    
    def find_one_row_in_DataFrame (
        main_df, #DataFrame that contain our object 
        object_to_search_for, #what we need to find
        item_column #name of column to look into for item 
    ):
        time_the_function(find_one_row_in_DataFrame (
            main_df,
            object_to_search_for,
            item_column 
        ))
    
    def find_rows_in_DataFrame(
        main_df, #DataFrame that contain our object 
        object_to_search_for, #what we need to find
        item_column #name of column to look into for item
    ):
        time_the_function(find_rows_in_DataFrame(
            main_df, 
            object_to_search_for,
            item_column  
        ))
    
    def from_many_csv_to_one_df(
        self,
        files_to_read, 
        set_index_names, 
        csv_separator
    ):
        time_the_function(from_many_csv_to_one_df(
            files_to_read,
            set_index_names,
            csv_separator
        ))
    
    
    
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