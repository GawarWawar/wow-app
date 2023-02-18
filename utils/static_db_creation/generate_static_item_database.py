import numpy as np
import pandas as pd
import pyarrow as pa

import pyarrow.parquet as pq

import time

start_timer = time.perf_counter()


# Reading table w/ info about loot in Naxx
Naxx_df = pd.read_csv(
    "data/data_for_staic_db/manually_changed_static_db/Wow app - Items_from_Naxx_transfer.csv",
    usecols=[
        "boss_name",
        "item_id",
        "item_name"
    ],
    index_col=[0]
)

# Read names and ids of all bosses
bosses_list = pd.read_csv(
    "data/data_for_staic_db/manually_changed_static_db/Wow app - Bosses table.csv",
    usecols=[
        "boss_name",
        "boss_id",
    ]
)

# Dict for loot_table
loot_dict = {
    "boss_id" : [],
    "item_id" : []
}
# List of all items in the raids
all_items_ids = [] #theirs ids
all_items_names = [] #theirs names

wowhead_separator = ", "
for df_index in Naxx_df.index:
    # Getting items for the first boss
    item_ids = str(Naxx_df.loc[df_index]["item_id"]).split(wowhead_separator)
    
    boss_id = bosses_list.loc[bosses_list.loc[:,"boss_name"]==df_index]
    boss_id = boss_id.iloc[0].at["boss_id"]
    
    # Creat DataFrame w/ loot for certain boss
    df_add_loot = pd.DataFrame(
        {
            "item_id": item_ids,
            "boss_id": boss_id
        }
    )
    
    boss_dict = df_add_loot.to_dict(orient="list")
    
    # Add loot from boss to loot_dict
    loot_dict["boss_id"].extend(boss_dict["boss_id"])
    loot_dict["item_id"].extend(boss_dict["item_id"])
    
    all_items_ids.extend(
        item_ids
    )
    all_items_names.extend(
        str(Naxx_df.loc[df_index]["item_name"]).split(wowhead_separator)
    )

path_to_st_db="Data/Static_database"

# Writing prosses into loot_table
loot_df = pd.DataFrame.from_dict(loot_dict) 
loot_df = loot_df.sort_values(
    by=["boss_id","item_id"], 
    ignore_index=True
)

loot_df.to_parquet(
    path=path_to_st_db+"/"+"loot_of_bosses.parquet",
    engine="pyarrow",
)   

loot_df.to_csv(
        path_to_st_db+"/"+"loot_of_bosses.csv", 
        index_label=False, 
        index=False,
        header=True, 
    )

# Writing prosses into items_table
df_items = pd.DataFrame(
    {
        "item_id": all_items_ids,
        "item_name": all_items_names
    }
)

df_items = df_items.drop_duplicates()
df_items = df_items.sort_values(by="item_id", inplace=False, ignore_index=True)

df_items.to_parquet(
    path=path_to_st_db+"/"+"items.parquet",
    engine="pyarrow",
)   

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

df_bosses = pd.read_csv("Data/data_for_staic_db/manually_changed_static_db/Wow app - Bosses table.csv")

df_bosses.to_parquet(
    "Data/Static_database/bosses.parquet",
    engine="pyarrow"
)

df_raids = pd.read_csv("Data/data_for_staic_db/manually_changed_static_db/Wow app - Raid table.csv")

df_raids.to_parquet(
    "Data/Static_database/raids.parquet",
    engine="pyarrow"
)