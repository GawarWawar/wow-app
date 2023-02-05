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

def runs_of_the_guild_m(
    dn_db_runs_table,
    dn_db_characters_table,
    dn_db_run_members
):
    #accept info about new run
    new_run = request.json
    
    #read table with info about runs
    df_for_runs = pd.read_csv(dn_db_runs_table)
    
    #adding new run to the runs_table
    run_id = add_row.id_and_two_columns(
        df_for_runs,
        dict_w_info={
            #info about the run 
            1: new_run["guild_id"],
            0: new_run["raid_id"],
        }
    )

    #writing runs back to the file
    df_for_runs.to_csv(
        dn_db_runs_table,
        index=False,
        index_label=False
    )
    df_for_runs = None
    
    #reading table w/ 
    df_for_characters = pd.read_csv(
        dn_db_characters_table #all existing characters 
    )
    df_all_runs_members = pd.read_csv(
        dn_db_run_members #members of all runs
    )
    
    df_this_run_members = pd.DataFrame.from_records(
        new_run["participants"]
    )
    print(df_this_run_members)
    

    for run_member_counter in range(
        len(df_this_run_members.loc[:,"name"])
    ):
        #find character in the character table
        member_existence = \
            u_tools.find_item_in_DataFrame_without_for(
                df_for_characters,
                df_this_run_members.loc[run_member_counter,"name"],
                "character_name"
            )
            
        #check if this character already exist 
        if member_existence.empty:
            #adding new character to the character_table
            character_id = add_row.id_and_three_columns(
                df_for_characters,
                dict_w_info={
                    #info about that character we need to write
                    0:df_this_run_members.loc[run_member_counter,"name"],
                    1:new_run["guild_id"],
                    2:df_this_run_members.loc[run_member_counter,"class"],
                }
            )
        else:
            #if exist -> getting its id
            character_id = member_existence.iloc[0].at["character_id"]
        
        #getting system time for the run_members_table
        exact_time = datetime.datetime.now()
        
        #adding run member to the table  
        add_row.three_columns(
            df_all_runs_members,
            dict_w_info={
                    #info about that character we need to write
                    0: run_id,
                    1: character_id,
                    2: exact_time
                }
        )
    
    #writing info back into talbes 
    df_for_characters.to_csv(
        dn_db_characters_table,
        index=False,
        index_label=False
    )
    df_all_runs_members.to_csv(
        dn_db_run_members,
        index=False,
        index_label=False
    )
     
    #returning run_id as the respons
    return run_id