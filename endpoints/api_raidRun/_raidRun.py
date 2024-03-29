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

import utils.simple_utils.simple_tools as su_tools
import utils.tools as u_tools
from utils.simple_utils import add_row

def create_new_run_m(
    dn_db_runs_table,
    dn_db_characters_table,
    dn_db_run_members
):
    #accept info about new run
    new_run = request.json
    
    #read table with info about runs
    df_for_runs = pd.read_parquet(
        dn_db_runs_table,
        engine="pyarrow"
    )
    
    #adding new run to the runs_table
    
    run_id = add_row.add_a_row_with_id_and_exact_time(
        df_for_runs,
        # Info about the run 
        list_with_info=[ 
            new_run["guild_id"],
            new_run["raid_id"],
        ]
    )

    #writing runs back to the file
    df_for_runs.to_parquet(
        dn_db_runs_table,
        engine="pyarrow"
    )
    df_for_runs = None
    
    #reading table w/ 
    df_for_characters = pd.read_parquet(
        dn_db_characters_table #all existing characters 
    )
    df_all_runs_members = pd.read_parquet(
        dn_db_run_members #members of all runs
    )
    
    #reading who will be in the raid
    df_this_run_members = pd.DataFrame.from_records(
        new_run["participants"]
    )
    
    df_this_run_members = df_this_run_members.rename(
        {
            "class" : "character_class"
        },
        axis="columns"
    )

    for run_member_counter in range(
        len(df_this_run_members.loc[:,"name"])
    ):
        character_id = u_tools.check_character_existence_add_if_not(
            df_for_characters,
            df_this_run_members,
            run_member_counter,
            new_run["guild_id"]
        )
        
        add_row.add_a_row_with_exact_time(
            #adding run member to the table
            df_all_runs_members,
            list_with_info=[
                #info about that character we need to write
                run_id,
                character_id
            ]
        )
    
    #writing info back into talbes 
    df_for_characters.to_parquet(
        dn_db_characters_table,
        engine="pyarrow"
    )
    
    df_all_runs_members.to_parquet(
        dn_db_run_members,
        engine="pyarrow"
    )
     
    #returning run_id as the respons
    return run_id