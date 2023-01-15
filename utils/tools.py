import numpy as np
import pandas as pd
import time

def read_columns_of_the_csv_to_DF (
    file_to_read, #file that we need to read
    columns = False #what columns do we need to read
    ):
    """
        read file with the header and standart separator (,); \n
        return DataFrame with contamination of the columns we gave
    """
    #start timer
    start_timer = time.perf_counter()
    df = pd.read_csv(file_to_read, header = 0, usecols=columns)
    #end timer
    end_timer = time.perf_counter()
    print("read_columns_of_the_csv_to_DF timer =",end_timer-start_timer)
    print(df.columns)
    return(df)

def read_the_file_to_DF (
    file_to_read, #file that we need to read
    file_type = "csv" #what type is our file, that we are reading
    ):
    """
        read file with the header and standart separator (,); \n
        return DataFrame with contamination of the file
    """
    #start timer
    start_timer = time.perf_counter()
    if file_type == "csv":
        df = pd.read_csv(file_to_read)
    elif file_type == "json":
        df = pd.read_json(file_to_read, orient="index")
    else:
        return(print ("Error, we dont suppot such file extention"))
    #end timer
    end_timer = time.perf_counter()
    print("read_the_file_to_DF timer =",end_timer-start_timer)
    return(df)

def find_1_row_in_DataFrame (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    item_column #name of column to look into for item 
    ):
    """
        Finds entety that we are looking for in given DataFrame
    """
    #start timer
    start_timer = time.perf_counter()
    #looking for the item
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            #end_timer
            end_timer = time.perf_counter()
            print("find_item_in_DataFrame timer =", end_timer-start_timer)
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
    #start timer
    start_timer = time.perf_counter()
    #looking for the item
    df_to_return = pd.DataFrame(columns=main_df.columns)
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
    print("find_item_in_DataFrame timer =", end_timer-start_timer)
    return(df_to_return)

def find_many_rows_in_DataFrame_without_concat (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    item_column #name of column to look into for item
    ):
    """
        Finds all enteties that we are looking for in given DataFrame
    """
    #start timer
    start_timer = time.perf_counter()
    #looking for the item
    #dict_to_df = []
    dict_to_df = {}
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            #df_to_return=main_df.iloc[j]
            #df_to_return = df_to_return.transpose()
            s = pd.Series(main_df.iloc[j]).T
            dict_to_df[len(dict_to_df)] = s.to_dict()
        j = j+1
    print (dict_to_df)
    df_to_return = pd.DataFrame.from_records(dict_to_df)
    #end_timer
    end_timer = time.perf_counter()
    print("find_many_rows_in_DataFrame_without_concat timer =", end_timer-start_timer)
    return(df_to_return)

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


column = ["raid id"]
main_df = read_the_file_to_DF(dynamic_database["guilds_table"])
lable = find_1_row_in_DataFrame(main_df,"GGuild", "guild_name")
main_df = read_the_file_to_DF(dynamic_database["characters_table"])
item = find_many_rows_in_DataFrame_without_concat(main_df,lable.loc["guild_id"],"guild_id")
res = item.to_csv("123.csv")
print(item,"\n")


"""
main_df = read_the_file_to_DF(file_to_look_into)
#item = find_item_in_DataFrame(main_df,"raid_1", "raid id")
print(main_df,"\n")

main_df = read_the_file_to_DF(file_to_look_into_csv)
item = find_item_in_DataFrame(main_df,"Heroic Key to the Focusing Iris", "item_name")
item1 = find_item_in_DataFrame1(main_df,"Heroic Key to the Focusing Iris", "item_name")
print(item,"\n", item1)


#bosses = 1
"""