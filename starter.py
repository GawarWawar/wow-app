import numpy as np
import pandas as pd
import json

import time

from flask import Flask, request, Response, jsonify, json, render_template
from markupsafe import escape

import utils.tools as u_tools

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
    "events_table" : "data/Dynamic_database/events_table.csv"
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
    df_to_work_with_guild = pd.read_csv(
        dynamic_database["guilds_table"]
    )

    #get all guild's info
    guild_info = u_tools.find_one_row_in_DataFrame(
        df_to_work_with_guild,
        object_to_search_for = guild_name,
        item_column = "guild_name"
        )
    
    #check is there such guild
    guild_info_type = guild_info.__class__.__name__
    if guild_info_type == "NoneType" :
        return jsonify("There is no such guild")   
    
    #read table w/ characters info
    df_to_work_with_characters = pd.read_csv(
        dynamic_database["characters_table"]
        )
    
    #find all members of the given guild
    df_to_return = u_tools.find_rows_in_DataFrame(
        df_to_work_with_characters,
        object_to_search_for = guild_info.loc["guild_id"],
        item_column = "guild_id"
        )
    
    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)


@app.route("/api/raids") #methods = ["GET"]
#user wants to create new raid and we need to give all of the raid to him
def give_info_for_the_new_raid ():
    #read the table w/ info about raids
    df_to_work_with = pd.read_csv(
        static_database["raid_table"]
    )
    
    #get needed columns where the info stored
    df_to_send = df_to_work_with.loc[:,["raid_id","raid_name","raid_type"]]
    
    result = json.loads(df_to_send.to_json(orient="index"))
    return json.dumps(result, indent=2)


@app.route("/api/characters/<guild_name>") #methods = ["GET"]
#giving all the characters in the certain guild
def characters_of_the_guild (guild_name):
    guild_name = escape(guild_name) 

    #read table w/ guilds info
    df_to_work_with_guild = pd.read_csv(
        dynamic_database["guilds_table"]
        )
    
    #get all guild's info
    guild_info = u_tools.find_one_row_in_DataFrame(
        df_to_work_with_guild,
        object_to_search_for = guild_name,
        item_column = "guild_name"
    )
    
    #check is there such guild
    guild_info_type = guild_info.__class__.__name__
    if guild_info_type == "NoneType" :
        return jsonify("There is no such guild")   

    #read table w/ characters info
    df_to_work_with_characters = pd.read_csv(dynamic_database["characters_table"])
    
    #find all members of the given guild
    df_to_return = pd.DataFrame.merge(
        guild_info.to_frame().T,
        df_to_work_with_characters,
        on="guild_id")

    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)


@app.route("/api/raidRun", methods = ["POST"])
def runs_of_the_guild():
    #accept info about new run
    new_run_df = pd.DataFrame.from_dict(request.json, orient="index")
    
    #read table with run info    
    df_to_work_with_runs = pd.read_csv(dynamic_database["runs_table"])
    
    #adding new run to the runs_table
    if len(df_to_work_with_runs.index)==0:
        #if we adding first run ever we will use the lenght of the table
        df_to_work_with_runs.loc[len(df_to_work_with_runs.index)] = [
                len(df_to_work_with_runs.index),
                new_run_df.loc["0","guild_id"],
                new_run_df.loc["0","raid_id"], 
                new_run_df.loc["0","date_of_raid"]
        ] 
    else:
        #if we are adding not the first run:
        #we are using privious last id to generate run_id for the new one
        run_id = df_to_work_with_runs.loc[:,"run_id"].iat[
            len(df_to_work_with_runs.index)-1
        ]
        
        len(df_to_work_with_runs.index)
        df_to_work_with_runs.loc[len(df_to_work_with_runs.index)] = [
                run_id+1,
                new_run_df.loc["0","guild_id"],
                new_run_df.loc["0","raid_id"], 
                new_run_df.loc["0","date_of_raid"]
        ]
    
    #writing runs back to the file
    df_to_work_with_runs.to_csv(
        dynamic_database["runs_table"],
        index=False,
        index_label=False
    )
    return("Done")

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
    df_to_work_with_bosses = pd.read_csv(
        static_database["boss_table"]
        )
    #add bosses of our raid
    df_to_return = pd.DataFrame.merge(
        df_to_return.to_frame().T,
        df_to_work_with_bosses,
        on="raid_id")

    
    #reading table w/ dropp info
    df_to_work_with_drop = pd.read_csv(
        static_database["drop_table"]
    )
    #add drop from selected bosses
    df_to_return = pd.merge(
        df_to_work_with_drop, 
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
    raid_run_id = id
    if request.method == "PUT":
        a=1
    return()

"""
@app.route("/api/raidRuns") #methods = ["GET"]
def a():

    return()
"""

if __name__ == "__main__":
    app.run(debug=True)
