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
from utils.simple_utils import add_row


def raid_run_info_m(
    run_id,
    #dynamic database
    dn_db_runs_table,
    dn_db_events_table,
    dn_db_run_members,
    dn_db_characters_table,
    #static database
    st_db_raid_table,
    #message
    message= {"result" : True}
):
    #start timer
    s_t = time.perf_counter()
    
    raid_run_id = int(escape(run_id))

    #reading table w/ info about runs
    df_runs = pd.read_parquet( 
            dn_db_runs_table,
            columns=[
              "run_id",
              "guild_id",
              "raid_id",
              "date_finished"  
            ]
        )
    
    #find run by its id in runs table
    run_info = su_tools.find_item_in_DataFrame_without_for(
        df_runs,
        raid_run_id,
        "run_id"
    )
    run_index = run_info.index[0]
    
    
    #creating dictionary that we will send
    dict_to_send = {
        "data":{
            #adding already known info from run_info
            "id": raid_run_id,
            "date_finished": run_info.iloc[0].at["date_finished"],
            #creating structure
            "raid": {},
            "participants":[],
            "loot_distributed":[]
        },
        "message": message
    }
    
    #we dont need that info about run anymore 
    run_info.pop("guild_id")
    run_info.pop("date_finished")
    
    
    #read the table w/ info about raids
    df_run_raid = pd.read_parquet(
        st_db_raid_table
    )
    
    #getting info about our run
    df_run_raid = pd.DataFrame.merge(
        df_run_raid,
        run_info,
        on="raid_id"
    )
    
    #we dont need that info about run in df_run_raid
    df_run_raid.pop("run_id")
    #naming items according to doc
    df_run_raid = df_run_raid.rename(
        mapper={
            "raid_id": "id",
            "raid_name": "name"
        },
        axis="columns"
    )
    
    #adding our info to dict_to_send
    raid_to_add = json.loads(
        df_run_raid.to_json(orient="records")
    )
    dict_to_send["data"]["raid"] = raid_to_add[0]
    
    print(dict_to_send["data"]["raid"])
    
    #we dont need that info about run anymore 
    run_info.pop("raid_id")
    
    #reading table w/ info about run members
        # we are not readint colums w/ # in the DataFrame
    df_run_members = pd.read_parquet(
        dn_db_run_members,
        columns=[
            "run_id",
            "character_id",
            "system_time"
        ]
    )
    
    #getting info about only this run members
    df_run_members = pd.DataFrame.merge(
        df_run_members,
        run_info,
        on="run_id"
    )
    
    #we dont need that info about run members anymore 
    df_run_members.pop("run_id")

    #getting last action in the member_creation prosses 
    last_member_creation = df_run_members.pop("system_time").max()

    #getting details about all characters in this run
    df_run_members = pd.DataFrame.merge(
        df_run_members,
        #reading df_characters
        pd.read_parquet(dn_db_characters_table),
        on="character_id"
    )
    
    #naming items according to doc
    df_run_members = df_run_members.rename(
        mapper={
            "character_id": "id",
            "character_name": "name",
            "character_class": "class"
        },
        axis="columns"
    )
    
    #structuring info about our run members into dict object
        #add run members info into dict_to_send
    su_tools.extend_list_by_dict_from_df(
        df_run_members,
        dict_to_send["data"]["participants"]
    )
    df_run_members = None
    
    #reading table w/ info about events
        # we are not readint colums w/ # in the DataFrame
    df_for_events = pd.read_parquet(
        dn_db_events_table, 
        columns=[
            "event_id",
            "run_id",
            "boss_id",
            "item_id",
            "character_id",
            "system_time" 
        ]
    )
    
    #getting events only for our run
    df_for_events = pd.DataFrame.merge(
        df_for_events,
        run_info,
        on="run_id"
    )
    
    #getting last action in the event_creation prosses 
    last_action = df_for_events.pop("system_time").max()

    #the latest action is written into 
        #dict_to_send["data"]["last_action"]
    if last_action > last_member_creation:
        dict_to_send["data"]["date_finished"] = last_action
    elif last_action < last_member_creation:
        dict_to_send["data"]["date_finished"] = last_member_creation
    
    df_runs.loc[run_index,"date_finished"]= \
            dict_to_send["data"]["date_finished"]
    
    
    df_runs.to_parquet(
        dn_db_runs_table,
        engine="pyarrow"
    )
    
    #clearing variables that we wont use anymore
    raid_run_id = None
    
    #we dont need that info about events anymore 
    df_for_events.pop("run_id")
    
    df_for_events = df_for_events.rename(
        {
            "boss_id": "boss_dropped_from",
            "character_id": "character_assigned_to"
        },
        axis="columns"
    )
    
    su_tools.extend_list_by_dict_from_df(
        df_for_events,
        dict_to_send["data"]["loot_distributed"]
    )
    df_for_events = None
    
    #end timer
    e_t = time.perf_counter()
    print(f"Time of {raid_run_info_m.__name__}={e_t-s_t}")
    
    #sendind gathered info about run
    return json.dumps(dict_to_send, indent=2, cls=su_tools.MyEncoder)

def call_raid_run_info_m(
    run_id,
    dynamic_database,
    static_database,
    message= {"result" : True}
):
    result = raid_run_info_m(
        run_id,
        #dynamic database
        dn_db_runs_table=dynamic_database["runs_table"],
        dn_db_events_table=dynamic_database["events_table"],
        dn_db_run_members=dynamic_database["run_members"],
        dn_db_characters_table=dynamic_database["characters_table"],
        #static database
        st_db_raid_table=static_database["raid_table"],
        message=message
    )
    return result




def edit_run_m (
    run_id,
    #dynamic database
    dn_db_runs_table,
    dn_db_events_table
):
    raid_run_id = int(escape(run_id))
    
    #info that comes w/ the request
    run_update = pd.DataFrame.from_dict(request.json, orient="index")
    
    #reading tables w/ info about
    df_for_runs = pd.read_parquet(dn_db_runs_table) #runs
    df_for_events = pd.read_parquet( #events
        dn_db_events_table,
        #dtype={
        #    "run_id": np.int32,
        #    "boss_id": np.int32,
        #    "item_id": np.int32,
        #    "character_id": np.float64,
        #    "system_time": object
        #}
    ) 
    
    #check is there such run
    run_existence = su_tools.find_one_row_in_DataFrame(
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
        new_event_ids.append(
            #create new event
            add_row.add_a_row_with_id_and_exact_time(
                df_for_events,
                list_with_info=[
                    int(run_update.iloc[event].at["run_id"]),
                    int(run_update.iloc[event].at["boss_id"]),
                    int(run_update.iloc[event].at["item_id"]),
                    run_update.iloc[event].at["character_id"],
                ]
            )
        )
        
    #write info w/ new events into the table 
    df_for_events.to_parquet(
        dn_db_events_table,
        engine="pyarrow"
    )
    
    #returning list of new event_id -s as the respons
    dict_to_return = '''{"event_id" : %s}''' %new_event_ids
    result = json.loads(dict_to_return)
    return json.dumps(result)             