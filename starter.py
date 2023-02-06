import numpy as np
import pandas as pd
import json
import datetime

import time

from flask import Flask, request, Response, jsonify, json, render_template
from markupsafe import escape
from endpoints.api_guidStats import _g_id, _g_id_characters, _g_id_raidRuns
from endpoints.api_raidRun import _raidRun, _run_id, _run_id_characters, _run_id_drops
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


@app.route("/api/raids") #methods = ["GET"]
#user wants to create new raid and we need to give all of the raid to him
def give_info_about_all_raids ():
    #read the table w/ info about raids
    result = _raids.give_info_about_all_raids(
        st_db_raid_table=static_database["raid_table"]
    )
    return(result)

    
@app.route("/api/raids/<raid_id>") #methods = ["GET"]
#give all data about specific raid by it's id
def info_about_raid_id(raid_id):
    result = _raid_id.info_about_raid_id_m(
        raid_id,
        st_db_raid_table=static_database["raid_table"],
        st_db_boss_table=static_database["boss_table"],
        st_db_loot_table=static_database["loot_table"],
        st_db_item_table=static_database["item_table"]
    )
    return(result)


@app.route("/api/guildStats/<g_id>") #methods = ["GET"]
#get all data about the guild
#right now gives only list of guild members
def give_all_aviable_guild_stats(g_id):
    result = _g_id.give_all_aviable_guild_stats_m(
        g_id,
        #dynamic_database
        dn_db_guilds_table=dynamic_database["guilds_table"],
        dn_db_characters_table=dynamic_database["characters_table"]
    )
    return(result)


@app.route("/api/guildStats/<g_id>/characters") #methods = ["GET"]
#giving all the characters in the certain guild
def characters_of_the_guild (g_id):
    result = _g_id_characters.characters_of_the_guild_m(
        g_id,
        dn_db_guilds_table=dynamic_database["guilds_table"],
        dn_db_characters_table=dynamic_database["characters_table"]
    )
    return(result)


@app.route("/api/guildStats/<g_id>/raidRuns") #methods = ["GET"]
#get info about all runs of the guild
def get_all_guilds_runs(g_id):
    result = _g_id_raidRuns.get_all_guilds_runs_m(
        g_id,
        #dynamic_database
        dn_db_guilds_table= dynamic_database["guilds_table"],
        dn_db_runs_table= dynamic_database["runs_table"],
        #static_database
        st_db_raid_table = static_database["raid_table"]
    )
    return (result)


@app.route("/api/raidRun", methods = ["POST"])
#create new run
def runs_of_the_guild():
    new_run_id = _raidRun.create_new_run_m(
        dn_db_runs_table=dynamic_database["runs_table"],
        dn_db_characters_table=dynamic_database["characters_table"],
        dn_db_run_members=dynamic_database["run_members"]
    )
    #forming basik response 
    result = _run_id.raid_run_info_m(
        new_run_id,
        #dynamic database
        dn_db_runs_table=dynamic_database["runs_table"],
        dn_db_events_table=dynamic_database["events_table"],
        dn_db_run_members=dynamic_database["run_members"],
        dn_db_characters_table=dynamic_database["characters_table"],
        #static database
        st_db_raid_table=static_database["raid_table"],
        st_db_item_table=static_database["item_table"],
        st_db_boss_table=static_database["boss_table"]
    )
    
    return(result)


@app.route("/api/raidRun/<run_id>", methods = ["GET", "PUT"])
#PUT - update run_id
#GET - get info about run_id 
def raid_run (run_id):
    if request.method == "GET":
        result = _run_id.raid_run_info_m(
            run_id,
            #dynamic database
            dn_db_runs_table=dynamic_database["runs_table"],
            dn_db_events_table=dynamic_database["events_table"],
            dn_db_run_members=dynamic_database["run_members"],
            dn_db_characters_table=dynamic_database["characters_table"],
            #static database
            st_db_raid_table=static_database["raid_table"],
            st_db_item_table=static_database["item_table"],
            st_db_boss_table=static_database["boss_table"]
        )
    elif request.method == "PUT":
        result = _run_id.edit_run_m(
            run_id,
            dn_db_runs_table=dynamic_database["runs_table"],
            dn_db_events_table=dynamic_database["events_table"]
        )
    return(result)


@app.route("/api/raidRun/<run_id>/characters", methods=["POST","DELETE"])
def edit_run_members (run_id):
    if request.method == "DELETE":
        message = _run_id_characters.delet_run_members_m(
            run_id,
            dn_db_run_members=dynamic_database["run_members"]
        )
        result = _run_id.raid_run_info_m(
                run_id,
                #dynamic database
                dn_db_runs_table=dynamic_database["runs_table"],
                dn_db_events_table=dynamic_database["events_table"],
                dn_db_run_members=dynamic_database["run_members"],
                dn_db_characters_table=dynamic_database["characters_table"],
                #static database
                st_db_raid_table=static_database["raid_table"],
                st_db_item_table=static_database["item_table"],
                st_db_boss_table=static_database["boss_table"],
                #message
                message=message
        )
        return(result)


@app.route("/api/raidRun/<run_id>/drops", methods=["POST","DELETE"])
def edit_run_drops (run_id):
    return("a")
    

"""
"""

if __name__ == "__main__":
    app.run(
        debug=True
    )
