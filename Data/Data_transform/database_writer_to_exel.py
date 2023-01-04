import numpy as np
import pandas as pd

def csv_to_dataframe (csv, dataframe):
    dataframe = pd.read_csv(csv, engine='python', sep = ", ", index_col = False, header=None)
    dataframe = dataframe.transpose()
    return dataframe

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
main_df = pd.DataFrame()

for i in files:
    df_situational = pd.DataFrame()
    df_situational = csv_to_dataframe (i, df_situational)
    main_df = pd.concat([main_df,df_situational])

excel = "../Items.xlsx"
main_df.to_excel(excel, index=False)  
print(main_df)