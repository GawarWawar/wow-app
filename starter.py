import numpy as np
import pandas as pd
import json

from flask import Flask, request, Response, jsonify, json
from markupsafe import escape

from utils.tools import read_the_file_to_DF, find_item_in_DataFrame

app = Flask(__name__)
enctype="multipart/form-data"

static_database = {
    "raid_table" : "Data/Static_database/Wow app - Raid table.csv",
    "boss_table" : "Data/Static_database/Wow app - Bosses table.csv",
    "item_table" : "Data/Static_database/Items.csv"
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

@app.route("/guildStats") #methods = ["GET"]
#get all data about the guild
def give_all_aviable_guild_stats():

    return()

@app.route("/raids") #methods = ["GET"]
#user wants to create new raid and we need to give all of the raid to him
def create_new_raid ():
    df_to_work_with = read_the_file_to_DF(static_database["raid_table"])
    df_to_send = df_to_work_with.iloc[:,[0,1]]
    result = json.loads(df_to_send.to_json(orient="index"))
    return json.dumps(result, indent=2)
@app.route("/characters") #methods = ["GET"]
#giving all the characters in the certain guild
def characters_of_the_guild ():
    
    return()

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
