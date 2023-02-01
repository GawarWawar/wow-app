import numpy as np
import pandas as pd
import json


from flask import jsonify
from markupsafe import escape

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.tools as u_tools

#getting raid id to look for
def info_about_raid_id_m(
        id, 
        static_database
):
    raid_id = int(escape(id))
    
    
    #read table w/ raid info
    main_df = pd.read_csv(
        static_database["raid_table"]
        )

    #looking for the specific raid id
    main_df = u_tools.find_one_row_in_DataFrame(
        main_df,
        object_to_search_for = raid_id,
        item_column = "raid_id"
    )
    
    #check is there such raid
    main_df_type = main_df.__class__.__name__
    if main_df_type == "NoneType" :
        return jsonify("There is no such raid")
    
    dict_to_send = {
        "raid_name" : main_df["raid_name"],
        "raid_type" : int(main_df["raid_type"]),
        "bosses" : []
    }
    
    #reading table w/ bosses info
    df_for_bosses = pd.read_csv(
        static_database["boss_table"]
        )
    #add bosses of our raid
    main_df = pd.DataFrame.merge(
        main_df.to_frame().T,
        df_for_bosses,
        on="raid_id")

    main_df = main_df.set_index(
        ["raid_id","raid_name","raid_type"]
    )
    
    #reading table w/ dropp info
    df_for_drop = pd.read_csv(
        static_database["loot_table"]
    )
    #read items info
    df_items = pd.read_csv(
        static_database["item_table"]
    )
    
    #for every boss get its loot
    for row in range(len(main_df["boss_id"])):
        series_row = main_df[main_df.loc[:, "boss_id"] == row] 
        
        #getting loot_drop of sertain boss
        df_for_work = pd.merge(
            series_row,
            df_for_drop,
            on="boss_id"
        )
        
        #getting info about items from boss's loot
        df_for_work = df_for_work.set_index(["boss_id","boss_name","npc_wowhead_id"])
        df_for_work = pd.merge(
            df_for_work,
            df_items,
            on="item_id"
        )
        
        #writing info about boss and its loot into the dict
        add_part = {
            "boss_id" : int(series_row.iloc[0].at["boss_id"]),
            "boss_name" : series_row.iloc[0].at["boss_name"],
            "npc_wowhead_id" : series_row.iloc[0].at["npc_wowhead_id"],
            "loot": json.loads(df_for_work.to_json(orient="records"))
        }

        #writing boss's data into the main dict
        dict_to_send["bosses"].append(add_part)
    
    return json.dumps(dict_to_send, indent=2)