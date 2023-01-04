import numpy as np
import pandas as pd

def csv_to_dataframe (csv, dataframe):
    dataframe = pd.read_csv(csv, engine='python', sep = ", ", index_col = False, header=None)
    dataframe = dataframe.transpose()
    return dataframe

files = ["CSV/Items/Anub'Rekhan_10.csv"]
main_df = pd.DataFrame()
i = 0

for i in files:
    df_situational = pd.DataFrame()
    df_situational = csv_to_dataframe (i, df_situational)
    main_df = pd.concat([main_df,df_situational])

excel = "../Items.xlsx"
main_df.to_excel(excel, index=False)  
print(main_df)