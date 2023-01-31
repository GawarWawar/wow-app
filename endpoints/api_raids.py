
import numpy as np
import pandas as pd
import json

def give_info_about_all_raids (static_database):
    #read the table w/ info about raids
    df_for = pd.read_csv(
        static_database["raid_table"]
    )
    
    #get needed columns where the info stored
    df_to_send = df_for.loc[:,["raid_id","raid_name","raid_type"]]
    
    result = json.loads(df_to_send.to_json(orient="index"))
    return json.dumps(result, indent=2)