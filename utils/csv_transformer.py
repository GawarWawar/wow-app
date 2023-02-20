import numpy as np
import pandas as pd

import pyarrow.parquet as pq
import pyarrow as pa

import os

file_path_to_read = "Data/Dynamic_database"

for f in os.listdir(file_path_to_read):
    if os.path.isfile(os.path.join(file_path_to_read, f)):
        try:
            if f != "runs_of_the_guilds_table.csv":
                df = pd.read_csv(
                    f'{file_path_to_read}/{f}'
                )
            else:
                df = pd.read_csv(
                    f'{file_path_to_read}/{f}',
                    dtype={
                        "run_id": np.int64,
                        "guild_id": np.int64,
                        "raid_id": np.int64,
                        "date_finished": object
                    }

                )
            f_dif_end = f.removesuffix(".csv")+".parquet"
            df.to_parquet(
                f'{file_path_to_read}/{f_dif_end}',
                engine="pyarrow"
            )
        except:
            print(f'{f} is already .parquet')            

