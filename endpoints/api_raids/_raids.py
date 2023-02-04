
import numpy as np
import pandas as pd
import json

def give_info_about_all_raids (static_database):
    #read the table w/ info about raids
    df_for_raids = pd.read_csv(
        static_database["raid_table"]
    )
    
    result = json.loads(df_for_raids.to_json(orient="records"))
    #orient="records" gives us -> 
        #info about every raid in form of the list
            #each elem of list have:
            #   "raid_id"
            #   "raid_name"
            #   "raid_type"
    
    return json.dumps(result, indent=2)