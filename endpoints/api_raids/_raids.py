import numpy as np
import pandas as pd
import json
#import datetime

#import time

#from flask import request, jsonify
#from markupsafe import escape

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.simple_utils.simple_tools as su_tools
#import utils.add_row as add_row

def give_info_about_all_raids (
    st_db_raid_table,
):
    #read the table w/ info about raids
    df_for_raids = pd.read_parquet(st_db_raid_table)
    
    df_for_raids.rename(
        {
            "raid_id": "id",
            "raid_name": "name"
        },
        axis="columns",
        inplace=True
    )
    
    dict_to_send ={
        "data": []
    }
    
    su_tools.extend_list_by_dict_from_df(
        df_for_raids,
        dict_to_send["data"]
    )
    
    #orient="records" gives us -> 
        #info about every raid in form of the list
            #each elem of list have:
            #   "id"
            #   "name"
            #   "raid_capacity"
    
    return json.dumps(dict_to_send, indent=2)