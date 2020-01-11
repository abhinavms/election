import pandas as pd
import numpy as np

file_loc = "/mnt/f/Projects/Election/ElectionApp/.data/S5.xlsx"
df = pd.read_excel(file_loc, 
                   index_col=None, 
                   na_values=['NA'], 
                   usecols = "B,B:D")

year = int(df.iloc[3][1])
department = df.iloc[4][1]
degree = df.iloc[5][1]

df.drop(df.index[:9], inplace=True)
df.columns = ['username', 'full_name', 'sex']