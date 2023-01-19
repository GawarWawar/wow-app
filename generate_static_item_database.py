import numpy as np
import pandas as pd
import time

from utils.useless_tools import from_many_csv_to_one_file_of_any_filetype
from utils.tools import from_many_csv_to_one_df, wowhead_style_csv_to_df
    
start_timer = time.perf_counter()
 
files_for_items_list = [
    "Data/Data_transform/Items_from_Naxx/Anub'Rekhan_10.csv",
    "Data/Data_transform/Items_from_Naxx/Anub'Rekhan_25.csv",
    "Data/Data_transform/Items_from_Naxx/Four_Horsemen_Chest_10.csv",
    "Data/Data_transform/Items_from_Naxx/Four_Horsemen_Chest_25.csv",
    "Data/Data_transform/Items_from_Naxx/Gothik_the_Harvester_10.csv",
    "Data/Data_transform/Items_from_Naxx/Gothik_the_Harvester_25.csv",
    "Data/Data_transform/Items_from_Naxx/Grand_Widow_Faerlina_10.csv",
    "Data/Data_transform/Items_from_Naxx/Grand_Widow_Faerlina_25.csv",
    "Data/Data_transform/Items_from_Naxx/Grobbulus_10.csv",
    "Data/Data_transform/Items_from_Naxx/Grobbulus_25.csv",
    "Data/Data_transform/Items_from_Naxx/Heigan_the_Unclean_10.csv",
    "Data/Data_transform/Items_from_Naxx/Heigan_the_Unclean_25.csv",
    "Data/Data_transform/Items_from_Naxx/Instructor_Razuvious_10.csv",
    "Data/Data_transform/Items_from_Naxx/Instructor_Razuvious_25.csv",
    "Data/Data_transform/Items_from_Naxx/Kel'Thuzad_10.csv",
    "Data/Data_transform/Items_from_Naxx/Kel'Thuzad_25.csv",
    "Data/Data_transform/Items_from_Naxx/Loatheb_10.csv",
    "Data/Data_transform/Items_from_Naxx/Loatheb_25.csv",
    "Data/Data_transform/Items_from_Naxx/Maexxna_10.csv",
    "Data/Data_transform/Items_from_Naxx/Maexxna_25.csv",
    "Data/Data_transform/Items_from_Naxx/Naxxramas_trash_10.csv",
    "Data/Data_transform/Items_from_Naxx/Noth_the_Plaguebringer_10.csv",
    "Data/Data_transform/Items_from_Naxx/Noth_the_Plaguebringer_25.csv",
    "Data/Data_transform/Items_from_Naxx/Patchwerk_10.csv",
    "Data/Data_transform/Items_from_Naxx/Patchwerk_25.csv",
    "Data/Data_transform/Items_from_Naxx/Sapphiron_10.csv",
    "Data/Data_transform/Items_from_Naxx/Sapphiron_25.csv",
    "Data/Data_transform/Items_from_Naxx/Thaddius_10.csv",
    "Data/Data_transform/Items_from_Naxx/Thaddius_25.csv"
]

wowhead_separator = ", "
indexes_that_we_want_to_set_up = [
        "item_id", 
        "item_name"
]

df_for_items = from_many_csv_to_one_df(
        files_to_read = files_for_items_list,
        set_index_names = indexes_that_we_want_to_set_up,
        csv_separator = wowhead_separator
)

df_for_items = df_for_items.drop_duplicates(indexes_that_we_want_to_set_up[0])
df_for_items = df_for_items.sort_values(indexes_that_we_want_to_set_up[0])
df_for_items.to_csv(
    "Data/Static_database/items.csv", 
    index_label=False, 
    header=True, 
    index=False
)


"""
#create exel file for items
df_for_items.to_csv(
    "Data/Static_database/items.xlsx", 
    index_label=False, 
    header=True, 
    index=False
)


#create json file for items
df_for_items.to_csv(
    "Data/Static_database/items.json", 
    index_label=False, 
    header=True, 
    index=False
)
"""


#creating file for the gluth_10
files_for_gluth_10 = [
    "Data/Data_transform/Items_from_Naxx/Anub'Rekhan_10.csv",
    "Data/Data_transform/Items_from_Naxx/Four_Horsemen_Chest_10.csv",
    "Data/Data_transform/Items_from_Naxx/Gothik_the_Harvester_10.csv",
    "Data/Data_transform/Items_from_Naxx/Grand_Widow_Faerlina_10.csv",
    "Data/Data_transform/Items_from_Naxx/Grobbulus_10.csv",
    "Data/Data_transform/Items_from_Naxx/Heigan_the_Unclean_10.csv",
    "Data/Data_transform/Items_from_Naxx/Instructor_Razuvious_10.csv",
    "Data/Data_transform/Items_from_Naxx/Loatheb_10.csv",
    "Data/Data_transform/Items_from_Naxx/Maexxna_10.csv",
    "Data/Data_transform/Items_from_Naxx/Patchwerk_10.csv",
    "Data/Data_transform/Items_from_Naxx/Noth_the_Plaguebringer_10.csv",
    "Data/Data_transform/Items_from_Naxx/Thaddius_10.csv"
]
df_for_gluth_10 = from_many_csv_to_one_df(
    files_to_read = files_for_gluth_10,
    set_index_names = indexes_that_we_want_to_set_up,
    csv_separator = wowhead_separator
)

df_for_gluth_10 = df_for_gluth_10.drop_duplicates(indexes_that_we_want_to_set_up[0])
df_for_gluth_10 = df_for_gluth_10.sort_values(indexes_that_we_want_to_set_up[0])
#transpoe df to make it the same orientation as other files
df_for_gluth_10 = df_for_gluth_10.transpose()

df_for_gluth_10.to_csv(
    "Data/Data_transform/Items_from_Naxx/Gluth_10_not_wowhead.csv", 
    index_label=False, 
    header=False, 
    index=False
)


#creating Gluth_25 file
files_for_gluth_25 = [
    "Data/Data_transform/Items_from_Naxx/Anub'Rekhan_25.csv",
    "Data/Data_transform/Items_from_Naxx/Four_Horsemen_Chest_25.csv",
    "Data/Data_transform/Items_from_Naxx/Gothik_the_Harvester_25.csv",
    "Data/Data_transform/Items_from_Naxx/Grand_Widow_Faerlina_25.csv",
    "Data/Data_transform/Items_from_Naxx/Grobbulus_25.csv",
    "Data/Data_transform/Items_from_Naxx/Heigan_the_Unclean_25.csv",
    "Data/Data_transform/Items_from_Naxx/Instructor_Razuvious_25.csv",
    "Data/Data_transform/Items_from_Naxx/Loatheb_25.csv",
    "Data/Data_transform/Items_from_Naxx/Maexxna_25.csv",
    "Data/Data_transform/Items_from_Naxx/Patchwerk_25.csv",
    "Data/Data_transform/Items_from_Naxx/Noth_the_Plaguebringer_25.csv",
    "Data/Data_transform/Items_from_Naxx/Thaddius_25.csv"
]

df_for_gluth_25 = from_many_csv_to_one_df(
    files_to_read = files_for_gluth_10,
    set_index_names = indexes_that_we_want_to_set_up,
    csv_separator = wowhead_separator
)

df_for_gluth_25 = df_for_gluth_25.drop_duplicates(indexes_that_we_want_to_set_up[0])
df_for_gluth_25 = df_for_gluth_25.sort_values(indexes_that_we_want_to_set_up[0])
#transpoe df to make it the same orientation as other file
df_for_gluth_25 = df_for_gluth_25.transpose()

df_for_gluth_25.to_csv(
    "Data/Data_transform/Items_from_Naxx/Gluth_25_not_wowhead.csv", 
    index_label=False, 
    header=False, 
    index=False
)


# Building table for loot that drops from bosses
bosses_list = pd.read_csv(
    "Data/Static_database/Wow app - Bosses table.csv"
)
bosses_list = bosses_list.sort_values("boss_name")
#temporary droping lists, that doesnt have files
bosses_list = bosses_list.drop([16])
#droping not wowhead files
bosses_list = bosses_list.drop([3, 19])

#creating table for items, that can drop from certain bosses
file_for_drops_from_bosses = files_for_items_list
drop_dict = {
    "boss_id" : [],
    "item_id" : []
}

j = 0
for i in file_for_drops_from_bosses:
    boss_df = pd.DataFrame()
    boss_dict = {}
    
    boss_df = wowhead_style_csv_to_df(
        i,
        boss_df,
        indexes_that_we_want_to_set_up,
        wowhead_separator
    )

    boss_id = bosses_list.iat[j,0]
    
    #creat DataFrame w/ drop for certain boss
    boss_df["boss_id"] = boss_id
    boss_df.pop("item_name")
    
    boss_dict = boss_df.to_dict(orient="list")
    drop_dict["boss_id"].extend(boss_dict["boss_id"])
    drop_dict["item_id"].extend(boss_dict["item_id"])
    
    j += 1

drop_df = pd.DataFrame.from_dict(drop_dict)    
drop_df.to_csv("Data/Static_database/drop_of_bosses.csv",index=False,index_label=False)


end_timer = time.perf_counter()
print(
    "generate_static_item_database time =",
    end_timer-start_timer
)