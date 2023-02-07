import numpy as np
import pandas as pd
import datetime

import time

def id_and_two_columns (
    main_df, #df to add a row
    dict_w_info={ #dictionary w/ content info, that we need to add ->
       0 : None,
       1 : None
    } #keys = 0,1,2; values = values we need to add
    
):
    """
    Add row w/ 3 columns, in which the 1st one is generated id \n
        \n
        return id
    """
    #we have place holder in each table, so we dont need to worry about 
        #nothing beeng in the table
        
    #we are using privious last id to generate id for the new row
    next_id = main_df.iloc[:,0].\
                iat[
                    len(main_df.index)-1
                ] + 1
    
    #adding row w/ info from our dict
    main_df.loc[
                len(
                    main_df.index
                )
            ] = [
                    next_id,
                    dict_w_info[0],
                    dict_w_info[1]
                ]
            
    return(next_id)

def three_columns (
    main_df, #df to add a row
    dict_w_info={ #dictionary w/ content info, that we need to add ->
       0 : None,
       1 : None,
       2 : None 
    } #keys = 0,1,2; values = values we need to add
): 
    """
    Add row w/ 3 columns \n
        \n
        return None
    """
    #adding row w/ info from our dict
    main_df.loc[
                len(
                    main_df.index
                )
            ] = [
                    dict_w_info[0],
                    dict_w_info[1], 
                    dict_w_info[2]
                ]
            
    return()

def two_columns_and_exact_time (
    main_df,
    dict_w_info ={
        0: None,
        1: None
    }
):
    """
    Add row w/ 3 columns, in which the last one is generated exact time\n
        \n
        return None
    """
    #getting system time for the exact moment
    exact_time = datetime.datetime.now()
    #adding new row to the talbe  
    three_columns(
        main_df,
        dict_w_info={
                #info about that object we need to write
                0: dict_w_info[0],
                1: dict_w_info[1],
                2: exact_time
            }
    )

def id_and_three_columns (
    main_df, #df to add a row
    dict_w_info={ #dictionary w/ content info, that we need to add ->
       0 : None,
       1 : None,
       2 : None 
    } #keys = 0,1,2; values = values we need to add
    
):
    """
    Add row w/ 4 columns, in which the 1st one is generated id \n
        \n
        return id
    """
    #we have place holder in each table, so we dont need to worry about 
        #nothing beeng in the table
        
    #we are using privious last id to generate id for the new row
    next_id = main_df.iloc[:,0].\
                iat[
                    len(main_df.index)-1
                ] + 1
    
    #adding row w/ info from our dict
    main_df.loc[
                len(
                    main_df.index
                )
            ] = [
                    next_id,
                    dict_w_info[0],
                    dict_w_info[1], 
                    dict_w_info[2]
                ]
            
    return(next_id)

def id_and_five_columns (
    main_df, #df to add a row
    dict_w_info={ #dictionary w/ content info, that we need to add ->
       0 : None,
       1 : None,
       2 : None,
       3 : None,
       4 : None 
    } #keys = 0,1,2; values = values we need to add
    
):
    """
    Add row w/ 6 columns, in which the 1st one is generated id \n
        \n
        return id
    """
    #we have place holder in each table, so we dont need to worry about 
        #nothing beeng in the table
        
    #we are using privious last id to generate id for the new row
    next_id = main_df.iloc[:,0].\
                iat[
                    len(main_df.index)-1
                ] + 1
    
    #adding row w/ info from our dict
    main_df.loc[
                len(
                    main_df.index
                )
            ] = [
                    next_id,
                    dict_w_info[0],
                    dict_w_info[1], 
                    dict_w_info[2],
                    dict_w_info[3], 
                    dict_w_info[4]
                ]
            
    return(next_id)

def id_four_columns_and_exact_time(
    main_df,
    dict_w_info={
            0: None,
            1: None,
            2: None,
            3: None,
    }
):
    """
    Add row w/ 6 columns, in which the 1st one is generated id \n
        and the last one is generated exact time\n
        \n
        return id
    """
    exact_time = datetime.datetime.now() #system time
    #create new row
    id = id_and_five_columns(
        main_df,
        dict_w_info={
            0: dict_w_info[0],
            1: dict_w_info[1],
            2: dict_w_info[2],
            3: dict_w_info[3],
            4: exact_time,
        }
    )
    return (id)
