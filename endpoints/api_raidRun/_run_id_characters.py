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

import utils.tools as u_tools
import utils.add_row as add_row

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
            "not_in_the_run" : None
        }
    else: 
        #massage if we did find someone, who wasnt in the run
        message = {
            "result" : True,
            "were_not_in_the_run": they_werent_in_the_run
        }
    return(message)
            
        