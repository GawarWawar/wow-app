import numpy as np
import pandas as pd
import json
import datetime

import time

from flask import request, jsonify
from markupsafe import escape

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.simple_utils.simple_tools as su_tools
import utils.simple_utils.add_row as add_row
import utils.tools as u_tools

def add_loots_m (
    run_id,
    #dynamic database
    dn_db_events_table,
):
    run_id = int(escape(run_id))
    
    #forming df for new events  
    new_loot = request.json
    new_loot = pd.DataFrame.from_records(new_loot)
    
    #reading table w/ info about all events
    df_events = pd.read_csv(dn_db_events_table)
    
    events_added = []
    events_changed = []
    for loot in range(len(new_loot.index)):
        #cheking if this event exist by combination of 1+2
            #1: "boss_id"
        event_boss_x_item = su_tools.\
            find_item_in_DataFrame_without_for(
                df_events,
                new_loot.iloc[loot].at["boss_dropped_from_id"],
                "boss_id"
            )
            #2: "item_id"
        event_boss_x_item = su_tools.\
            find_item_in_DataFrame_without_for(
                event_boss_x_item,
                new_loot.iloc[loot].at["item_id"],
                "item_id"
            )
        
        #if it doesnt exist ->
            #create new event
        if event_boss_x_item.empty:
            event_id = add_row.id_four_columns_and_exact_time(
                df_events,
                dict_w_info={
                    0: int(run_id),
                    1: int(
                        new_loot.iloc[loot].\
                            at["boss_dropped_from_id"]
                    ),
                    2: int(
                        new_loot.iloc[loot].\
                            at["item_id"]
                    ),
                    3: float(
                        new_loot.iloc[loot].\
                            at["character_assigned_to_id"]
                    ),
                }
            )
            events_added.append(int(event_id))
        #if it does exist ->
            #change old event
        else:
            df_events.loc[
                event_boss_x_item.index[0],
                "character_id"
            ] = float(new_loot.iloc[loot].\
                    at["character_assigned_to_id"])
            events_changed.append(
                int(df_events.loc[
                    event_boss_x_item.index[0],
                    "event_id"
                ])
            )
            
    #write info back to table
    df_events.to_csv(
        dn_db_events_table,
        index=False,
        index_label=False
    )

    #response is this message
    message = {
            "result" : True,
            "events_added": events_added,
            "events_changed": events_changed
        }
    return(message)


def delete_loot(
    run_id,
    #dynamic database
    dn_db_events_table,
):
    run_id = int(escape(run_id))

    loot_to_delete = request.json
    
    df_events = pd.read_csv(dn_db_events_table)
    
    they_werent_in_the_loot = []
    for loot in loot_to_delete:
        loot_to_look = su_tools.find_item_in_DataFrame_without_for(
            df_events,
            int(loot),
            "event_id"
        )
        
        if loot_to_look.empty:
            they_werent_in_the_loot.append(loot)
        else:
            df_events = df_events.drop(loot_to_look.index[0])
    
    df_events.to_csv(
        dn_db_events_table,
        index=False,
        index_label=False
    )
    
    if len(they_werent_in_the_loot) == 0:
        #massage if we didnt find anyone, who wasnt in the run
        message={
            "result" : True,
            "were_not_in_the_loot" : None
        }
    else: 
        #massage if we did find someone, who wasnt in the run
        message = {
            "result" : True,
            "were_not_in_the_loot": they_werent_in_the_loot
        }
    return(message)           
        