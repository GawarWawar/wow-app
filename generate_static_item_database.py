import numpy as np
import pandas as pd
import time

from utils.useless_tools import from_many_csv_to_one_file_of_any_filetype
from utils.tools import from_many_csv_to_one_df
 
start_timer = time.perf_counter()
    
#all files that we are adding to our list 
files = [
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
indexes_that_we_want_to_set_up = ["item_id", "item_name"]

from_many_csv_to_one_file_of_any_filetype(
    files_to_read=files,
    file_to_write="Data/Static_database/Items.csv",
    ftw_type = "csv",
    set_index_names=indexes_that_we_want_to_set_up,
    csv_separator = wowhead_separator
)
"""
from_many_csv_to_one_file_of_any_filetype(
    files_to_read=files,
    file_to_write="Data/Static_database/Items.json",
    ftw_type = "json",
    set_index_names=indexes_that_we_want_to_set_up,
    csv_separator = wowhead_separator
)

from_many_csv_to_one_file_of_any_filetype(
    files_to_read=files,
    file_to_write="Data/Items_from_Naxx.xlsx",
    ftw_type = "exel",
    set_index_names=indexes_that_we_want_to_set_up,
    csv_separator = wowhead_separator
)
"""

#creating Gluth_10 file
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
from_many_csv_to_one_file_of_any_filetype(
    files_to_read = files_for_gluth_10,
    file_to_write = "Data/Data_transform/Items_from_Naxx/Gluth_10_not_wowhead.csv",
    ftw_type = "csv",
    set_index_names=indexes_that_we_want_to_set_up,
    csv_separator=wowhead_separator,
    should_be_df_transposed=False  
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
from_many_csv_to_one_file_of_any_filetype(
    files_to_read = files_for_gluth_25,
    file_to_write = "Data/Data_transform/Items_from_Naxx/Gluth_25_not_wowhead.csv",
    ftw_type = "csv",
    set_index_names=indexes_that_we_want_to_set_up,
    csv_separator=wowhead_separator,
    should_be_df_transposed=False  
)

end_timer = time.perf_counter()
print("generate_static_item_database time =", end_timer-start_timer)