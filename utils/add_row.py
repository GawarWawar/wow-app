import numpy as np
import pandas as pd
import time


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
        and return id
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
        and return None
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
    Add row w/ 4 columns, in which the 1st one is generated id \n
        and return id
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

