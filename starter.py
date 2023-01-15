import numpy as np
import pandas as pd
import json

from flask import Flask, request, Response, jsonify, json
from markupsafe import escape

import utils.tools as u_tools

app = Flask(__name__)
enctype="multipart/form-data"

static_database = {
    "raid_table" : "Data/Static_database/Wow app - Raid table.csv",
    "boss_table" : "Data/Static_database/Wow app - Bosses table.csv",
    "item_table" : "Data/Static_database/Items.csv"
}

dynamic_database = {
    "guilds_table" : "Data/Dynamic_database/guilds_table.csv",
    "characters_table" : "Data/Dynamic_database/characters_table.csv",
    "runs_table" : "Data/Dynamic_database/runs_of_the_guilds_table.csv",
    "events_table" : "Data/Dynamic_database/events_table.csv"
}




@app.route('/')
def index():
    return 'Index Page'

@app.route('/books')
def list_of_books():
    books = [
        {'name': 'The Call of the Wild', 'author': 'Jack London'},
        {'name': 'Heart of Darkness', 'author': 'Joseph Conrad'}
    ]
    #return json.dumps(books, indent=4)
    return jsonify(books)

@app.route("/guildStats/<name>") #methods = ["GET"]
#get all data about the guild
def give_all_aviable_guild_stats(name):
    #recieve guild name to look for
    guild_name = escape(name) 

    #define variables
    guild_info = pd.Series()

    #read table w/ guilds info
    df_to_work_with_guild = u_tools.read_the_file_to_DF(dynamic_database["guilds_table"])
    #print(df_to_work_with_guild)
    #get all guild's info
    guild_info = u_tools.find_1_row_in_DataFrame(
        df_to_work_with_guild,
        object_to_search_for = guild_name,
        item_column = "guild_name"
        )
    #check is there such guild
    guild_info_type = guild_info.__class__.__name__
    if guild_info_type == "NoneType" :
        return jsonify("There is no such guild")   

    #read table w/ characters info
    df_to_work_with_characters = u_tools.read_the_file_to_DF(dynamic_database["characters_table"])
    
    #find all members of the given guild
    df_to_return = u_tools.find_many_rows_in_DataFrame(
        df_to_work_with_characters,
        object_to_search_for = guild_info.loc["guild_id"],
        item_column = "guild_id"
        )
    result = json.loads(df_to_return.to_json(orient="index"))
    return json.dumps(result, indent=2)

@app.route("/raids") #methods = ["GET"]
#user wants to create new raid and we need to give all of the raid to him
def create_new_raid ():
    df_to_work_with = u_tools.read_the_file_to_DF(static_database["raid_table"])
    df_to_send = df_to_work_with.iloc[:,[0,1]]
    result = json.loads(df_to_send.to_json(orient="index"))
    return json.dumps(result, indent=2)

@app.route("/characters/<name>") #methods = ["GET"]
#giving all the characters in the certain guild
def characters_of_the_guild (name):
    #recieve guild name to look for
    guild_name = escape(name) 

    #define variables
    guild_info = pd.Series()

    #read table w/ guilds info
    df_to_work_with_guild = u_tools.read_the_file_to_DF(dynamic_database["guilds_table"])
    
    #get all guild's info
    guild_info = u_tools.find_1_row_in_DataFrame(
        df_to_work_with_guild,
        object_to_search_for = guild_name,
        item_column = "guild_name"
        )
    #check is there such guild
    guild_info_type = guild_info.__class__.__name__
    if guild_info_type == "NoneType" :
        return jsonify("There is no such guild")   

    #read table w/ characters info
    df_to_work_with_characters = u_tools.read_the_file_to_DF(dynamic_database["characters_table"])
    
    #find all members of the given guild
    df_to_return = u_tools.find_many_rows_in_DataFrame(
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

"""
@app.route("/raidRun", methods = ["POST"])
def a():

    return()

@app.route("/raid/:id") #methods = ["GET"]
def a():

    return()

@app.route("/raidRun/:id", methods = ["GET", "PUT"])
def a():

    return()

@app.route("/raidRuns") #methods = ["GET"]
def a():

    return()
"""

if __name__ == "__main__":
    app.run(debug=True)
