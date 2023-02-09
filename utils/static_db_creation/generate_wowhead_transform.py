import numpy as np
import pandas as pd
import time

from os import listdir
from os.path import isfile, join, dirname, abspath
#
#import sys
#
#SCRIPT_DIR = dirname(abspath(__file__))
#sys.path.append(dirname(SCRIPT_DIR))

import db_creation_utils.db_creation_tools as db_tools

start_timer = time.perf_counter()

file_path_to_ftw = "data/wowhead_data/items_from_Naxx"
wowhead_separator = ", "
file_path_to_ri = "data/data_for_staic_db/items_from_naxx"

files_to_rewrite = [f for f in listdir(file_path_to_ftw) 
                    if isfile(join(file_path_to_ftw, f))]

for each_file in files_to_rewrite:
    db_tools.rewrite_wowhead_separator(
        each_file,
        file_path_to_ftw,
        file_path_to_ri,
    )

indexes_that_we_want_to_set_up =["0","1"]

#creating file for the gluth_10   
files_for_gluth_10 = [
    "Anub'Rekhan_10_not_wowhead.csv",
    "Gothik_the_Harvester_10_not_wowhead.csv",
    "Grand_Widow_Faerlina_10_not_wowhead.csv",
    "Grobbulus_10_not_wowhead.csv",
    "Heigan_the_Unclean_10_not_wowhead.csv",
    "Instructor_Razuvious_10_not_wowhead.csv",
    "Loatheb_10_not_wowhead.csv",
    "Maexxna_10_not_wowhead.csv",
    "Patchwerk_10_not_wowhead.csv",
    "Noth_the_Plaguebringer_10_not_wowhead.csv",
    "Thaddius_10_not_wowhead.csv",
    "The_Four_Horsemen_10_not_wowhead.csv"
]

db_tools.from_many_csv_to_one_csv(
    files_to_read=files_for_gluth_10,
    path_to_fstr=file_path_to_ri,
    file_to_write="Gluth_10_not_wowhead.csv",
    path_to_ftw=file_path_to_ri,
    set_index_names=indexes_that_we_want_to_set_up
)

#creating Gluth_25 file
files_for_gluth_25 = [
    "Anub'Rekhan_25_not_wowhead.csv",
    "Gothik_the_Harvester_25_not_wowhead.csv",
    "Grand_Widow_Faerlina_25_not_wowhead.csv",
    "Grobbulus_25_not_wowhead.csv",
    "Heigan_the_Unclean_25_not_wowhead.csv",
    "Instructor_Razuvious_25_not_wowhead.csv",
    "Loatheb_25_not_wowhead.csv",
    "Maexxna_25_not_wowhead.csv",
    "Patchwerk_25_not_wowhead.csv",
    "Noth_the_Plaguebringer_25_not_wowhead.csv",
    "Thaddius_25_not_wowhead.csv",
    "The_Four_Horsemen_25_not_wowhead.csv"

]

db_tools.from_many_csv_to_one_csv(
    files_to_read=files_for_gluth_10,
    path_to_fstr=file_path_to_ri,
    file_to_write="Gluth_25_not_wowhead.csv",
    path_to_ftw=file_path_to_ri,
    set_index_names=indexes_that_we_want_to_set_up
)

end_timer = time.perf_counter()
print(
    "generate_wowhead_transform time =",
    end_timer-start_timer
)