import numpy as np
import pandas as pd
import time


def read_the_file_to_DF (
    file_to_read, #file that we need to read
    file_type = "csv" #what type is our file, that we are reading
    ):
    """
        read file with the header and standart separator (,); 
        return DataFrame with conramination of the file
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
    print(end_timer-start_timer)
    return(df)


def find_item_in_DataFrame (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    object_position = 0, #column to look for item (should be integer, to use in iloc)
    ):
    """
        Finds entety that we are looking for in given DataFrame
    """
    #start timer
    start_timer = time.perf_counter()
    #looking for the item
    for i in main_df.iloc[:,object_position]:
        if i == object_to_search_for:
            #end_timer
            end_timer = time.perf_counter()
            print(end_timer-start_timer)
            return(i)

file_to_look_into_csv = "Data/Static_database/Items_from_Naxx.csv"
file_to_look_into = "Data/Static_database/Wow app - Raid table.csv"

main_df = read_the_file_to_DF(file_to_look_into)
item = find_item_in_DataFrame(main_df,"raid_1")
#bosses = 1