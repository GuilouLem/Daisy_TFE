# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 13:03:49 2026

@author: Guillaume
"""

"Lecture DWF"

import os 
from pathlib import Path 
import matplotlib.pyplot as plt
import pandas as pd

fpath = Path().resolve()
path_src = os.path.join(fpath, "lonzee_daily_G.dwf")

dwf = pd.read_csv(path_src, sep="\t", skiprows=37)
unit = dwf.iloc[0]
dwf = dwf.drop(index=0)

dwf["dt"] = pd.to_datetime(dict(year=dwf["Year"], month=dwf["Month"], day=dwf["Day"], hour=dwf["Hour"]))

dwf = dwf.drop(dwf.columns[[0, 1, 2, 3]], axis=1)
var = dwf.columns.tolist()
var.remove("dt")
dic = {col: unit[col] for col in var}

for v in var:
    print(v)
    plt.figure()
    plt.plot(dwf["dt"], dwf[v].astype(float))
    plt.xlabel("Date")
    plt.ylabel(f"{v} [{dic[v]}]")
    plt.title(v)
    plt.show()
    
    
    
    
    
    