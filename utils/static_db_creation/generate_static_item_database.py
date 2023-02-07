import numpy as np
import pandas as pd
import time

from os import listdir
from os.path import isfile, join, dirname, abspath
#
#import sys
#
#SCRIPT_DIR = dirname(abspath(__file__))
#sys.path.append(dirname(SCRIPT_DIR))

import db_creation_utils.db_creation_tools as db_tools

start_timer = time.perf_counter()

#giving basic info about our futer database
file_path_to_read = "data/data_for_staic_db/items_from_naxx"
indexes_that_we_want_to_set_up = [
        "item_id", 
        "item_name"
]

files_for_items_list = [f for f in listdir(file_path_to_read) 
                    if isfile(join(file_path_to_read, f))]

db_tools.from_many_csv_to_one_csv(
    files_to_read=files_for_items_list,
    path_to_fstr=file_path_to_read,
    file_to_write="items.csv",
    path_to_ftw="Data/Static_database",
    set_index_names=indexes_that_we_want_to_set_up,
    transpose_grouped_file=False,
    options_for_tocsv={
        "index_label":False,
        "header" : True,
        "index":False
    }
)

# Building table for loot that drops from bosses
bosses_list = pd.read_csv(
    "Data/Static_database/Wow app - Bosses table.csv"
)
bosses_list = bosses_list.sort_values("boss_name")
#temporary droping lists, that doesnt have files
#bosses_list = bosses_list.drop([16])

#creating table for items, that can drop from certain bosses
file_for_drops_from_bosses = files_for_items_list
file_for_drops_from_bosses.sort()
drop_dict = {
    "boss_id" : [],
    "item_id" : []
}

j = 0
for file in file_for_drops_from_bosses:
    boss_df = pd.DataFrame()
    boss_dict = {}
    
    boss_df = db_tools.vertical_csv_to_df(
        file_to_read = file,
        path_to_ftr = file_path_to_read,
        dataframe = boss_df,
        set_indexes_names = indexes_that_we_want_to_set_up
    )

    boss_id = bosses_list.iat[j,0]
    
    #creat DataFrame w/ drop for certain boss
    boss_df["boss_id"] = boss_id
    boss_df.pop("item_name")
    
    boss_dict = boss_df.to_dict(orient="list")
    #create dictiorary to transform into df
    drop_dict["boss_id"].extend(boss_dict["boss_id"])
    drop_dict["item_id"].extend(boss_dict["item_id"])
    
    j += 1

drop_df = pd.DataFrame.from_dict(drop_dict) 
drop_df = drop_df.sort_values(by=["boss_id","item_id"])   
drop_df.to_csv(
    "Data/Static_database/loot_of_bosses.csv",
    index=False,
    index_label=False
)

end_timer = time.perf_counter()
print(
    "generate_static_item_database time =",
    end_timer-start_timer
)
