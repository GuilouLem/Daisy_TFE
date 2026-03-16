# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:33:03 2025

@author: Guillaume
"""

import pandas as pd
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
import scipy.io
os.chdir(r"C:\Users\Guillaume\Desktop\TFE\Code")
import funcs

def read_L2_file(csv_file):
    os.chdir(r'C:\Users\Guillaume\Desktop\TFE\Code')
    return pd.read_csv(csv_file, index_col='TIMESTAMP_END', parse_dates=True,
                       na_values="-9999")

df = read_L2_file(r"C:\Users\Guillaume\Desktop\TFE\FLX_BE-Lon_FLUXNET_2004-2020.csv")
names = df.columns
df.index = df.index + datetime.timedelta(minutes=30)
df_meteo = df.loc['2016-10-27 01:00:00':'2020-11-18 23:30:00', ['TA_F', 'SW_IN_F',
                                                                'VPD_F', 'WS_F', 'P_F']]

df_meteo.isna().sum()
df_meteo.loc[df_meteo.loc[:, 'SW_IN_F'] < 0, 'SW_IN_F'] = 0
df_mean = df_meteo.loc[:, ['TA_F', 'SW_IN_F', 'VPD_F', 'WS_F']].groupby(pd.Grouper(freq='h')).mean()
df_P = df_meteo.loc[:, 'P_F'].groupby(pd.Grouper(freq='h')).sum()
output = pd.concat([df_mean, df_P], axis=1)  # , sif_mean
output = output.fillna(-1)

years = output.index.year
months = output.index.month
days = output.index.day
hours = output.index.hour
all_var = output.round(2)
all_var.insert(0, "Year", years)
all_var.insert(1, "Month", months)
all_var.insert(2, "Day", days)
all_var.insert(3, "Hour", hours)
all_var = all_var.rename(columns={"TA_F":"AirTemp", "SW_IN_F":"GlobRad", "VPD_F":"VapPres", "WS_F":"Wind", "P_F":"Precip"})

unit = pd.DataFrame(columns=all_var.columns)
unit.loc[0] = ["year", "month", "day", "hour", "dgC", "W/m^2", "hPa", "m/s", "m/h"]
all_var = pd.concat([unit, all_var]) 

all_var.to_csv('lonzee_daily_G.csv', sep='\t', index=False)
