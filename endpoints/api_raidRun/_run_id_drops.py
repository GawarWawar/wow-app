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

def add_drops_m (
    run_id,
    #dynamic database
    dn_db_runs_table,
    dn_db_events_table,
    dn_db_run_members,
    dn_db_characters_table,
    #static database
    st_db_raid_table
):
    run_id = int(escape(run_id))
    
    new_drop = request.json
    new_drop = pd.DataFrame.from_records(new_drop)
    
    df_events = pd.read_csv(dn_db_events_table)
    
    print(new_drop.index)
    
    events_added = []
    events_changed = []
    for drop in range(len(new_drop.index)):
        event_boss_x_item = su_tools.find_item_in_DataFrame_without_for(
            df_events,
            new_drop.iloc[drop].at["boss_dropped_from_id"],
            "boss_id"
        )
        event_boss_x_item = su_tools.find_item_in_DataFrame_without_for(
            event_boss_x_item,
            new_drop.iloc[drop].at["item_id"],
            "item_id"
        )
        if event_boss_x_item.empty:
            event_id = add_row.id_four_columns_and_exact_time(
                df_events,
                dict_w_info={
                    0: int(run_id),
                    1: int(new_drop.iloc[drop].at["boss_dropped_from_id"]),
                    2: int(new_drop.iloc[drop].at["item_id"]),
                    3: float(new_drop.iloc[drop].at["character_assigned_to_id"]),
                }
            )
            events_added.append(int(event_id))
        else:
            df_events.loc[
                event_boss_x_item.index[0],
                "character_id"
            ] = float(new_drop.iloc[drop].at["character_assigned_to_id"])
            events_changed.append(
                int(df_events.loc[
                    event_boss_x_item.index[0],
                    "event_id"
                ])
            )
            
    df_events.to_csv(
        dn_db_events_table,
        index=False,
        index_label=False
    )

    message = {
            "result" : True,
            "events_added": events_added,
            "events_changed": events_changed
        }
    return(message)
    
    
    