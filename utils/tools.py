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
    print(read_columns_of_the_csv_to_DF.__name__, "timer =",end_timer-start_timer)
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
    print(read_the_file_to_DF.__name__, "timer =",end_timer-start_timer)
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
    #loop to look for the item
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            #end_timer
            end_timer = time.perf_counter()
            print(find_1_row_in_DataFrame.__name__,"timer =", end_timer-start_timer)
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
    #declare a variable
    dict_to_df = {}
    #we are looking for the item we need and adding it to the list of dictionaries 
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            #dict_to_df[len(dict_to_df)] = pd.Series(main_df.iloc[j]).T.to_dict()
            dict_to_df[len(dict_to_df)] = pd.Series(main_df.iloc[j]).T.to_dict()
        j = j+1
    #transforming list of dicts into dataframe
    df_to_return = pd.DataFrame.from_dict(dict_to_df, orient="index")
    #end_timer + return
    end_timer = time.perf_counter()
    print(find_many_rows_in_DataFrame.__name__, "timer =", end_timer-start_timer)
    return(df_to_return)

#get data from the different files and write into 1
def from_many_csv_to_one_df (
    files_to_read, #list of files to read from
    set_index_names, #names for columns/indexes for ur dataframe
    csv_separator=None, #separator for csv files (oprional)
):
    #startin timer
    start_timer = time.perf_counter()
    #dataframe to combine all of the file content in
    main_df = pd.DataFrame(columns=set_index_names)
    #transforming set_index_names for DataFrame.set_index
    set_index_names = [set_index_names]
    #cycle to get every csv-file into our main DataFrame
    for i in files_to_read: 
        #dataframe for each step of the cycle
        df_situational = pd.DataFrame()
        #reading next file our situational dataframe (df_situational)
        df_situational = pd.read_csv(i, engine= "python",sep=csv_separator, header=None )
        #giving names for columns in the created dataframe
        df_situational = df_situational.set_index(set_index_names)
        #transposing created dataframe
        df_situational = df_situational.transpose()
        #writing transposed situational dataframe (df_situational) into our main storage container
        main_df = pd.concat([main_df,df_situational], ignore_index=True)
    #ending timer
    end_timer = time.perf_counter()
    print(from_many_csv_to_one_df.__name__,"time =", end_timer-start_timer)
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

column = ["raid id"]
main_df = read_the_file_to_DF(
    file_to_read = dynamic_database["guilds_table"])
lable = find_1_row_in_DataFrame(
    main_df,
    object_to_search_for="GGuild",
    item_column =  "guild_name"
    )
main_df = read_the_file_to_DF(
    file_to_read = dynamic_database["characters_table"]
    )
item = find_many_rows_in_DataFrame(
    main_df, 
    object_to_search_for = lable.loc["guild_id"],
    item_column = "guild_id"
    )
print(item,"\n")


main_df = read_the_file_to_DF(file_to_look_into)
#item = find_item_in_DataFrame(main_df,"raid_1", "raid id")
print(main_df,"\n")

main_df = read_the_file_to_DF(file_to_look_into_csv)
item = find_item_in_DataFrame(main_df,"Heroic Key to the Focusing Iris", "item_name")
item1 = find_item_in_DataFrame1(main_df,"Heroic Key to the Focusing Iris", "item_name")
print(item,"\n", item1)


#bosses = 1
"""