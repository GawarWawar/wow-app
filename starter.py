import numpy as np
import pandas as pd
import json

import time
import datetime

from flask import Flask, request, Response, jsonify, json, render_template
from markupsafe import escape

import utils.tools as u_tools
import utils.add_row as add_row

from endpoints import (
    api_characters_guild_name,
    api_raidRun,
    api_raid_id,
    api_raidRun_id,
    api_raidRuns_g_id,
    api_raids
)

render_dir = "FE"

app = Flask(__name__, template_folder=render_dir)
enctype="multipart/form-data"


static_database = {
    "raid_table" : "data/Static_database/Wow app - Raid table.csv",
    "boss_table" : "data/Static_database/Wow app - Bosses table.csv",
    "loot_table" : "data/Static_database/loot_of_bosses.csv",
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
def give_info_about_all_raids ():
    #read the table w/ info about raids
    result = api_raids.give_info_about_all_raids(static_database)
    return(result)


@app.route("/api/characters/<guild_name>") #methods = ["GET"]
#giving all the characters in the certain guild
def characters_of_the_guild (guild_name):
    result = api_characters_guild_name.characters_of_the_guild_m(guild_name,dynamic_database)
    return(result)


@app.route("/api/raidRun", methods = ["POST"])
#create new run
def runs_of_the_guild():
    result = api_raidRun.runs_of_the_guild_m(dynamic_database)
    return(result)

    
#give all data about specific raid by it's id
@app.route("/api/raid/<id>") #methods = ["GET"]
def info_about_raid_id(id):
    result = api_raid_id.info_about_raid_id_m(id, static_database)
    return(result)


@app.route("/api/raidRun/<id>", methods = ["GET", "PUT"])
def edit_raid_run (id):
    result = api_raidRun_id.edit_raid_run_m(id, dynamic_database, static_database)
    return(result)


@app.route("/api/raidRuns/<g_id>") #methods = ["GET"]
def get_all_guilds_runs(g_id):
    result = api_raidRuns_g_id.get_all_guilds_runs_m(g_id, dynamic_database)
    return (result)

"""
"""

if __name__ == "__main__":
    app.run(debug=True)
