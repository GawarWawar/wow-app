import numpy as np
import pandas as pd
dickt = {
    'row1': [1994,1995,1996,1997],
    'row2': [2002,2003,2004,2005],
    'row3': [2012,2014,2015,2017]
}
db = pd.DataFrame.from_dict(dickt)
#print(db)
#print(db.index)
#print(db.columns)
print(pd.cut(np.array([2, 7, 5, 4, 6, 3]), 2))