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

import utils.tools as u_tools
#import utils.add_row as add_row

def give_all_aviable_guild_stats_m(
    g_name,
    dynamic_database
):
    guild_name = escape(g_name) 
    guild_info = pd.Series()
    
    #read table w/ guilds info
    df_for_guild = pd.read_csv(
        dynamic_database["guilds_table"]
    )

    #get all guild's info
    guild_info = u_tools.find_one_row_in_DataFrame(
        df_for_guild,
        object_to_search_for = guild_name,
        item_column = "guild_name"
        )
    
    #check is there such guild
    guild_info_type = guild_info.__class__.__name__
    if guild_info_type == "NoneType" :
        return jsonify("There is no such guild")   
    
    #read table w/ characters info
    df_for_characters = pd.read_csv(
        dynamic_database["characters_table"]
        )
    
    #find all members of the given guild
    df_to_return = u_tools.find_rows_in_DataFrame(
        df_for_characters,
        object_to_search_for = guild_info.loc["guild_id"],
        item_column = "guild_id"
        )
    
    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)