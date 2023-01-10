import numpy as np
import pandas as pd
import time


def read_the_file_to_DF (
    file_to_read, #file that we need to read
    file_type = "csv" #what type is our file, that we are reading
    ):
    """
        read file with the header and standart separator (,); \n
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
    print("read_the_file_to_DF timer =",end_timer-start_timer)
    return(df)


def find_item_in_DataFrame (
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
    for i in main_df.loc[:,column_name]:
        if i == object_to_search_for:
            #end_timer
            end_timer = time.perf_counter()
            print("find_item_in_DataFrame timer =", end_timer-start_timer)
            return(i)

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

"""
file_to_look_into_csv = "Data/Static_database/Items_from_Naxx.csv"
file_to_look_into = "Data/Static_database/Wow app - Raid table.csv"

main_df = read_the_file_to_DF(file_to_look_into)
item = find_item_in_DataFrame(main_df,"raid_1", "raid id")
item1 = find_item_in_DataFrame1(main_df,"raid_1", "raid id")
print(item,"\n", item1)

main_df = read_the_file_to_DF(file_to_look_into_csv)
item = find_item_in_DataFrame(main_df,"Heroic Key to the Focusing Iris", "item_name")
item1 = find_item_in_DataFrame1(main_df,"Heroic Key to the Focusing Iris", "item_name")
print(item,"\n", item1)


#bosses = 1
"""