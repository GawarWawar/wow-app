import numpy as np
import pandas as pd
import time

#This is slower, but let it be
def find_item_in_DataFrame_without_for (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    column_name #name of column to look into for item 
    ):
    """
        Finds entety that we are looking for in given DataFrame
    """
    #start timer
    start_timer = time.perf_counter()
    #looking for the item
    item = main_df[main_df.loc[:, column_name] == object_to_search_for]  
    #end_timer
    end_timer = time.perf_counter()
    print("find_item_in_DataFrame_without_for timer =", end_timer-start_timer)
    return(item)

def find_many_rows_in_DataFrame_with_for__concat (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    item_column #name of column to look into for item
    ):
    """
        Finds all enteties that we are looking for in given DataFrame
    """
    #start timer
    start_timer = time.perf_counter()
    #declare a variable
    df_to_return = pd.DataFrame(columns=main_df.columns)
    #looking for the item
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            #df_to_return=main_df.iloc[j]
            #df_to_return = df_to_return.transpose()
            s = pd.Series(main_df.iloc[j])
            df_to_return = pd.concat([df_to_return, s.to_frame().T], ignore_index=True) 
        j = j+1
    #end_timer
    end_timer = time.perf_counter()
    print(find_many_rows_in_DataFrame_with_for__concat.__name__, " timer =", end_timer-start_timer)
    
    return(df_to_return)


#transform from csv into DataFrame with forward transposing it`s content
def csv_with_no_header_to_transposed_dataframe (
    csv, #file to read from
    dataframe, #dataframe to write into
    set_names_for_transposed_indexes=False, #names for the indexes (optional)
    separetor = False, #separator into csv file (optional)
):
    #startin timer
    start_timer = time.perf_counter()
    if separetor != False: 
        dataframe = pd.read_csv(csv, engine='python', sep = separetor, header=None)
    else:
        dataframe = pd.read_csv(csv, header=None)
    if set_names_for_transposed_indexes != False :
        dataframe = dataframe.set_index(set_names_for_transposed_indexes) 
    dataframe = dataframe.transpose()
    #ending timer
    end_timer = time.perf_counter()
    print(csv_with_no_header_to_transposed_dataframe.__name__,"time =", end_timer-start_timer)
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
    #startin timer
    start_timer = time.perf_counter()
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
    #ending timer
    end_timer = time.perf_counter()
    print(from_many_csv_to_one_file_of_any_filetype.__name__,"time =", end_timer-start_timer)

#useless reads
def read_columns_of_the_csv_to_DF (
        file_to_read, #file that we need to read
        columns = False #what columns do we need to read
):
    """
        Read file with the header and standart separator (,); \
        Return DataFrame with contamination of the columns we gave
    """
    
    df = pd.read_csv(file_to_read, header = 0, usecols=columns)

    return(df)


def read_the_file_to_DF (
    file_to_read, #file that we need to read
    file_type = "csv" #what type is our file, that we are reading
):
    """
        read file with the header and standart separator (,); \n
        return DataFrame with contamination of the file
    """

    if file_type == "csv":
        df = pd.read_csv(file_to_read)
    elif file_type == "json":
        df = pd.read_json(file_to_read, orient="index")
    else:
        return(print ("Error, we dont suppot such file extention"))

    return(df)
    