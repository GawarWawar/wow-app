import numpy as np
import pandas as pd
import time

start_timer = time.perf_counter()

#transform from csv into DataFrame with forward transposing it`s content
def csv_with_no_header_to_transposed_dataframe (
    csv, #file to read from
    dataframe, #dataframe to write into
    set_names_for_transposed_indexes=False, #names for the indexes (optional)
    separetor = False, #separator into csv file (optional)
):
    if separetor != False: 
        dataframe = pd.read_csv(csv, engine='python', sep = separetor, header=None)
    else:
        dataframe = pd.read_csv(csv, header=None)
    if set_names_for_transposed_indexes != False :
        dataframe = dataframe.set_index(set_names_for_transposed_indexes) 
    dataframe = dataframe.transpose()
    return dataframe

#get data from the different files and write into 1
def from_many_csv_to_one_file_of_any_filetype (
    files_to_read, #list of files to read from 
    file_to_write, #file to write into
    ftw_type,      #type of file to write into, can support: json, csv or exel (xlsx) 
    set_index_names, #names for columns/indexes for ur dataframe
    csv_separator=False, #separator for csv files (oprional)
    should_be_df_transposed = True, #should dataframe be transposed, boolean, True by default (optional)
):
    #dataframe to combine all of the file content in
    main_df = pd.DataFrame(columns=set_index_names)
    
    #cycle to get every csv-file into our main DataFrame
    for i in files_to_read: 
        #dataframe for each step of the cycle
        df_situational = pd.DataFrame()
        #reading next file our situational dataframe (df_situational) and transposing it
        df_situational = csv_with_no_header_to_transposed_dataframe(
            csv = i,
            dataframe = df_situational, 
            set_names_for_transposed_indexes=[set_index_names], 
            separetor=csv_separator
        )
        #writing transposed situational dataframe (df_situational) into our main storage container
        main_df = pd.concat([main_df,df_situational], ignore_index=True)
     
    
    #deliting dublicates and sorting by the first element of set_index_names
    main_df = main_df.drop_duplicates(set_index_names[0])
    main_df = main_df.sort_values(set_index_names[0], ignore_index=True)
    
    if should_be_df_transposed != True:
        main_df = main_df.transpose()

    #writing into specified file_type file
    if ftw_type == "csv":
        main_df.to_csv(file_to_write, index_label=False, header=True, index=False)
    elif ftw_type == "json":
        main_df.to_json(file_to_write, orient="index", indent=2)
    elif ftw_type == "exel":
        main_df.to_excel(file_to_write, index=False) 
    else: 
        print("No such file type is supported")
    
end_timer = time.perf_counter()
print(-start_timer+end_timer)