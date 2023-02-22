import numpy as np
import pandas as pd
import json
#import datetime

from flask import request, jsonify
from markupsafe import escape

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.simple_utils.simple_tools as su_tools
import utils.tools as u_tools

#import utils.add_row as add_row

def give_all_aviable_guild_stats_m(
    g_id,
    #dynamic database
    dn_db_guilds_table,
    dn_db_characters_table,
    dn_db_runs_table,
    #static database
    st_db_raid_table
):
    guild_id = int(escape(g_id)) 
    
    #read table w/ guilds info
    df_for_guild = pd.read_parquet(
        dn_db_guilds_table
    )

    #get all guild's info
    guild_info = su_tools.find_item_in_DataFrame_without_for(
        df_for_guild,
        guild_id,
        "guild_id"
        )
    
    #check is there such guild
    if guild_info.empty:
        response = {
            "data" : {
                "error" : True,
                "message": "There is no such guild"
            }
        }
        return jsonify(response) 
    
    #forming the structure for the response
    dict_to_return = {
        "data":{
            "id": guild_id,
            "name": guild_info.iloc[0].at["guild_name"], 
            "characters":[],
            "guildRuns": []
        }
    }
    
    #read table w/ characters info
    df_characters = pd.read_parquet(
        dn_db_characters_table
    )
    
    #find all members of the given guild
    df_characters = su_tools.find_item_in_DataFrame_without_for(
        df_characters,
        guild_id,
        "guild_id"
    )
    
    #forming info to give into the response
    df_characters.pop("guild_id")
    
    #changing names from db form to the response form
    df_characters = df_characters.rename(
        {
            "character_id": "id",
            "character_name": "name",
            "character_class": "class"
        },
        axis="columns"
    )
    
    #adding our info to the response
    dict_to_return["data"]["characters"] = \
        df_characters.to_dict(orient="records")
    df_characters= None
    
    #reading table about
    df_runs = pd.read_parquet(dn_db_runs_table)#runs 
    df_raids = pd.read_parquet(st_db_raid_table)#raids
    
    #changing names from db form to the response form
    df_raids = df_raids.rename(
        {
            "raid_id" : "id",
            "raid_name" : "name"
        },
        axis="columns"
    )
    
    #finding all runs of the guild
    df_runs = su_tools.find_item_in_DataFrame_without_for(
        df_runs,
        guild_id,
        "guild_id"
    )
    #forming info to give into the response
    df_runs.pop("guild_id")
    
    #changing names from db form to the response form
    df_runs = df_runs.rename(
        {
            "raid_id" : "id"
        },
        axis="columns"
    )
    
    #adding the new column to store info about raid for each run
    df_runs["raid"]="place_holder"
    
    #proseed in if guild has at least 1 run
    if not df_runs.empty:
        #forming list of unique raids guild was in
        raids_unique_ids = df_runs["id"].copy()
        raids_unique_ids = raids_unique_ids.to_frame()
        raids_unique_ids = raids_unique_ids.\
            drop_duplicates(ignore_index=True)
        
        #for every run -> add add info about it's raid
        for raid_id in range(len(raids_unique_ids.loc[:,"id"])):
            #getting info about raid in raid table
            raid_info = su_tools.find_item_in_DataFrame_without_for(
                df_raids,
                raids_unique_ids.loc[raid_id,"id"],
                "id"
            )
            #transforming info into writing form
            raid_info = [json.loads(
                raid_info.to_json(orient="records")
                )
            ]
            #looking for every run w/ this raid ->
                #add info about that raid to the run
            df_runs.loc[
                df_runs.loc[:,"id"]==\
                    raids_unique_ids.loc[raid_id,"id"],
                "raid"
            ]=raid_info
        
        #forming info to give into the response
        df_runs.pop("id")
        
        #changing names from db form to the response form
        df_runs = df_runs.rename(
            {
                "run_id": "id"
            },
            axis="columns"
        )
        
        #adding our info to the response
        dict_to_return["data"]["guildRuns"].extend(
            json.loads(
                df_runs.to_json(
                    orient="records",
                    indent=2
                )
            )
        )
    else:
        pass
    
    #returning all info we found
    return json.dumps(dict_to_return, indent=2)