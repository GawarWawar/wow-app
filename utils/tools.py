import numpy as np
import pandas as pd
import json

import time

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.add_row as add_row


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
#has drop duplicantes and sort_value on colomn n0
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

def check_character_existence_add_if_not (
    df_characters, #df for all characters (characters table)
    #members of run we need to check if they exist in df_characters
    df_run_members, 
    run_member_counter, #inside counter for the members
    #if we need to create new member, give him this id
    new_members_guild_id 
):
    #find character in the character table
    member_existence = \
        find_item_in_DataFrame_without_for(
            df_characters,
            df_run_members.loc[run_member_counter,"name"],
            "character_name"
        )
        
    #check if this character already exist 
    if member_existence.empty:
        #adding new character to the character_table
        character_id = add_row.id_and_three_columns(
            df_characters,
            dict_w_info={
                #info about that character we need to write
                0:df_run_members.loc[run_member_counter,"name"],
                1:new_members_guild_id,
                2:df_run_members.loc[run_member_counter,"character_class"],
            }
        )
    else:
        #if exist -> getting its id
        character_id = member_existence.iloc[0].at["character_id"] 
    
    return(character_id)