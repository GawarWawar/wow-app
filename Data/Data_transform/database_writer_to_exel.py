import numpy as np
import pandas as pd

csv = "CSV/Items_from_Anub'Rekhan_10.csv"
df = pd.read_csv(csv, engine='python', sep = ", ", index_col = False, header=None)
df = df.transpose()

excel = "../Items.xlsx"
df.to_excel(excel, index=False)  
print(df)