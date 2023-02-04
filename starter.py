import numpy as np
import pandas as pd
import json
import datetime

import time

from flask import Flask, request, Response, jsonify, json, render_template
from markupsafe import escape
from endpoints.api_guidStats import _g_id, _g_id_characters, _g_id_raidRuns
from endpoints.api_raidRun import _raidRun, _run_id
from endpoints.api_raids import _raid_id, _raids

import utils.tools as u_tools
import utils.add_row as add_row

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
def give_all_aviable_guild_stats(g_id):
    result = g_id.give_all_aviable_guild_stats_m(g_id,dynamic_database)
    return(result)


@app.route("/api/raids") #methods = ["GET"]
#user wants to create new raid and we need to give all of the raid to him
def give_info_about_all_raids ():
    #read the table w/ info about raids
    result = _raids.give_info_about_all_raids(static_database)
    return(result)

    
@app.route("/api/raids/<id>") #methods = ["GET"]
#give all data about specific raid by it's id
def info_about_raid_id(id):
    result = _raid_id.info_about_raid_id_m(id, static_database)
    return(result)


@app.route("/api/guildStats/<g_id>/characters") #methods = ["GET"]
#giving all the characters in the certain guild
def characters_of_the_guild (g_id):
    result = _g_id_characters.characters_of_the_guild_m(g_id,dynamic_database)
    return(result)


@app.route("/api/raidRun", methods = ["POST"])
#create new run
def runs_of_the_guild():
    result = _raidRun.runs_of_the_guild_m(dynamic_database)
    return(result)


@app.route("/api/raidRun/<run_id>", methods = ["GET", "PUT"])
#PUT - update run_id
#GET - get info about run_id 
def raid_run (run_id):
    result = _run_id.edit_raid_run_m(run_id, dynamic_database, static_database)
    return(result)


@app.route("/api/guildStats/<g_id>/raidRuns") #methods = ["GET"]
#get info about all runs of the guild
def get_all_guilds_runs(g_id):
    result = _g_id_raidRuns.get_all_guilds_runs_m(g_id, dynamic_database, static_database)
    return (result)

"""
"""

if __name__ == "__main__":
    app.run(
        debug=True
    )
