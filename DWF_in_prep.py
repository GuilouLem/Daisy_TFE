# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 10:53:58 2022

@author: u226422
"""

import pandas as pd
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
import scipy.io
os.chdir(r"C:\Users\Guillaume\Desktop\TFE\Code Laura")
import funcs

#%%
# #%%
# # import ann


# #  ---  LECTURE DES FICHIERS D'ENTREE  ---

# L2 = funcs.read_L2_unlab_file('BE-Lon_L2_1401-1412.csv')
# for i in ['15', '16', '17', '18', '19', '20', '21']:
#     L2 = pd.concat([L2, funcs.read_L2_file('BE-Lon_L2_'+i+'01-'+i+'12.csv')], sort=False)
# L2 = pd.concat([L2, funcs.read_L2_file('BE-Lon_L2_2201-2212.csv')], sort=False)

# L2['SW_IN_1_1_1'] = funcs.gap_filling(L2, 'SW_IN_1_1_1')
# L2['SW_IN_1_1_1'] = funcs.lin_reg(L2['SW_IN_1_1_1'], L2['PPFD_IN_1_1_1'])
# L2['SW_IN_1_1_1'] = funcs.lin_reg(L2['SW_IN_1_1_1'], L2['PPFD_IN_1_1_2'])
# L2['TA_1_1_1'] = funcs.gap_filling(L2, 'TA_1_1_1')
# L2['RH_1_1_1'] = funcs.gap_filling(L2, 'RH_1_1_1')
# L2['P_1_1_1'] = funcs.gap_filling(L2, 'P_1_1_1')
# L2['WS_1_1_1'] = funcs.gap_filling(L2, 'WS_1_1_1')
# L2['WD_1_1_1'] = funcs.gap_filling(L2, 'WD_1_1_1')

# columns_wanted = ['TA_1_1_1', 'SW_IN_1_1_1', 'RH_1_1_1', 'WS_1_1_1', 'P_1_1_1']
# L2 = L2.loc[:, columns_wanted]
# df = L2.loc[:, ['TA_1_1_1', 'SW_IN_1_1_1', 'RH_1_1_1',
#                 'WS_1_1_1']].groupby(pd.Grouper(freq='H')).mean()
# df_P = L2.loc[:, 'P_1_1_1'].fillna(np.inf).groupby(pd.Grouper(freq='H')).sum().replace(np.inf,
#                                                                                        np.nan)
# df = pd.concat([df, df_P], axis=1)
# print('NaNs remaining', df.isna().sum())

# PMSB = funcs.read_pameseb_file('grouped_010116_311219_hora.txt')
# PMSB.index = PMSB.index - pd.DateOffset(hours=1)
# PMSB['time'] = PMSB.index
# set_index = PMSB.set_index(['sid', 'time'], inplace=True)


# #  ---  RESEAU NEURONAL - GAP-FILLING OF WIND STRENGTH  ---

# X = df.loc['2016-01-01 00:00:00':'2019-12-31 22:00:00'].copy()
# X['26_WS'] = PMSB.xs(26, level='sid').loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'vvt']
# X['27_WS'] = PMSB.xs(27, level='sid').loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'vvt']
# X['19_WS'] = PMSB.xs(19, level='sid').loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'vvt']
# X['18_WS'] = PMSB.xs(18, level='sid').loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'vvt']
# X['26_SW'] = PMSB.xs(26, level='sid').loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'ens']
# X['27_SW'] = PMSB.xs(27, level='sid').loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'ens']
# X['19_SW'] = PMSB.xs(19, level='sid').loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'ens']
# X['18_SW'] = PMSB.xs(18, level='sid').loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'ens']

# # WS_NN_X = ann.Neuronal_network(X, 'WS_1_1_1', df, 12,
# #                                df.loc['2016-01-01 00:00:00':'2019-12-31 22:00:00'])

# #  2014-2015

# PMSB_Y = funcs.read_pameseb_file('27_010114_311215_hora.txt')
# PMSB_Y.index = PMSB_Y.index - pd.DateOffset(hours=1)
# PMSB_Y['time'] = PMSB_Y.index

# Y = df.loc['2014-01-01 00:00:00':'2015-12-31 22:00:00'].copy()
# Y['27_WS'] = PMSB_Y.loc['2014-01-01 00:00:00':'2015-12-31 22:00:00', 'vvt']
# Y['27_SW'] = PMSB_Y.loc['2014-01-01 00:00:00':'2015-12-31 22:00:00', 'ens']

# # WS_NN_Y = ann.Neuronal_network(Y, 'WS_1_1_1', df, 6,
# #                                df.loc['2014-01-01 00:00:00':'2015-12-31 22:00:00'])

# # df.loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'WS_f'] = df.loc['2016-01-01 00:00:00':'2019-12-31 22:00:00', 'WS_1_1_1'].fillna(WS_NN_X)
# # df.loc['2014-01-01 00:00:00':'2015-12-31 22:00:00', 'WS_f'] = df.loc['2014-01-01 00:00:00':'2015-12-31 22:00:00', 'WS_1_1_1'].fillna(WS_NN_Y)
# # df.loc['2019-12-31 22:00:00':, 'WS_f'] = df.loc['2019-12-31 22:00:00':, 'WS_1_1_1']

# fig, ax = plt.subplots(2)
# ax[0].plot(df['WS_f'])
# ax[0].set_title('Gap filled wind speed')
# ax[1].plot(df['WS_1_1_1'])
# ax[1].set_title('Non gap filled wind speed')
# fig.autofmt_xdate(rotation=30)

# #%%  ---  SEPARATION DU FICHIER POUR CHAQUE VARIETE  ---

# def read_pheno_file(file):
#     os.chdir('C:/Users/u226422/OneDrive - Universite de Liege/Documents/Measurements/Lonzee_data')
#     return pd.read_excel(file, engine='openpyxl', header=0, index_col='Date', date_parser=pd.to_datetime)


class Variety:
    def __init__(self, name):
        self.name = name

    def wheat_period(self, pheno, df):
        self.sowing = pheno[(pheno['Variété'] == str(self.name)) &
                            (pheno['Stade BBCH'] == 0)].index.tolist()[0]
        self.harvest = pheno[(pheno['Variété'] == str(self.name)) &
                             (pheno['Stade BBCH'] == 99)].index.tolist()[0]
        self.meteo = df.loc[self.sowing - pd.DateOffset(days=10):
                            self.harvest + pd.DateOffset(days=10)].copy()


bbch = read_pheno_file('Wheat_phenology.xlsx')
varieties = ['Sahara2', 'Tobak', 'KWS Smart', 'LG Skyscraper']
objs = [Variety(i) for i in iter(varieties)]
for obj in range(len(objs)):
    objs[obj].wheat_period(bbch, df)
    print(objs[obj].name, objs[obj].meteo.isna().sum())
    objs[obj].meteo.loc[objs[obj].meteo.loc[:, 'SW_IN_1_1_1'] < 0, 'SW_IN_1_1_1'] = 0
    for j in iter(['TA_1_1_1', 'SW_IN_1_1_1', 'RH_1_1_1', 'P_1_1_1', 'WS_f']):
        objs[obj].meteo[j] = funcs.roll_mean(objs[obj].meteo[j], 5)
    print(objs[obj].name, objs[obj].meteo.isna().sum())

# #  objs[0].meteo.loc[objs[0].meteo.loc[:,'P_1_1_1'].isna(), 'P_1_1_1']

# #%%  ---  POTATO CROP  ---

def read_L2_file(csv_file):
    os.chdir(r'C:\Users\Guillaume\Desktop\TFE')
    return pd.read_csv(csv_file, index_col='TIMESTAMP_END', date_parser=pd.to_datetime,
                       na_values="-9999")


df = read_L2_file(r"C:\Users\Guillaume\Desktop\TFE\FLX_BE-Lon_FLUXNET_2004-2020.csv")
names = df.columns
df_meteo_MDS = df.loc['2018-04-13 00:00:00':'2018-09-21 00:00:00', ['TA_F_MDS', 'SW_IN_F_MDS',
                                                                    'VPD_F_MDS', 'WS_F', 'P_F']]
df_meteo = df.loc['2018-04-13 00:00:00':'2018-09-21 00:00:00', ['TA_F', 'SW_IN_F',
                                                                'VPD_F', 'WS_F', 'P_F']]
df_qc_MDS = df.loc['2018-04-13 00:00:00':'2018-09-21 00:00:00', ['TA_F_MDS_QC', 'SW_IN_F_MDS_QC',
                                                                 'VPD_F_MDS_QC', 'WS_F_QC', 'P_F_QC']]
df_qc = df.loc['2018-04-13 00:00:00':'2018-09-21 00:00:00', ['TA_F_QC', 'SW_IN_F_QC',
                                                             'VPD_F_QC', 'WS_F_QC', 'P_F_QC']]
df_meteo.isna().sum()
df_meteo.loc[df_meteo.loc[:, 'SW_IN_F'] < 0, 'SW_IN_F'] = 0

df_mean = df_meteo.loc[:, ['TA_F', 'SW_IN_F', 'VPD_F', 'WS_F']].groupby(pd.Grouper(freq='H')).mean()
df_P = df_meteo.loc[:, 'P_F'].groupby(pd.Grouper(freq='H')).sum()
output = pd.concat([df_mean, df_P], axis=1)

fig, ax = plt.subplots()
ax.plot(df.loc['2018-04-13 00:00:00':'2018-09-21 00:00:00', ['SWC_F_MDS_1', 'SWC_F_MDS_2',
                                                             'SWC_F_MDS_3', 'SWC_F_MDS_4', 'SWC_F_MDS_5']])

fig, ax = plt.subplots()
ax.plot(df.loc['2018-04-13 00:00:00':'2018-09-21 00:00:00', ['TS_F_MDS_1', 'TS_F_MDS_2', 'TS_F_MDS_3',
                                                             'TS_F_MDS_4', 'TS_F_MDS_5', 'TS_F_MDS_6']])

#%% CORRECTION FOR SKYSCRAPER (30-MIN OFFSET)

data = scipy.io.loadmat('SIFTOT.mat')['SIF_TOT_FULL_PSII']
date = pd.date_range(start='2022-01-01 01:30:00', periods=17520, freq=datetime.timedelta(minutes=30))
df2 = pd.DataFrame(data=data, index=date, columns=['SIF'])
df2.index = df2.index + datetime.timedelta(minutes=30)
sif = df2.loc['2021-10-17 01:00:00':'2022-08-03 23:30:00'] 
sif_mean = sif.fillna(np.inf).groupby(pd.Grouper(freq='H')).mean().replace(np.inf, np.nan)




df = read_L2_file(r"C:\Users\Guillaume\Desktop\TFE\FLX_BE-Lon_FLUXNET_2004-2020.csv")
names = df.columns
df.index = df.index + datetime.timedelta(minutes=30)
df_meteo = df.loc['2021-06-01 01:00:00':'2022-08-03 23:30:00', ['TA_F', 'SW_IN_F',
                                                                'VPD_F', 'WS_F', 'P_F']]

df_meteo.isna().sum()
df_meteo.loc[df_meteo.loc[:, 'SW_IN_F'] < 0, 'SW_IN_F'] = 0
df_mean = df_meteo.loc[:, ['TA_F', 'SW_IN_F', 'VPD_F', 'WS_F']].groupby(pd.Grouper(freq='H')).mean()
df_P = df_meteo.loc[:, 'P_F'].groupby(pd.Grouper(freq='H')).sum()
output = pd.concat([df_mean, df_P], axis=1)  # , sif_mean
output = output.fillna(-1)

#%%  ---  ECRITURE DES FICHIERS DE SORTIE  ---

# for obj in range(len(objs)):
#     output = objs[obj].meteo.loc[:, ['TA_1_1_1', 'SW_IN_1_1_1', 'RH_1_1_1', 'WS_f', 'P_1_1_1']]
#     output.isna().sum()
#     years = output.index.year
#     months = output.index.month
#     days = output.index.day
#     hours = output.index.hour
#     all_var = output.round(2)
#     all_var.insert(0, "Year", years)
#     all_var.insert(1, "Month", months)
#     all_var.insert(2, "Day", days)
#     all_var.insert(3, "Hour", hours)
#     all_var.to_csv('Lonzee_hourly_weather_'+objs[obj].name+'.csv', sep='\t', index=False)

years = output.index.year
months = output.index.month
days = output.index.day
hours = output.index.hour
all_var = output.round(2)
all_var.insert(0, "Year", years)
all_var.insert(1, "Month", months)
all_var.insert(2, "Day", days)
all_var.insert(3, "Hour", hours)
all_var.to_csv('Lonzee_hourly_weather_.csv', sep='\t', index=False)
