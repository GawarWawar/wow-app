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

df = pd.read_csv(
    "data/data_for_staic_db/manually_changed_static_db/Wow app - Transfer sheet for Items.csv",
    usecols=[
        "boss_name",
        "item_id",
        "item_name"
    ],
    index_col=[0]
)

#building table for loot that drops from bosses
bosses_list = pd.read_csv(
    "data/data_for_staic_db/manually_changed_static_db/Wow app - Bosses table.csv",
    usecols=[
        "boss_name",
        "boss_id",
    ]
)

drop_dict = {
    "boss_id" : [],
    "item_id" : []
}
all_items_ids = []
all_items_names = []
for df_index in df.index:
    item_ids = str(df.loc[df_index]["item_id"]).split(", ")
    
    boss_id = bosses_list.loc[bosses_list.loc[:,"boss_name"]==df_index]
    boss_id = boss_id.iloc[0].at["boss_id"]
    
    #creat DataFrame w/ drop for certain boss
    df_add_drop = pd.DataFrame(
        {
            "item_id": item_ids,
            "boss_id": boss_id
        }
    )
    
    boss_dict = df_add_drop.to_dict(orient="list")
    #create dictiorary to transform into df
    drop_dict["boss_id"].extend(boss_dict["boss_id"])
    drop_dict["item_id"].extend(boss_dict["item_id"])

    all_items_ids.extend(
        item_ids
    )
    all_items_names.extend(
        str(df.loc[df_index]["item_name"]).split(", ")
    )

path_to_st_db="Data/Static_database"

drop_df = pd.DataFrame.from_dict(drop_dict) 
drop_df = drop_df.sort_values(
    by=["boss_id","item_id"], 
    ignore_index=True
)   

drop_df.to_csv(
        path_to_st_db+"/"+"loot_of_bosses.csv", 
        index_label=False, 
        index=False,
        header=True, 
    )

df_items = pd.DataFrame(
    {
        "item_id": all_items_ids,
        "item_name": all_items_names
    }
)

df_items = df_items.drop_duplicates()
df_items = df_items.sort_values(by="item_id", inplace=False, ignore_index=True)

df_items.to_csv(
        path_to_st_db+"/"+"items.csv", 
        index_label=False, 
        index=False,
        header=True, 
    )

end_timer = time.perf_counter()
print(
    "generate_static_item_database time =",
    end_timer-start_timer
)
