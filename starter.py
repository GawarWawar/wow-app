import numpy as np
import pandas as pd
import json

from flask import Flask, request, Response, jsonify, json
from markupsafe import escape

import utils.tools as u_tools

app = Flask(__name__)
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


@app.route("/guildStats/<name>") #methods = ["GET"]
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


@app.route("/raids") #methods = ["GET"]
#user wants to create new raid and we need to give all of the raid to him
def create_new_raid ():
    #read the table w/ info about raids
    df_to_work_with = pd.read_csv(
        static_database["raid_table"]
    )
    
    #get needed columns where the info stored
    df_to_send = df_to_work_with.loc[:,["raid_id","raid_name"]]
    
    result = json.loads(df_to_send.to_json(orient="index"))
    return json.dumps(result, indent=2)


@app.route("/characters/<guild_name>") #methods = ["GET"]
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
    df_to_return = u_tools.find_rows_in_DataFrame(
        df_to_work_with_characters,
        object_to_search_for = guild_info.loc["guild_id"],
        item_column = "guild_id"
    )
    
    #check is there any member of that guild
    df_to_return_type = df_to_return.__class__.__name__
    if df_to_return_type == "NoneType" :
        return jsonify("There is no members in",guild_name)

    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)


@app.route("/raidRun", methods = ["POST"])
def runs_of_the_guild():
    
    return()


#give all data about specific raid by it's id
#need to add loot from bosses
@app.route("/raid/<id>") #methods = ["GET"]
def info_about_raid_id(id):
    #getting raid id to look for
    raid_id = int(escape(id))
    
    #read table w/ raid info
    df_to_work_with_raid = pd.read_csv(
        static_database["raid_table"]
        )
    
    #looking for the specific raid id
    raid_info = u_tools.find_one_row_in_DataFrame(
        df_to_work_with_raid,
        object_to_search_for = raid_id,
        item_column = "raid_id"
    )
    
    #check is there such raid
    raid_info_type = raid_info.__class__.__name__
    if raid_info_type == "NoneType" :
        return jsonify("There is no such raid")
    
    #reading table w/ bosses info
    df_to_work_with_bosses = pd.read_csv(
        static_database["boss_table"]
        )
    
    #looking for the bosses in our raid
    needed_bosses = u_tools.find_rows_in_DataFrame(
            df_to_work_with_bosses,
            object_to_search_for = raid_id,
            item_column = "raid_id"
    )
    
    #reading table w/ dropp info
    df_to_work_with_drop = pd.read_csv(
        static_database["drop_table"]
    )

    
    #looking for the loot for our bosses
    needed_items = u_tools.many_to_many_finder(
        df_to_work_with_drop,
        needed_bosses.loc[:,"boss_id"],
        "boss_id"
    )

    #combining info into 1 substance
    df_to_return = pd.merge(raid_info.to_frame().T,
                            needed_bosses,
                            on="raid_id")

    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)

"""
@app.route("/raidRun/:id", methods = ["GET", "PUT"])
def a():

    return()

@app.route("/raidRuns") #methods = ["GET"]
def a():

    return()
"""

if __name__ == "__main__":
    app.run(debug=True)
