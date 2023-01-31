import numpy as np
import pandas as pd
import json
import datetime

from flask import request, jsonify
from markupsafe import escape

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.tools as u_tools
import utils.add_row as add_row


def edit_raid_run_m(
    id,
    dynamic_database,
    static_database
):
    raid_run_id = int(escape(id))
    
    #reading tables w/ info
    df_for_runs = pd.read_csv(dynamic_database["runs_table"]) #runs
    df_for_events = pd.read_csv(dynamic_database["events_table"]) #events
    
    if request.method == "PUT":
        #info that comes w/ the request
        run_update = pd.DataFrame.from_dict(request.json, orient="index")
        
        #check is there such run
        run_existence = u_tools.find_one_row_in_DataFrame(
            df_for_runs,
            raid_run_id,
            "run_id"
        )
        run_existence_type = run_existence.__class__.__name__
        if run_existence_type == "NoneType" :
            return jsonify("There is no such run")
        
        #get indexes of old events
        to_drop = pd.DataFrame(df_for_events.loc[:,"run_id"]==raid_run_id)
        to_drop = to_drop[to_drop["run_id"]==True].index.to_list()
        
        
        #delete old events
        df_for_events = df_for_events.drop(
            to_drop
        )
        
        new_event_ids = []
        
        #create new events from response info
        for event in range(len(run_update)):
            exact_time = datetime.datetime.now() #system time
            #create new event
            new_event_ids.append(
                add_row.id_and_five_columns(
                    df_for_events,
                    dict_w_info={
                        0: run_update.iloc[event].at["run_id"],
                        1: run_update.iloc[event].at["boss_id"],
                        2: run_update.iloc[event].at["item_id"],
                        3: run_update.iloc[event].at["character_id"],
                        4: exact_time,
                    }
                )
            )
            
        #write info w/ new events into the table 
        df_for_events.to_csv(
            dynamic_database["events_table"],
            index=False,
            index_label=False
        )

        #returning list of new event_id -s as the respons
        dict_to_return = '''{"event_id" : %s}''' %new_event_ids
        result = json.loads(dict_to_return)
        return json.dumps(result)             
    
    #GET
    else:
        #find run by its id in runs table
        df_to_return = u_tools.find_item_in_DataFrame_without_for(
            df_for_runs,
            raid_run_id,
            "run_id"
        )

        #find all events in events table by the run id
        df_to_return = pd.DataFrame.merge(
            df_to_return,
            df_for_events,
            on="run_id"
        )
        
        #get info about characters
        df_for_characters = pd.read_csv(dynamic_database["characters_table"])
        
        #find all characters, that were involved in run
        df_to_return = pd.DataFrame.merge(
            df_to_return,
            df_for_characters,
            on="character_id",
            #there is guild in run table and characters table ->
            suffixes=["_run","_character"] 
        #we are giving them different names
        )
        
        #read info about items
        df_for_items = pd.read_csv(static_database["item_table"])
        
        #find all items, that has been dropped 
        df_to_return = pd.DataFrame.merge(
            df_to_return,
            df_for_items,
            on="item_id"
        )
        
        #return json w/ full info
        result = json.loads(df_to_return.to_json(orient="index"))
        return json.dumps(result, indent=2)