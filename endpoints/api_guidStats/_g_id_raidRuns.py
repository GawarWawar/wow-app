import numpy as np
import pandas as pd
import json
#import datetime

#from flask import request, jsonify
from markupsafe import escape

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.tools as u_tools
#import utils.add_row as add_row

def get_all_guilds_runs_m(
    g_id,
    #dynamic_database
    dn_db_guilds_table,
    dn_db_runs_table,
    #static_database
    st_db_raid_table
):
    needed_guild_id = int(escape(g_id))
    
    #read table w/ info about guilds
    df_for_guild = pd.read_csv(dn_db_guilds_table)
    #finding all info about needed_guild 
    guild_info = u_tools.find_one_row_in_DataFrame(
        df_for_guild,
        needed_guild_id,
        "guild_id"
    )
    df_for_guild = None #no need df_for_guild anymore
    
    #writing getted info into dict_to_send
    dict_to_send = {
        "guild_name": guild_info.loc["guild_name"],
        #structuring list to write guild_runs into
        "guild_runs": []
    }
    guild_info = None #no need guild_info anymore
    
    #reading table w/ info about all runs
    df_for_runs = pd.read_csv(dn_db_runs_table)

    #find all runs of given guild
    main_df = u_tools.find_item_in_DataFrame_without_for(
        df_for_runs,
        needed_guild_id,
        "guild_id"
    )
    df_for_runs = None #no need df_for_runs anymore
    
    #delitting info that we wont write into response
    main_df.pop("guild_id")
    
    #read table w/ info about raids
    df_for_raids = pd.read_csv(st_db_raid_table)
    
    #writing info about raids into runs
    main_df = pd.DataFrame.merge(
        main_df,
        df_for_raids,
        on="raid_id"
    )

    #adding our info about runs into dict_to_send
    u_tools.extend_list_by_dict_from_df(
        main_df,
        dict_to_send["guild_runs"]
    )
    
    #return json w/ full info
    return json.dumps(dict_to_send, indent=2)