import numpy as np
import pandas as pd
import time

import sys
from os.path import dirname, abspath

SCRIPT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(SCRIPT_DIR))

import utils.simple_utils.simple_tools as u_tools

#change separetor from ", " to ","
def rewrite_wowhead_separator(
    file_to_rewrite, #file which separator we want to change
    path_to_ftw, #path to file to write
    new_path, #path to new file
    sep_style = ", ", #by default common sep from wowhead
    rename_pattern = "_not_wowhead" #what to add to file, "_not_wowhead" for default
):
    df_to_rewrite = pd.read_csv(
        path_to_ftw + "/"+ file_to_rewrite, #combinepath + filename 
        engine='python', 
        sep = sep_style, 
        header=None
    )
    split_file_name = file_to_rewrite.split(".")
    new_path = f"{new_path}/{split_file_name[0]}{rename_pattern}.{split_file_name[1]}"
    df_to_rewrite.to_csv(
        new_path,
        index=False,
        index_label=False,
        header=None     
    )

#transform from csv into DataFrame with forward transposing it`s content
#old name: wowhead_inspired_csv_to_df
def vertical_csv_to_df (
    file_to_read, #file to read from
    path_to_ftr, #path to file to read
    dataframe, #dataframe to write into
    set_indexes_names, #names for the indexes (optional)
):
    dataframe = pd.read_csv(
        path_to_ftr +"/"+file_to_read,  
        header=None
    )
    dataframe = dataframe.set_index([set_indexes_names]) 
    dataframe = dataframe.transpose()
    return dataframe


#get data from the different files and write into 1
def from_many_csv_to_one_df (
        files_to_read, #list of files to read from
        path_to_fstr, #path to file to read
        set_index_names, #names for columns/indexes for ur dataframe
    ):
    #dataframe to combine all of the file content in
    main_df = pd.DataFrame(columns=set_index_names)
    
    #cycle to get every csv-file into our main DataFrame
    for i in files_to_read: 
        df_situational = pd.DataFrame()
        df_situational = vertical_csv_to_df(
            i,
            path_to_fstr,
            df_situational,
            set_index_names
        )
        main_df = pd.concat([main_df,df_situational], ignore_index=True)
        
    return (main_df)


#read many csv to create one csv
#has drop duplicantes and sort_value on colomn n0
#write options: index_label=False, header=False, index=False
def from_many_csv_to_one_csv(
    files_to_read, #list of files to read from
    path_to_fstr, #path to file to read
    file_to_write, #file to write
    path_to_ftw, #path to write file
    set_index_names, #names for columns/indexes for ur dataframe
    transpose_grouped_file=True, #check if new file should be transposed
    options_for_tocsv = {   #options for pd.csv
        "index_label":False,
        "header":False,
        "index":False
    }
):
    main_df = from_many_csv_to_one_df(
        files_to_read=files_to_read,
        path_to_fstr=path_to_fstr,
        set_index_names=set_index_names
    )

    main_df = main_df.drop_duplicates(
        set_index_names[0]
    )
    main_df = main_df.sort_values(
        set_index_names[0]
    )
    
    #transpoe df to make it the same orientation as antecedence files
    if transpose_grouped_file:
        main_df = main_df.transpose()

    main_df.to_csv(
        path_to_ftw+"/"+file_to_write, 
        index_label=options_for_tocsv["index_label"], 
        header=options_for_tocsv["header"], 
        index=options_for_tocsv["index"]
    )


#This is slower, but let it be
def find_item_in_DataFrame_without_for (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    column_name #name of column to look into for item 
    ):
    """
        Finds entety that we are looking for in given DataFrame
    """
    #looking for the item
    item = main_df[main_df.loc[:, column_name] == object_to_search_for]  
    return(item)

#outdated, due to existence of pd.DataFrame.merge()
#still leave it here if they will be needed


def find_many_rows_in_DataFrame_with_for__concat (
    main_df, #DataFrame that contain our object 
    object_to_search_for, #what we need to find
    item_column #name of column to look into for item
    ):
    """
        Finds all enteties that we are looking for in given DataFrame
    """
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
    
    return(df_to_return)


#searches for the position of the needed item in the given list
def next_in_series (
    item_to_compair,
    series_for_search,
    position_to_start
):
    for search in range(
        position_to_start,
        len(series_for_search-1)
    ):
        if series_for_search.iat[search] >= item_to_compair:
            return search

#find many rows that contain searched object in 1 column
def find_rows_in_DataFrame (
        main_df, #DataFrame that contain our object 
        object_to_search_for, #what we need to find
        item_column #name of column to look into for item
):
    """
        Finds all enteties that we are looking for in given DataFrame
    """
    dict_to_work = {}
    
    #loop to find all lines and add them to the 1 dictionary 
    #after that we can create df from it
    j = 0
    for i in main_df.loc[:,item_column]:
        if i == object_to_search_for:
            dict_to_work[len(dict_to_work)] = pd.Series(main_df.iloc[j]).T.to_dict()
        j = j+1

    df_to_return = pd.DataFrame.from_dict(dict_to_work, orient="index")
    return(df_to_return)

#find many rows for each object we are looking for in the column
#based on in_pandas finder and pd.DataFrame.to_dict
def many_to_many_finder (
        main_df, #DataFrame that contain our object 
        series_to_search_for, #list of what we need to find
        item_column #name of column to look into for item
    ):
    t_start = time.perf_counter()
    
    #create main dict to extend after finding elements for each criteria
    dict_to_work = pd.DataFrame(columns=main_df.columns)
    dict_to_work = dict_to_work.to_dict(orient="list")
    
    #loop to find all lines for all criterias
    for i in series_to_search_for:
        dict_to_extend = main_df[main_df.loc[:, item_column] == i]\
            .to_dict(orient="list")
        #extend every element of the main dict for the found criteria
        for j in dict_to_work:
            dict_to_work[j].extend(dict_to_extend[j])
    
    df_to_return = pd.DataFrame.from_dict(dict_to_work)
    
    t_end = time.perf_counter()
    print(many_to_many_finder.__name__,"time =",t_end-t_start)
    
    return(df_to_return)

#find many rows for each object we are looking for in the column
def many_to_many_finder_based_myltiple_for (
        main_df, #DataFrame that contain our object 
        series_to_search_for, #list of what we need to find
        item_column #name of column to look into for item
):
    """
    Find items for the list for given criterias
    Befor searching for the items sorts "item_colum" and "series_to_search_for" 
    """
    t_start = time.perf_counter()

    dict_to_work = {}
    
    #sorting list_to_sear_for and item column to make less searches
    main_df = main_df.sort_values(item_column)
    series_to_search_for = series_to_search_for.sort_values()
    
    #loop to find all lines and add them to 1 dictionary 
    df_lvl_counter = 0
    series_counter = 0
    
    for i in main_df.loc[:,item_column]:
        if i == series_to_search_for.iat[series_counter]:
            dict_to_work[len(dict_to_work)] = pd.Series(
                main_df.iloc[df_lvl_counter]).T.to_dict()
        
        #check if the search item still in the range of search 
        elif series_to_search_for.iat[series_counter] < i:
            #look for the next criteria to compair
            series_counter = next_in_series(
                i,
                series_to_search_for,
                series_counter
            )
            #if there is no more items to search for -> break
            if series_counter == None:
                break
            #check the same item after changing criteria
            elif i == series_to_search_for[series_counter]:
                dict_to_work[len(dict_to_work)] = pd.Series(
                    main_df.iloc[df_lvl_counter]).T.to_dict()
        df_lvl_counter += 1

    df_to_return = pd.DataFrame.from_dict(dict_to_work, orient="index")
    
    t_end = time.perf_counter()
    print(many_to_many_finder.__name__,"time =",t_end-t_start)
    
    return(df_to_return)

#find many rows for each object we are looking for in the column
def many_to_many_based_on_pandas_search_with_concat (
        main_df, #DataFrame that contain our object 
        series_to_search_for, #list of what we need to find
        item_column #name of column to look into for item
    ):
    t_start = time.perf_counter()
    
    df_to_return = pd.DataFrame()
    #loop to find all lines for all criterias
    for i in series_to_search_for:
        df_to_concat = main_df[main_df.loc[:, item_column] == i]
        #add them through concat
        df_to_return = pd.concat([df_to_return,df_to_concat])    
    
    t_end = time.perf_counter()
    print(function.__name__,"time =",t_end-t_start)
    
    return(df_to_return)



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
        df_situational = u_tools.vertical_csv_to_df(
            i,
            path_to_ftr= "",
            dataframe=df_situational,
            set_indexes_names=set_index_names
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


#useless reads
def read_columns_of_the_csv_to_DF (
        file_to_read, #file that we need to read
        columns = None #what columns do we need to read
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
    
def three_lvl_dict_check(dict_to_check):
    for lvl1 in dict_to_check:
            if dict_to_check[lvl1].__class__.__name__ == "list":
                for lvl1_elem in dict_to_check[lvl1]:
                    for lvl2 in lvl1_elem:
                        if lvl1_elem[lvl2].__class__.__name__=="list":
                            for lvl2_elem in lvl1_elem[lvl2]:
                                for lvl3 in lvl2_elem:
                                    print(
                                        lvl3, lvl2_elem[lvl3],
                                        f"{lvl3}.type", lvl2_elem[lvl3].__class__
                                    )
                        else:
                            print(
                                lvl2, lvl1_elem[lvl2],
                                f"{lvl2}.type", lvl1_elem[lvl2].__class__
                            )      
            else:
                print(
                    lvl1,dict_to_check[lvl1],
                    f"{lvl1}.type", dict_to_check[lvl1].__class__
                )

#need to be checked
def infinite_lvl_dict_check (dict_to_check):
    for lvl1 in dict_to_check:
        if dict_to_check[lvl1].__class__.__name__ == "list":
            for lvl1_elem in dict_to_check[lvl1]:
                infinite_lvl_dict_check(lvl1_elem)
        else:
                print(
                    lvl1,dict_to_check[lvl1],
                    f"{lvl1}.type", dict_to_check[lvl1].__class__
                )
                
