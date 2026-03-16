# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:28:28 2022

@author: u226422
"""

import pandas as pd
import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def read_L2_unlab_file(csv_file):
    os.chdir('C:/Users/u226422/OneDrive - Universite de Liege/Documents/Measurements/Lonzee_data/L2')
    return pd.read_csv(csv_file, index_col='Timestamp', date_parser=pd.to_datetime,
                       na_values="-9999")


def read_L2_file(csv_file):
    os.chdir('C:/Users/u226422/OneDrive - Universite de Liege/Documents/Measurements/Lonzee_data/L2')
    return pd.read_csv(csv_file, index_col='TIMESTAMP_END', date_parser=pd.to_datetime,
                       na_values="-9999")


def read_pheno_file(file):
    os.chdir('C:/Users/u226422/OneDrive - Universite de Liege/Documents/Measurements/Lonzee_data')
    return pd.read_excel(file, header=0, index_col='Date', date_parser=pd.to_datetime)


def read_pameseb_file(txt_file):
    os.chdir('C:/Users/u226422/OneDrive - Universite de Liege/Documents/Measurements/Lonzee_data/Pameseb')
    return pd.read_csv(txt_file, na_values="-9999.0", index_col='timestamp',
                       date_parser=pd.to_datetime)


def gap_filling(df, var):
    """
    Returns the weather observation gap-filled with the measurements provided
    by the second station (backup) at the same height.

    Parameter
    ---------
    df : dataframe containing both variables(the main and the second/doublon one)
    var : weather observation variable to gap-fill

    """
    df_filled = df[var].fillna(df[var.rsplit(sep='_', maxsplit=1)[0] + '_2'])
    print('For the variable '+var+': '
          + str(df[var].isna().sum()-df_filled.isna().sum())+' NaN values replaced\n'
          + ' and '+str(df_filled.isna().sum())+' NaN remaining.')
    return df_filled


def lin_reg(x, y):
    """
    Computes the parameters of the linear regession between x and y and
    returns x gap-filled with the regression if possible
    """
    mask = ~np.isnan(x) & ~np.isnan(y)
    reg = stats.linregress(x[mask], y[mask])
    x = x.fillna(y/reg[0] - reg[1])
    print('For the variable SW_IN: '+str(x.isna().sum())+'NaN remaining')
    print(reg[0])
    return x


def roll_mean(var, win):
    """
    Returns weather observation data gap-filled with a rolling mean

    Parameter
    ---------
    var : Series
        Weather observations.
    win : int
        Size of the window.

    """
    var = var.fillna(var.rolling(window=win, min_periods=1,
                                 center=True).mean())
    if (var.isna().sum()) > 0:
        print("Error: Missing gaps are too significant for", var.name, "data")
        print("There're still", var.isna().sum(), "values needed to be filled")
    return var


def graphs(obj, var, titre, line):
    fig, axs = plt.subplots(3, 3, sharey=True, figsize=(11, 8))
    axs = axs.ravel()
    for i in range(9):
        if line == 0:
            axs[i].scatter(getattr(obj[i], var).index, getattr(obj[i], var), s=15)
        elif line == 1:
            axs[i].plot(getattr(obj[i], var))
        axs[i].set_title(obj[i].name, fontsize=10, pad=2, loc='left')
        axs[i].xaxis.set_major_locator(mdates.MonthLocator())
        axs[i].xaxis.set_major_formatter(mdates.ConciseDateFormatter
                                         (axs[i].xaxis.get_major_locator()))
        axs[i].set_xlim(obj[i].sowing, obj[i].harvest)
    fig.suptitle(titre, fontweight='bold', y=0.93)


def graphs_VPD(obj, var, titre):
    fig, axs = plt.subplots(3, 3, sharey=True, figsize=(11, 8))
    axs = axs.ravel()
    for i in range(9):
        if var == 'SWIN':
            variable = getattr(obj[i], var)
        else:
            variable = getattr(obj[i], var)[:-1]
        variable = variable[variable.notna()]
        axs[i].scatter(variable[(obj[i].VPD_class == 1)].index, variable[(obj[i].VPD_class == 1)],
                       label='VPD<0.5', c='blue', s=15)
        axs[i].scatter(variable[(obj[i].VPD_class == 2)].index, variable[(obj[i].VPD_class == 2)],
                       label='0.5<VPD<1.2', c='cornflowerblue', s=15)
        axs[i].scatter(variable[(obj[i].VPD_class == 3)].index, variable[(obj[i].VPD_class == 3)],
                       label='1.2<VPD<1.5', c='mediumseagreen', s=15)
        axs[i].scatter(variable[(obj[i].VPD_class == 4)].index, variable[(obj[i].VPD_class == 4)],
                       label='1.5<VPD<2', c='yellowgreen', s=15)
        axs[i].scatter(variable[(obj[i].VPD_class == 5)].index, variable[(obj[i].VPD_class == 5)],
                       label='2<VPD<2.5', c='peru', s=15)
        axs[i].scatter(variable[(obj[i].VPD_class == 6)].index, variable[(obj[i].VPD_class == 6)],
                       label='VPD>2.5', c='firebrick', s=15)
        axs[i].set_title(obj[i].name, fontsize=10, pad=2, loc='left')
        axs[i].xaxis.set_major_locator(mdates.MonthLocator())
        axs[i].xaxis.set_major_formatter(mdates.ConciseDateFormatter
                                         (axs[i].xaxis.get_major_locator()))
        axs[i].set_xlim(obj[i].sowing, obj[i].harvest)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower right', title='VPD [kPa]')
    fig.suptitle(titre, fontweight='bold', y=0.93)


def graphs_REW(obj, var, classe, titre):
    fig, axs = plt.subplots(3, 3, sharey=True, figsize=(11, 8))
    axs = axs.ravel()
    for i in range(9):
        if var == 'SWIN':
            variable = getattr(obj[i], var)
        else:
            variable = getattr(obj[i], var)[:-1]
        variable = variable[variable.notna()]
        mask = getattr(obj[i], classe)
        axs[i].scatter(variable[(mask == 1)].index, variable[(mask == 1)],
                       label='REW>=1', c='blue', s=15)
        axs[i].scatter(variable[(mask == 2)].index, variable[(mask == 2)],
                       label='0.5<REW<1', c='cornflowerblue', s=15)
        axs[i].scatter(variable[(mask == 3)].index, variable[(mask == 3)],
                       label='0.4<REW<=0.5', c='peru', s=15)
        axs[i].scatter(variable[(mask == 4)].index, variable[(mask == 4)],
                       label='REW<=0.4', c='firebrick', s=15)
        axs[i].set_title(obj[i].name, fontsize=10, pad=2, loc='left')
        axs[i].xaxis.set_major_locator(mdates.MonthLocator())
        axs[i].xaxis.set_major_formatter(mdates.ConciseDateFormatter
                                         (axs[i].xaxis.get_major_locator()))
        axs[i].set_xlim(obj[i].sowing, obj[i].harvest)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower right')
    fig.suptitle(titre, fontweight='bold', y=0.93)
