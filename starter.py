import numpy as np
import pandas as pd
import json

import time
import datetime

from flask import Flask, request, Response, jsonify, json, render_template
from markupsafe import escape

import utils.tools as u_tools
import utils.add_row as add_row

render_dir = "FE"

app = Flask(__name__, template_folder=render_dir)
enctype="multipart/form-data"


static_database = {
    "raid_table" : "data/Static_database/Wow app - Raid table.csv",
    "boss_table" : "data/Static_database/Wow app - Bosses table.csv",
    "drop_table" : "data/Static_database/drop_of_bosses.csv",
    "item_table" : "data/Static_database/Items.csv"
}

dynamic_database = {
    "guilds_table" : "data/Dynamic_database/guilds_table.csv",
    "characters_table" : "data/Dynamic_database/characters_table.csv",
    "runs_table" : "data/Dynamic_database/runs_of_the_guilds_table.csv",
    "events_table" : "data/Dynamic_database/events_table.csv",
    "run_members" : "data/Dynamic_database/run_members.csv"
}


@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/api/guildStats/<name>") #methods = ["GET"]
#get all data about the guild
#right now gives only list of guild members
def give_all_aviable_guild_stats(name):
    guild_name = escape(name) 
    guild_info = pd.Series()
    
    #read table w/ guilds info
    df_for_guild = pd.read_csv(
        dynamic_database["guilds_table"]
    )

    #get all guild's info
    guild_info = u_tools.find_one_row_in_DataFrame(
        df_for_guild,
        object_to_search_for = guild_name,
        item_column = "guild_name"
        )
    
    #check is there such guild
    guild_info_type = guild_info.__class__.__name__
    if guild_info_type == "NoneType" :
        return jsonify("There is no such guild")   
    
    #read table w/ characters info
    df_for_characters = pd.read_csv(
        dynamic_database["characters_table"]
        )
    
    #find all members of the given guild
    df_to_return = u_tools.find_rows_in_DataFrame(
        df_for_characters,
        object_to_search_for = guild_info.loc["guild_id"],
        item_column = "guild_id"
        )
    
    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)


@app.route("/api/raids") #methods = ["GET"]
#user wants to create new raid and we need to give all of the raid to him
def give_info_for_the_new_raid ():
    #read the table w/ info about raids
    df_for = pd.read_csv(
        static_database["raid_table"]
    )
    
    #get needed columns where the info stored
    df_to_send = df_for.loc[:,["raid_id","raid_name","raid_type"]]
    
    result = json.loads(df_to_send.to_json(orient="index"))
    return json.dumps(result, indent=2)


@app.route("/api/characters/<guild_name>") #methods = ["GET"]
#giving all the characters in the certain guild
def characters_of_the_guild (guild_name):
    guild_name = escape(guild_name) 

    #read table w/ guilds info
    df_for_guild = pd.read_csv(
        dynamic_database["guilds_table"]
        )
    
    #get all guild's info
    guild_info = u_tools.find_one_row_in_DataFrame(
        df_for_guild,
        object_to_search_for = guild_name,
        item_column = "guild_name"
    )
    
    #check is there such guild
    guild_info_type = guild_info.__class__.__name__
    if guild_info_type == "NoneType" :
        return jsonify("There is no such guild")   

    #read table w/ characters info
    df_for_characters = pd.read_csv(dynamic_database["characters_table"])
    
    #find all members of the given guild
    df_to_return = pd.DataFrame.merge(
        guild_info.to_frame().T,
        df_for_characters,
        on="guild_id")

    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)


@app.route("/api/raidRun", methods = ["POST"])
def runs_of_the_guild():
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

#give all data about specific raid by it's id
@app.route("/api/raid/<id>") #methods = ["GET"]
def info_about_raid_id(id):
    #getting raid id to look for
    raid_id = int(escape(id))
    
    #read table w/ raid info
    df_to_return = pd.read_csv(
        static_database["raid_table"]
        )
    #looking for the specific raid id
    df_to_return = u_tools.find_one_row_in_DataFrame(
        df_to_return,
        object_to_search_for = raid_id,
        item_column = "raid_id"
    )
    
    #check is there such raid
    df_to_return_type = df_to_return.__class__.__name__
    if df_to_return_type == "NoneType" :
        return jsonify("There is no such raid")
    
    #reading table w/ bosses info
    df_for_bosses = pd.read_csv(
        static_database["boss_table"]
        )
    #add bosses of our raid
    df_to_return = pd.DataFrame.merge(
        df_to_return.to_frame().T,
        df_for_bosses,
        on="raid_id")

    
    #reading table w/ dropp info
    df_for_drop = pd.read_csv(
        static_database["drop_table"]
    )
    #add drop from selected bosses
    df_to_return = pd.merge(
        df_for_drop, 
        df_to_return, 
        on="boss_id" 
    )
    
    #read items info
    df_items = pd.read_csv(
        static_database["item_table"]
    )
    #add items info to the drops table
    df_to_return = pd.merge(
        df_to_return,
        df_items,
        on="item_id"
    )
    
    #sort respons to be in a-z order by "boss_id" 
    df_to_return = df_to_return.sort_values(by="boss_id", ignore_index=True)

    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)

@app.route("/api/raidRun/<id>", methods = ["GET", "PUT", "DELETE"])
def edit_raid_run(id):
    raid_run_id = int(id)
    
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
        
        #cheking every event that were updated
        new_event_ids = []
        for event in range(len(run_update)):
            #get event from the event table
            i_event = run_update.iloc[event]
            i_event = pd.merge(
                i_event.to_frame().T, 
                df_for_events, 
                on=["run_id", "boss_id", "item_id"],
                suffixes=["_new","_old"]
            )
            
            #check is there such event
            if len(i_event) == 0:
                exact_time = datetime.datetime.now() #system time
                #if there is non -> create new one
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
            else:
                #if there is one -> update it
                df_for_events.loc[i_event.loc[0,"event_id"],"character_id"] = \
                    i_event.at[0,"character_id_new"]
    
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
   
# elif request.method == "DELETE":
#        b=1
    
    else:
        df_to_return = u_tools.find_item_in_DataFrame_without_for(
            df_for_runs,
            raid_run_id,
            "run_id"
        )

        df_to_return = pd.DataFrame.merge(
            df_to_return,
            df_for_events,
            on="run_id"
        )
        
        df_for_characters = pd.read_csv(dynamic_database["characters_table"])
        
        df_to_return = pd.DataFrame.merge(
            df_to_return,
            df_for_characters,
            on="character_id",
            suffixes=["_run","_character"]
        )
        
        df_for_items = pd.read_csv(static_database["item_table"])
        
        df_to_return = pd.DataFrame.merge(
            df_to_return,
            df_for_items,
            on="item_id"
        )
        print(df_to_return)
        
        result = json.loads(df_to_return.to_json(orient="index"))
        return json.dumps(result, indent=2)


"""
@app.route("/api/raidRuns") #methods = ["GET"]
def a():

    return()
"""

if __name__ == "__main__":
    app.run(debug=True)
