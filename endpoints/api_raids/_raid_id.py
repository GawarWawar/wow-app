import numpy as np
import pandas as pd
import json

import time

from flask import jsonify
from markupsafe import escape

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.simple_utils.simple_tools as su_tools

#getting raid id to look for
def info_about_raid_id_m(
        id, 
        st_db_raid_table,
        st_db_boss_table,
        st_db_loot_table,
        st_db_item_table
):
    #start timer
    s_t = time.perf_counter()
    
    raid_id = int(escape(id))
    
    #read table w/ raid info
    main_df = pd.read_parquet(
        st_db_raid_table
    )

    #looking for the specific raid id
    main_df = su_tools.find_one_row_in_DataFrame(
        main_df,
        object_to_search_for = raid_id,
        item_column = "raid_id"
    )
    
    #check is there such raid
    main_df_type = main_df.__class__.__name__
    if main_df_type == "NoneType" :
        return jsonify("There is no such raid")
    
    dict_to_send = {
        "data" :{
            "id" : int(main_df["raid_id"]),
            "name" : main_df["raid_name"],
            "raid_capacity" : int(main_df["raid_capacity"]),
            "bosses" : []
        }
    }
    
    #delete columns that wont use in main_df
    main_df.pop("raid_name")
    main_df.pop("raid_capacity")
    
    #reading table w/ bosses info
    df_for_bosses = pd.read_parquet(
        st_db_boss_table,
        columns=[
            "boss_id",
            "raid_id",
            "boss_name",
            #"npc_wowhead_id"
        ]
    )
    
    #add bosses of our raid
    main_df = pd.DataFrame.merge(
        main_df.to_frame().T,
        df_for_bosses,
        on="raid_id")
    
    main_df.pop("raid_id")
    
    #reading table w/ dropp info
    df_for_drop = pd.read_parquet(
        st_db_loot_table
    )
    #read items info
    df_items = pd.read_parquet(
        st_db_item_table
    )
    
    #for every boss get its loot
    for row in main_df["boss_id"]:
        series_row = main_df[main_df.loc[:, "boss_id"] == row] 
        
        #writing info about boss and its loot into the dict
        add_part = {
            "id" : int(series_row.iloc[0].at["boss_id"]),
            "name" : series_row.iloc[0].at["boss_name"],
            #"npc_wowhead_id" : series_row.iloc[0].at["npc_wowhead_id"],
            "loot": []
        }
        
        #delete columns that wont use in df_for_cycle
        series_row.pop("boss_name")
        #series_row.pop("npc_wowhead_id")
        
        #getting loot_drop of sertain boss
        df_for_cycle = pd.merge(
            series_row,
            df_for_drop,
            on="boss_id"
        )
        
        #delete column that we dont need in df_for_cycle anymore
        df_for_cycle.pop("boss_id")
        
        #getting info about items for loot
        df_for_cycle = pd.merge(
            df_for_cycle,
            df_items,
            on="item_id"
        )

        df_for_cycle.rename(
            {
                "item_id": "id",
                "item_name": "name"
            },
            axis="columns",
            inplace=True
        )
        
        #renaming elements according to docs
        su_tools.extend_list_by_dict_from_df(
            df_for_cycle,
            add_part["loot"]
        )

        #writing boss's data into the main dict
        dict_to_send["data"]["bosses"].append(add_part)
    
    #end timer
    e_t = time.perf_counter()
    print(f"Time of {info_about_raid_id_m.__name__}={e_t-s_t}")
    
    return json.dumps(dict_to_send, indent=2)
