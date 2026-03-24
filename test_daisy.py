# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:29:16 2026

@author: Guillaume
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from PyDaisy import Daisy
import datetime
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import os
from pathlib import Path

fpath = Path().resolve()
path_src = os.path.join(fpath, "lonzee_estimation.dai")



d = Daisy.DaisyModel(path_src)

print(type(d.Input))
print(d.Input)

Daisy.DaisyModel.path_to_daisy_executable = r"C:\Program Files\daisy 7.1.0\bin\daisy.exe"
d.run()

for child in d.Input:
    print(child)


# d = Daisy.DaisyModel(path_src)
# print(path_src)
# Daisy.DaisyModel.path_to_daisy_executable = r"C:\Program Files\daisy 7.1.0\bin\daisy.exe"
# d.run()




#%%
print(d.Input['defcolumn'])
d.Input['defcolumn']['Bioclimate']['difrad']['beta0'].setvalue(4)
