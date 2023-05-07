import numpy as np
import pandas as pd
import json

import time

from os.path import dirname, abspath
import sys

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.simple_utils.simple_tools as su_tools
from utils.simple_utils import add_row

def check_character_existence_add_if_not (
    df_characters, #df for all characters (characters table)
    #members of run we need to check if they exist in df_characters
    df_run_members, 
    run_member_counter, #inside counter for the members
    #if we need to create new member, give him this id
    new_members_guild_id 
):
    #find character in the character table
    member_existence = \
        su_tools.find_item_in_DataFrame_without_for(
            df_characters,
            df_run_members.loc[run_member_counter,"name"],
            "character_name"
        )
        
    #check if this character already exist 
    if member_existence.empty:
        #adding new character to the character_table
        character_id = add_row.add_a_row_with_id(
            df_characters,
            list_with_info=[
                df_run_members.loc[run_member_counter,"name"],
                new_members_guild_id,
                df_run_members.loc[run_member_counter,"character_class"], 
            ]
        )
    else:
        #if exist -> getting its id
        character_id = member_existence.iloc[0].at["character_id"] 
    
    return(character_id)