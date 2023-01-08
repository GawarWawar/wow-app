import numpy as np
import pandas as pd
import time

def find_item_in_DataFrame (
    df_file, #file what contain DataFrame
    item_to_search_for, #what we need to find
    df_file_type = "csv" #file type of df_file (csv as a default)
):
    #writing our file contamination into DataFrame
    if df_file_type == "csv":
        main_df = pd.read_csv(df_file)
    for i in main_df.iloc[:,0]:
        if i == item_to_search_for:
            return(i)

file_to_look_into = "Data/Static_database/Wow app - Raid table.csv"
print (find_item_in_DataFrame(file_to_look_into,"raid_1"))
