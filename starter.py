import numpy as np
import pandas as pd
import json
import datetime

import time

from flask import Flask, request, Response, jsonify, json, render_template
from markupsafe import escape

import utils.tools as u_tools
import utils.add_row as add_row

from endpoints import (
    api_characters_g_id,
    api_guildStats_g_id,
    api_raids,
    api_raid_id,
    api_raidRun,
    api_raidRun_g_id,
    api_raidRuns_g_id,
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


@app.route("/api/guildStats/<g_id>") #methods = ["GET"]
#get all data about the guild
#right now gives only list of guild members
def give_all_aviable_guild_stats(g_name):
    result = api_guildStats_g_id.give_all_aviable_guild_stats_m(g_name,dynamic_database)
    return(result)


@app.route("/api/raids") #methods = ["GET"]
#user wants to create new raid and we need to give all of the raid to him
def give_info_about_all_raids ():
    #read the table w/ info about raids
    result = api_raids.give_info_about_all_raids(static_database)
    return(result)

    
@app.route("/api/raid/<id>") #methods = ["GET"]
#give all data about specific raid by it's id
def info_about_raid_id(id):
    result = api_raid_id.info_about_raid_id_m(id, static_database)
    return(result)


@app.route("/api/characters/<g_id>") #methods = ["GET"]
#giving all the characters in the certain guild
def characters_of_the_guild (g_id):
    result = api_characters_g_id.characters_of_the_guild_m(g_id,dynamic_database)
    return(result)


@app.route("/api/raidRun", methods = ["POST"])
#create new run
def runs_of_the_guild():
    result = api_raidRun.runs_of_the_guild_m(dynamic_database)
    return(result)


@app.route("/api/raidRun/<g_id>", methods = ["GET", "PUT"])
#PUT - update run_id
#GET - get info about run_id 
def edit_raid_run (g_id):
    result = api_raidRun_g_id.edit_raid_run_m(g_id, dynamic_database, static_database)
    return(result)


@app.route("/api/raidRuns/<g_id>") #methods = ["GET"]
#get info about all runs of the guild
def get_all_guilds_runs(g_id):
    result = api_raidRuns_g_id.get_all_guilds_runs_m(g_id, dynamic_database)
    return (result)

"""
"""

if __name__ == "__main__":
    app.run(
        debug=True
    )
