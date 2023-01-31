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
    dynamic_database
):
    needed_guild_id = int(escape(g_id))
    
    #reading table w/ info about all runs
    df_for_runs = pd.read_csv(dynamic_database["runs_table"])

    #find all runs of given guild
    df_to_return = u_tools.find_rows_in_DataFrame(
        df_for_runs,
        needed_guild_id,
        "guild_id"
    )

    #return json w/ full info
    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)