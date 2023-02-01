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

import utils.tools as u_tools
import utils.add_row as add_row


def edit_raid_run_m(
    g_id,
    dynamic_database,
    static_database
):
    #start timer
    s_t = time.perf_counter()
    
    raid_run_id = int(escape(g_id))
    
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
        run_info = u_tools.find_item_in_DataFrame_without_for(
            df_for_runs,
            raid_run_id,
            "run_id"
        )
        
        #clearing variables that we wont use anymore
        df_for_runs = None
        raid_run_id = None
        
        #creating dictionary that we will send
        dict_to_send = {
            #adding already known info from run_info
            "guild_id": int(run_info.iloc[0].at["guild_id"]),
            "raid_id": int(run_info.iloc[0].at["raid_id"]),
            #creating structure
            "run_members":[],
            "bosses":[]
        }
        
        #reading tables w/ info
        df_characters = pd.read_csv(dynamic_database["characters_table"])
        df_for_items = pd.read_csv(static_database["item_table"])
        df_run_members = pd.read_csv(dynamic_database["run_members"])
        df_boos_table = pd.read_csv(static_database["boss_table"])
        
        #getting info about only this run members
        df_run_members = pd.DataFrame.merge(
            df_run_members,
            run_info,
            on="run_id"
        )
        
        #deliting info about run that come from run_info
            #and we wont use it
        df_run_members.pop("guild_id")
        df_run_members.pop("run_id")
        df_run_members.pop("system_time")
        df_run_members.pop("raid_id")
        df_run_members.pop("date_of_raid")
        
        #getting details about all characters in this run
        df_run_members = pd.DataFrame.merge(
            df_run_members,
            df_characters,
            on="character_id"
        )

        #structuring info about our run members into dict object
        df_run_members = df_run_members.to_json(orient="records", indent=2)

        #add run members info into dict_to_send
        dict_to_send["run_members"].extend(json.loads(df_run_members))
        
        #getting events only for our run
        df_for_events = pd.DataFrame.merge(
            df_for_events,
            run_info,
            on="run_id"
        )
        
        #getting info about every looted item in this run
        df_for_events = pd.DataFrame.merge(
            df_for_items,
            df_for_events,
            on="item_id"
        )
        
        #creating df about killed bosses
        df_bosses = df_for_events["boss_id"]
        #making bosses ids unique
        df_bosses = df_bosses.drop_duplicates()
        #make bosses to be in the a -> z order
        df_bosses.sort_values(inplace=True)
        
        #getting info about bosses, that were killed in this run
        df_bosses = pd.DataFrame.merge(
            df_bosses,
            df_boos_table,
            on="boss_id"
        )
        
        #deliting info about events that come from run_info
            #and we wont use it
        df_for_events.pop("guild_id")
        df_for_events.pop("raid_id")
        df_for_events.pop("date_of_raid")
        df_for_events.pop("run_id")
        df_for_events.pop("event_id")
        df_for_events.pop("system_time")
        
        #gather info about boss -> add to dict_to_send
        for boss in df_bosses.loc[:,"boss_id"]:
            add_boss = {
                #adding info that we already know
                "boss_id": int(df_bosses.iloc[boss].at["boss_id"]),
                "boss_name": df_bosses.iloc[boss].at["boss_name"],
                #forming structure for the loot
                "dropped_loot":[]
            }
            
            #getting loot for the boss, that we are adding r/n
            boss_loot = df_for_events[df_for_events.loc[:, "boss_id"] == boss]
            boss_loot.reset_index(inplace=True,drop=True)
            
            #dont need to add this info to the response
            boss_loot.pop("boss_id")
            
            #structuring info about our boss_loot into dict object
            boss_loot = boss_loot.to_json(orient="records", indent=2)
            
            #add boss_loot info into add_boss
            add_boss["dropped_loot"].extend(json.loads(boss_loot))
            
            #adding every boss to the dict_to_send
            dict_to_send["bosses"].append(add_boss)

        #end timer
        e_t = time.perf_counter()
        print(f"Time of {edit_raid_run_m.__name__}={e_t-s_t}")
        
        #sendind gathered info about run
        return json.dumps(dict_to_send, indent=2)

