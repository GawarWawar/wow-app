import numpy as np
import pandas as pd

import pyarrow.parquet as pq
import pyarrow as pa

import os

file_path_to_read = "Data/Dynamic_database"

for file in os.listdir(file_path_to_read):
    if os.path.isfile(os.path.join(file_path_to_read, file)):
        try:
            df = pd.read_csv(
                f'{file_path_to_read}/{file}'
            )
            go_further = True
        except UnicodeDecodeError:
            print(f'{file} is already .parquet')
            go_further = False
                        
        if go_further:
            df = df.fillna(np.nan).replace([np.nan], [None])
            
            change_to_int = [
                "run_id",
                "event_id",
                "boss_id",
                "item_id",
                "guild_id",
                "raid_id",
            ]
            
            columns_of_df = list(df.columns)
            for indx in columns_of_df:
                if indx in columns_of_df:
                    for column in range(len(change_to_int)):
                        if change_to_int[column] == indx:
                            df[change_to_int[column]] = \
                                df[change_to_int[column]].\
                                    astype("Int64")
                            print(f'{change_to_int[column]} is in Int')
            
            change_to_datetime = [
                "system_time",  
                "date_finished" 
            ]
            
            columns_of_df = list(df.columns)
            for indx in columns_of_df:
                if indx in change_to_datetime:
                    for column in range(len(change_to_datetime)):
                        if change_to_datetime[column] == indx:
                            df[change_to_datetime[column]] = \
                                pd.to_datetime(
                                    df[change_to_datetime[column]]
                                )
                            print(f'{change_to_datetime[column]} is in Datetime')
                            
            
            print(f'{file} is Done')
            
            f_dif_end = file.removesuffix(".csv")+".parquet"
            df.to_parquet(
                f'{file_path_to_read}/{f_dif_end}',
                engine="pyarrow",
                compression="gzip"
            )

