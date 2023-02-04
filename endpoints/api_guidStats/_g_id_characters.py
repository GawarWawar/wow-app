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

def characters_of_the_guild_m (g_id, dynamic_database):
    guild_id = int(escape(g_id)) 

    #read table w/ guilds info
    df_for_guild = pd.read_csv(
        dynamic_database["guilds_table"]
    )
    
    #get all guild's info
    guild_info = u_tools.find_one_row_in_DataFrame(
        df_for_guild,
        object_to_search_for = guild_id,
        item_column = "guild_id"
    )
    
    #check is there such guild
    guild_info_type = guild_info.__class__.__name__
    if guild_info_type == "NoneType" :
        return jsonify("There is no such guild")   
        
    #read table w/ characters info
    df_for_characters = pd.read_csv(dynamic_database["characters_table"])
    
    
    #find all members of the given guild
    df_to_return = pd.DataFrame.merge(
        guild_info.to_frame().T,
        df_for_characters,
        on="guild_id"
    )
    
    #transform guild_id and guild_name columns into index 
    #   to create list of characters
    df_to_return = df_to_return.set_index(["guild_id", "guild_name"])
    
    #forming propper respons for the FE
    dict_to_return ={
        "guild_name": guild_info["guild_name"],
        "characters": df_to_return.to_dict(orient="records")
    } 
    
    return json.dumps(dict_to_return, indent=2)