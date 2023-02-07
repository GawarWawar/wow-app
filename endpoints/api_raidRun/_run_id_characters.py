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

import utils.simple_utils.simple_tools as su_tools
import utils.simple_utils.add_row as add_row
import utils.tools as u_tools

def delet_run_members_m (
    run_id,
    #dynamic database
    dn_db_run_members
):
    run_id = int(escape(run_id))
    
    #creating DataFrame w/ info about character we need to delete
    members_to_delete = request.json
    members_to_delete_df = pd.DataFrame(
        members_to_delete,
        columns=["character_id"]
    )
    #creating copy of character_id, to give in response if:
        #there were no character w/ this id  
    members_to_delete_df["character_id_copy"] = \
        members_to_delete_df["character_id"].copy()
    #creating 2nd part of the key 
    members_to_delete_df["run_id"] = run_id
    #setting the key as the criteria to look for 
    members_to_delete_df=members_to_delete_df.set_index(
        ["character_id","run_id"]
    )
    
    #reading talbe w/ members of all runs 
    df_run_members = pd.read_csv(dn_db_run_members)
    
    #setting the same key as in the members_to_delete_df
    df_run_members = df_run_members.set_index(["character_id","run_id"])
    
    they_werent_in_the_run = []
    #lookign for every member to delete from run
    for member in members_to_delete_df.index:
        #check if there is run_member w/ that id
        try:
            #delete member if find
            df_run_members=df_run_members.drop(member)
        except KeyError:
            #add to the respons if not find
            they_werent_in_the_run.append(
                int(
                    members_to_delete_df.loc[member,"character_id_copy"]
                )
            )
    
    #reset index keys after deletion 
    df_run_members = df_run_members.reset_index()
    
    #write new talbe into the file
    df_run_members.to_csv(
        dn_db_run_members,
        index=False,
        index_label=False
    )
    
    #forming respons
    if len(they_werent_in_the_run) == 0:
        #massage if we didnt find anyone, who wasnt in the run
        message={
            "result" : True,
            "were_not_in_the_run" : None
        }
    else: 
        #massage if we did find someone, who wasnt in the run
        message = {
            "result" : True,
            "were_not_in_the_run": they_werent_in_the_run
        }
    return(message)
            
def add_new_run_members (
    run_id,
    #dynamic database
    dn_db_runs_table,
    dn_db_run_members,
    dn_db_characters_table
):
    run_id = int(escape(run_id))
    
    #forming df of characters that we need to add to run
    members_to_add = request.json
    members_to_add = pd.DataFrame.from_records(members_to_add)
    members_to_add = members_to_add.rename(
        {
            "class": "character_class"
        },
        axis="columns"
    )
    
    #getting run info from dn_db_runs_table 
    run_info = pd.read_csv(dn_db_runs_table)
    run_info = su_tools.find_item_in_DataFrame_without_for(
        run_info,
        run_id,
        "run_id"
    )
    
    #reading info about all existing characters
    df_characters = pd.read_csv(
        dn_db_characters_table
    )
    
    #checking existence of all characters
    #if character doesnt exist -> add him to the list of characters 
    character_id_list = [] #-> all characters id we need to add to run
    for run_member_counter in range(
        len(members_to_add.loc[:,"name"])
    ):
        character_id = u_tools.check_character_existence_add_if_not(
            df_characters,
            members_to_add,
            run_member_counter,
            run_info.iloc[0].at["guild_id"]
        )
        character_id_list.append(character_id)
    
    #write df_character into file here
    df_characters.to_csv(
        dn_db_characters_table,
        index=False,
        index_label=False
    )
    df_characters = None
    
    #reading info about all run_members
    df_run_members = pd.read_csv(
        dn_db_run_members
    )
    
    #checking existence of all new run members into our run
    #if character doesnt exist -> add him to the list of run_members 
    they_were_in_the_run = [] #-> all characters_id that were 
                                    #already in the run
    for character_id in character_id_list:
        #checking in 2 stages bcz key contains in 2 columns
        character_to_find = su_tools.\
            find_item_in_DataFrame_without_for(
                df_run_members,
                character_id,
                "character_id"
            )
        character_to_find = su_tools.\
            find_item_in_DataFrame_without_for(
                character_to_find,
                run_id,
                "run_id"
            )
        
        if character_to_find.empty:
            #adding run member to the table
            add_row.twoo_columns_and_exect_time(
                df_run_members,
                dict_w_info ={
                    #info about that character we need to write
                    0: run_id,
                    1: character_id
                }
            )
        else:
            they_were_in_the_run.append(int(character_id))
          
    #write new df_run_members into the file
    df_run_members.to_csv(
        dn_db_run_members,
        index=False,
        index_label=False
    )
    
    #forming respons
    if len(they_were_in_the_run) == 0:
        #massage if we didnt find anyone, who was in the run
        message={
            "result" : True,
            "were_in_the_run" : None
        }
    else: 
        #massage if we did find someone, who was in the run
        message = {
            "result" : True,
            "were_in_the_run": they_were_in_the_run
        }
    return(message)