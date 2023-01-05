import numpy as np
import pandas as pd

def csv_to_transposed_dataframe (csv, dataframe, set_index_names=False):
    #transform from csv into column-based DataFrame
    dataframe = pd.read_csv(csv, engine='python', sep = ", ", header=None)
    if set_index_names != False :
        dataframe = dataframe.set_index(set_index_names) 
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
    #all files that we are adding to our list
main_df = pd.DataFrame(columns=["Item_id", "Item_Name"])
    #our main DataFrame, that will be witten 
for i in files:
    #cycle to get every csv-file into our main DataFrame 
    df_situational = pd.DataFrame()
    df_situational = csv_to_transposed_dataframe(i, df_situational, set_index_names=[["Item_id", "Item_Name"]])
    main_df = pd.concat([main_df,df_situational], ignore_index=True)
    #exit()

main_df = main_df.sort_values("Item_id", ignore_index=True)
lenght = main_df.loc[:, 'Item_id'].size
#print (lenght.size)
#print (main_df.loc[:,"Item_id"].size)
print(main_df.head(4))
i = 0
while i <= lenght-1:
    comparison_capsule_1 = main_df.iat[i,0]
    comparison_capsule_2 = main_df.iat[i+1,0]
    if comparison_capsule_1 == comparison_capsule_2:
        print (comparison_capsule_2)
        #main_df.pop(i+1)
    i = +500

#main_df.to_excel("../Items.xlsx", index=False) 
main_df
print(main_df.head(4))