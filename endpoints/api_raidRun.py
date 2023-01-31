import numpy as np
import pandas as pd
import json
import datetime

from flask import request
from markupsafe import escape

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.tools as u_tools
import utils.add_row as add_row

def runs_of_the_guild_m(dynamic_database):
    #accept info about new run
    new_run_df = pd.DataFrame.from_dict(request.json, orient="index")
    
    #read table with info about runs
    df_for_runs = pd.read_csv(dynamic_database["runs_table"])
    
    #adding new run to the runs_table
    run_id = add_row.id_and_three_columns(
        df_for_runs,
        dict_w_info={
            #info about the run 
            0: new_run_df.loc["0","guild_id"],
            1: new_run_df.loc["0","raid_id"], 
            2: new_run_df.loc["0","date_of_raid"]
        }
    )

    #writing runs back to the file
    df_for_runs.to_csv(
        dynamic_database["runs_table"],
        index=False,
        index_label=False
    )
    df_for_runs = None
    
    #reading table w/ all existing characters
    df_for_characters = pd.read_csv(
        dynamic_database["characters_table"] 
    )
    df_for_run_members = pd.read_csv(
        dynamic_database["run_members"] #members of all runs
    )
    
    #adding run members
    for member_counter in range(len(new_run_df.loc[:,"character_id"])):
        #check if character
        if new_run_df.loc[str(member_counter),"character_id"] == "new_char":
            
            #adding new character to the character_table
            character_id = add_row.id_and_three_columns(
                df_for_characters,
                dict_w_info={
                    #info about that character we need to write
                    0: new_run_df.loc[str(member_counter),"character_name"],
                    1: new_run_df.loc[str(member_counter),"guild_id"], 
                    2: new_run_df.loc[str(member_counter),"class"]
                }
            )
        else:
    #using the same variable to store character id
            character_id = new_run_df.loc[str(member_counter),"character_id"]
        
        #getting system time for the run_members_table
        exact_time = datetime.datetime.now()
        
        #adding run member to the table  
        add_row.three_columns(
            df_for_run_members,
            dict_w_info={
                    #info about that character we need to write
                    0: run_id,
                    1: character_id,
                    2: exact_time
                }
        )
    
    df_for_characters.to_csv(
        dynamic_database["characters_table"],
        index=False,
        index_label=False
    )
    df_for_run_members.to_csv(
        dynamic_database["run_members"],
        index=False,
        index_label=False
    )
     
    #returning run_id as the respons
    dict_to_return = '''{"run_id" : %s}''' %run_id
    result = json.loads(dict_to_return)
    return json.dumps(result)