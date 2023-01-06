import numpy as np
import pandas as pd
import time

start_timer = time.perf_counter()

def csv_with_no_header_to_transposed_dataframe (csv, dataframe, set_names_for_transposed_indexes=False, separetor = False):
    #transform from csv into DataFrame with forward transposing it`s content
    if separetor != False: 
        dataframe = pd.read_csv(csv, engine='python', sep = separetor, header=None)
    else:
        dataframe = pd.read_csv(csv, header=None)
    if set_names_for_transposed_indexes != False :
        dataframe = dataframe.set_index(set_names_for_transposed_indexes) 
    dataframe = dataframe.transpose()
    return dataframe

def from_many_csv_to_one_fiel_of_any_filetype (
    files_to_read, #list of files to read from 
    file_to_write, #file to write into
    ftw_type,      #type of file to write into, can support: json, csv or exel (xlsx) 
    set_index_names, #names for columns/indexes for ur dataframe
    csv_separator=False #separator for csv files (oprional)
):
    main_df = pd.DataFrame(columns=set_index_names)
    #dataframe to combine all of the file content in
    
    for i in files_to_read:
        #cycle to get every csv-file into our main DataFrame 
        df_situational = pd.DataFrame()
        #dataframe for each step of the cycle
        df_situational = csv_with_no_header_to_transposed_dataframe(
            csv = i,
            dataframe = df_situational, 
            set_names_for_transposed_indexes=[set_index_names], 
            separetor=csv_separator
        )
        #reading next file our situational dataframe (df_situational) and transposing it
        main_df = pd.concat([main_df,df_situational], ignore_index=True)
        #writing transposed situational dataframe (df_situational) into our main storage container
    
    main_df = main_df.drop_duplicates(set_index_names[0])
    main_df = main_df.sort_values(set_index_names[0], ignore_index=True)
    #deliting dublocates and sorting by the first (0) element of set_index_names
    
    #writing into specified file_type file
    if ftw_type == "csv":
        main_df.to_csv(file_to_write, index_label=False, header=True, index=False)
    elif ftw_type == "json":
        main_df.to_json(file_to_write, orient="index")
    elif ftw_type == "exel":
        main_df.to_excel(file_to_write, index=False) 
    else: 
        print("No such file type is supported")
    



files = [
    "Data/Data_transform/CSV/Items/Anub'Rekhan_10.csv",
    "Data/Data_transform/CSV/Items/Anub'Rekhan_25.csv",
    "Data/Data_transform/CSV/Items/Four_Horsemen_Chest_10.csv",
    "Data/Data_transform/CSV/Items/Four_Horsemen_Chest_25.csv",
    "Data/Data_transform/CSV/Items/Gothik_the_Harvester_10.csv",
    "Data/Data_transform/CSV/Items/Gothik_the_Harvester_25.csv",
    "Data/Data_transform/CSV/Items/Grand_Widow_Faerlina_10.csv",
    "Data/Data_transform/CSV/Items/Grand_Widow_Faerlina_25.csv",
    "Data/Data_transform/CSV/Items/Grobbulus_10.csv",
    "Data/Data_transform/CSV/Items/Grobbulus_25.csv",
    "Data/Data_transform/CSV/Items/Heigan_the_Unclean_10.csv",
    "Data/Data_transform/CSV/Items/Heigan_the_Unclean_25.csv",
    "Data/Data_transform/CSV/Items/Instructor_Razuvious_10.csv",
    "Data/Data_transform/CSV/Items/Instructor_Razuvious_25.csv",
    "Data/Data_transform/CSV/Items/Kel'Thuzad_10.csv",
    "Data/Data_transform/CSV/Items/Kel'Thuzad_25.csv",
    "Data/Data_transform/CSV/Items/Loatheb_10.csv",
    "Data/Data_transform/CSV/Items/Loatheb_25.csv",
    "Data/Data_transform/CSV/Items/Maexxna_10.csv",
    "Data/Data_transform/CSV/Items/Maexxna_25.csv",
    "Data/Data_transform/CSV/Items/Naxxramas_trash_10.csv",
    "Data/Data_transform/CSV/Items/Noth_the_Plaguebringer_10.csv",
    "Data/Data_transform/CSV/Items/Noth_the_Plaguebringer_25.csv",
    "Data/Data_transform/CSV/Items/Patchwerk_10.csv",
    "Data/Data_transform/CSV/Items/Patchwerk_25.csv",
    "Data/Data_transform/CSV/Items/Sapphiron_10.csv",
    "Data/Data_transform/CSV/Items/Sapphiron_25.csv",
    "Data/Data_transform/CSV/Items/Thaddius_10.csv",
    "Data/Data_transform/CSV/Items/Thaddius_25.csv"
]
#all files that we are adding to our list but relative pass to main folder
"""
files = [
    "CSV/Items/Anub'Rekhan_10.csv",
    "CSV/Items/Anub'Rekhan_25.csv",
    "CSV/Items/Anub'Rekhan_10.csv",
    "CSV/Items/Anub'Rekhan_25.csv",
    "CSV/Items/Four_Horsemen_Chest_10.csv",
    "CSV/Items/Four_Horsemen_Chest_25.csv",
    "CSV/Items/Gothik_the_Harvester_10.csv",
    "CSV/Items/Gothik_the_Harvester_25.csv",
    "CSV/Items/Grand_Widow_Faerlina_10.csv",
    "CSV/Items/Grand_Widow_Faerlina_25.csv",
    "CSV/Items/Grobbulus_10.csv",
    "CSV/Items/Grobbulus_25.csv",
    "CSV/Items/Heigan_the_Unclean_10.csv",
    "CSV/Items/Heigan_the_Unclean_25.csv",
    "CSV/Items/Instructor_Razuvious_10.csv",
    "CSV/Items/Instructor_Razuvious_25.csv",
    "CSV/Items/Kel'Thuzad_10.csv",
    "CSV/Items/Kel'Thuzad_25.csv",
    "CSV/Items/Loatheb_10.csv",
    "CSV/Items/Loatheb_25.csv",
    "CSV/Items/Maexxna_10.csv",
    "CSV/Items/Maexxna_25.csv",
    "CSV/Items/Naxxramas_trash_10.csv",
    "CSV/Items/Noth_the_Plaguebringer_10.csv",
    "CSV/Items/Noth_the_Plaguebringer_25.csv",
    "CSV/Items/Patchwerk_10.csv",
    "CSV/Items/Patchwerk_25.csv",
    "CSV/Items/Sapphiron_10.csv",
    "CSV/Items/Sapphiron_25.csv",
    "CSV/Items/Thaddius_10.csv",
    "CSV/Items/Thaddius_25.csv"
    ]
"""  
    #all files that we are adding to our list

wowhead_separator = ", "

from_many_csv_to_one_fiel_of_any_filetype(
    files_to_read=files,
    file_to_write="Data/Items.csv",
    ftw_type = "csv",
    set_index_names=["Item_id", "Item_Name"],
    csv_separator = wowhead_separator
)
from_many_csv_to_one_fiel_of_any_filetype(
    files_to_read=files,
    file_to_write="Data/Items.json",
    ftw_type = "json",
    set_index_names=["Item_id", "Item_Name"],
    csv_separator = wowhead_separator
)

from_many_csv_to_one_fiel_of_any_filetype(
    files_to_read=files,
    file_to_write="Data/Items.xlsx",
    ftw_type = "exel",
    set_index_names=["Item_id", "Item_Name"],
    csv_separator = wowhead_separator
)

end_timer = time.perf_counter()
print(-start_timer+end_timer)