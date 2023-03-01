import numpy as np
import pandas as pd

import pyarrow.parquet as pq
import pyarrow as pa

import os

def csv_to_parquet(
    log_on=False
):
    file_path_to_read = "Data/csv_data/dynamic_database_csv"
    file_path_to_write = "Data/Dynamic_database"

    for file in os.listdir(file_path_to_read):
        if os.path.isfile(os.path.join(file_path_to_read, file)):
            try:
                df = pd.read_csv(
                    f'{file_path_to_read}/{file}'
                )
                go_further = True
            except UnicodeDecodeError:
                if log_on:
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
                                if log_on:
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
                                if log_on:
                                    print(f'{change_to_datetime[column]} is in Datetime')


                if log_on:
                    print(f'{file} is Done')

                f_dif_end = file.removesuffix(".csv")+".parquet"
                df.to_parquet(
                    f'{file_path_to_write}/{f_dif_end}',
                    engine="pyarrow",
                    compression="gzip"
                )

def parquet_to_csv(
    log_on=False
):
    file_path_to_read = "Data/Dynamic_database"
    file_path_to_write = "Data/csv_data/dynamic_database_csv"

    for file in os.listdir(file_path_to_read):
        if os.path.isfile(os.path.join(file_path_to_read, file)):
            try:
                df = pd.read_parquet(
                    f'{file_path_to_read}/{file}'
                )
                go_further = True
            except pa.lib.ArrowInvalid:
                if log_on:
                    print(f'{file} is already .csv')
                go_further = False

        if go_further:
            if log_on:
                    print(f'{file} is Done')

            f_dif_end = file.removesuffix(".parquet")+".csv"
            df.to_csv(
                f'{file_path_to_write}/{f_dif_end}',
                index=False,
                index_label=False
            )