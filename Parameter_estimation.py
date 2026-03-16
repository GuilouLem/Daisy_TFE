# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:46:08 2025

@author: u226422
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from pydaisy import Daisy
import datetime
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error


#%% DATA READING

def read_L2_file(csv_file):
    os.chdir(r'C:\Users\u226422\Documents\CALIB\L2')
    return pd.read_csv(csv_file, index_col='TIMESTAMP_END', date_parser=pd.to_datetime,
                       na_values="-9999")


df = read_L2_file('FLX_BE-Lon_FLUXNET_2004-2020.csv')
dfs = pd.concat([df, read_L2_file('FLX_BE-Lon_FLUXNET_2021-2022.csv')])
dfs.index = dfs.index + datetime.timedelta(minutes=30)
df_col = dfs.columns

fraction = dfs.loc['2014-01-01 00:00:00':'2022-12-25 00:00:00', 'PPFD_DIF']/dfs.loc['2014-01-01 00:00:00':'2022-12-25 00:00:00', 'PPFD_IN']
hourly_fraction = fraction.fillna(np.inf).groupby(pd.Grouper(freq='H')).mean().replace(np.inf, np.nan)
hourly_fraction.isna().sum()
hourly_fraction.loc[hourly_fraction > 1.0] = np.nan
hourly_fraction.dropna(inplace=True)


#%% DWF FILE

df_meteo = dfs.loc[:, ['TA_F', 'SW_IN_F', 'VPD_F', 'WS_F', 'P_F']]
df_meteo.isna().sum()
df_meteo.loc[df_meteo.loc[:, 'SW_IN_F'] < 0, 'SW_IN_F'] = 0
df_mean = df_meteo.loc[:, ['TA_F', 'SW_IN_F', 'VPD_F', 'WS_F']].groupby(pd.Grouper(freq='H')).mean()
df_P = df_meteo.loc[:, 'P_F'].groupby(pd.Grouper(freq='H')).sum()
output = pd.concat([df_mean, df_P], axis=1)  # , sif_mean
years = output.index.year
months = output.index.month
days = output.index.day
hours = output.index.hour
all_var = output.round(2)
all_var.insert(0, "Year", years)
all_var.insert(1, "Month", months)
all_var.insert(2, "Day", days)
all_var.insert(3, "Hour", hours)
all_var.to_csv('Lonzee_hourly_weather_difrad.csv', sep='\t', index=False)

#%% RUNNING DAISY TO TEST

d = Daisy.DaisyModel(r"C:\Users\u226422\Documents\CALIB\difrad"+r'\Lonzee_all.dai')
Daisy.DaisyModel.path_to_daisy_executable = r'C:\Program Files\Daisy 2.11\bin\daisy.exe'
d.run()

b0 = -2.397
b1 = 2.771
b2 = 0.0334
b3 = 0.0536
b4 = 1.028

def incredibly_totally_accurate_modela(x):
    d.Input['defcolumn']['Bioclimate']['difrad']['beta0'].setvalue(x[0])
    d.Input['defcolumn']['Bioclimate']['difrad']['beta1'].setvalue(x[1])
    d.Input['defcolumn']['Bioclimate']['difrad']['beta2'].setvalue(x[2])
    d.Input['defcolumn']['Bioclimate']['difrad']['beta3'].setvalue(x[3])
    d.Input['defcolumn']['Bioclimate']['difrad']['beta4'].setvalue(x[4])
    d.save_as(r"C:\Users\u226422\Documents\CALIB\difrad"+r'\Lonzee_test.dai')
    d.run()
    max_retries = 3
    retries = 0
    success = False
    while not success and retries < max_retries:
        try:
            dlf = pd.read_csv(r"C:\Users\u226422\Documents\CALIB\difrad"+r'\diffuse.dlf', sep='\t',
                              skiprows=15, header=[0, 1])
            dlf.columns = dlf.columns.droplevel(1)
            dlf.rename(columns={"mday": "day"}, inplace=True)
            dlf.set_index(pd.to_datetime(dlf[['year', 'month', 'day', 'hour']]), inplace=True)
            fraction_ = dlf['difrad0']/dlf['global_radiation']
            fraction_model = fraction_.loc[hourly_fraction.index]
            success = True
        except KeyError:
            retries += 1
            d.run()
            print(f"Erreur de convergence (KeyError) - Tentative {retries}/{max_retries}")
    dlf = pd.read_csv(r"C:\Users\u226422\Documents\CALIB\difrad"+r'\diffuse.dlf', sep='\t',
                      skiprows=15, header=[0, 1])
    dlf.columns = dlf.columns.droplevel(1)
    dlf.rename(columns={"mday": "day"}, inplace=True)
    dlf.set_index(pd.to_datetime(dlf[['year', 'month', 'day', 'hour']]), inplace=True)
    fraction_ = dlf['difrad0']/dlf['global_radiation']
    fraction_model = fraction_.loc[hourly_fraction.index]
    fraction_model.dropna(inplace=True)
    fraction_data = hourly_fraction.loc[fraction_model.index] 
    RMSE = np.sqrt(mean_squared_error(fraction_data, fraction_model)).sum()
    return RMSE


opti = minimize(incredibly_totally_accurate_modela, [b0, b1, b2, b3, b4], method='nelder-mead',
                bounds=[(-7.0, -1.0), (0.0, 9.0), (-0.1, 0.1), (-0.1, 0.1), (0.0, 3.0)], options={'disp': True})

#%% PLOTTING

d.Input['defcolumn']['Bioclimate']['difrad']['beta0'].setvalue(opti.x[0])
d.Input['defcolumn']['Bioclimate']['difrad']['beta1'].setvalue(opti.x[1])
d.Input['defcolumn']['Bioclimate']['difrad']['beta2'].setvalue(opti.x[2])
d.Input['defcolumn']['Bioclimate']['difrad']['beta3'].setvalue(opti.x[3])
d.Input['defcolumn']['Bioclimate']['difrad']['beta4'].setvalue(opti.x[4])
d.save_as(r"C:\Users\u226422\Documents\CALIB\difrad"+r'\Lonzee_test.dai')
d.run()
dlf = pd.read_csv(r"C:\Users\u226422\Documents\CALIB\difrad"+r'\diffuse.dlf', sep='\t',
                  skiprows=15, header=[0, 1])
dlf.columns = dlf.columns.droplevel(1)
dlf.rename(columns={"mday": "day"}, inplace=True)
dlf.set_index(pd.to_datetime(dlf[['year', 'month', 'day', 'hour']]), inplace=True)
fraction_ = dlf['difrad0']/dlf['global_radiation']
fraction_model = fraction_.loc[hourly_fraction.index]
fraction_model.dropna(inplace=True)
fraction_data = hourly_fraction.loc[fraction_model.index] 
RMSE = np.sqrt(mean_squared_error(fraction_data, fraction_model)).sum()

dai = Daisy.DaisyModel(r"C:\Users\u226422\Documents\CALIB\difrad"+r'\Lonzee_dpf.dai')
Daisy.DaisyModel.path_to_daisy_executable = r'C:\Program Files\Daisy 2.9\bin\daisy.exe'
dai.run()
dlf = pd.read_csv(r"C:\Users\u226422\Documents\CALIB\difrad"+r'\diffuse.dlf', sep='\t',
                  skiprows=15, header=[0, 1])
dlf.columns = dlf.columns.droplevel(1)
dlf.rename(columns={"mday": "day"}, inplace=True)
dlf.set_index(pd.to_datetime(dlf[['year', 'month', 'day', 'hour']]), inplace=True)
fraction_ = dlf['difrad0']/dlf['global_radiation']
fraction_daisy = fraction_.loc[fraction_data.index]

fig, ax = plt.subplots()
ax.scatter(fraction_data.index, fraction_data, label='data', s=8)
ax.scatter(fraction_model.index, fraction_model, label='BRL model', s=8)
ax.legend()

fig, ax = plt.subplots()
ax.plot(fraction_data, label='data', marker='o', ms=8, color='black')
ax.plot(fraction_model, label='BRL model', marker='o', ms=8, color='red')
ax.plot(fraction_daisy, label='DPF model', marker='o', ms=8, color='blue')
ax.legend()

fig, ax = plt.subplots()
ax.plot([[0, 0], [1, 1]], color='black')
ax.scatter(fraction_data, fraction_daisy, label='DPF model', color='blue', alpha=0.8)
ax.scatter(fraction_data, fraction_model, label='BRL model', color='red', alpha=0.8)
ax.set_ylabel('Modelled diffuse fraction')
ax.set_xlabel('Measured diffuse fraction')
ax.legend()
