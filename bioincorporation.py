# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:14:19 2026

@author: Guillaume
"""

import subprocess
import os
from pathlib import Path
import numpy as np
from DLF import *
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd
import matplotlib.pyplot as plt

fpath = Path().resolve()
path_dai = os.path.join(fpath, "lonzee_bioinc.dai")
path_crop = os.path.join(fpath, "CROP_LTO_bioinc.dai")
path_bio = os.path.join(fpath, "run_current_bioinc.dai")
path_trad = os.path.join(fpath, "results", "trad")


# subprocess.run([r"C:\Program Files\daisy 7.1.0\bin\daisy.exe", path_dai])

bioinc = open(path_dai).read()
crop = open(path_crop).read()

# Rmax = np.linspace(0.1, 1.0, 10)
Rmax = np.linspace(0.1, 0.9, 9)
prof_max = np.linspace(-30, -100, 8)

path_src = os.path.join(fpath, "results", "bioinc")        
path_src = Path(path_src)

list_dlf = [f.name for f in path_src.glob("*.dlf")]
interest_var = ["NEE Daisy", "AOM_C", "SMB_C", "SOM_C", "Soil_C"]

#%%
for r in Rmax: 
    for p in prof_max:
        dai_run = crop.replace("@Rmax@", f"{r:.1f}")
        if p == -30:
            dai_run = dai_run.replace("(@prof_max@ [cm] 0 []) ", "")
        else:
            dai_run = dai_run.replace("@prof_max@", str(p))
        
        with open("run_current_CROP_LTO_bioinc.dai", "w") as f:
            f.write(dai_run)

        dai_run = bioinc.replace("@Rmax@", f"{r:.1f}")
        dai_run = dai_run.replace("@prof_max@", str(p))

        with open("run_current_bioinc.dai", "w") as f:
            f.write(dai_run)
            
        print(f"Running: rmax {r:.1f} and prof_max {p}")
        
        subprocess.run([r"C:\Program Files\daisy 7.1.0\bin\daisy.exe", path_bio])
        
        
#%%
"Lecture des fichier résultats"

"Flux hourly"

df = pd.DataFrame()

plt.figure()
for r in Rmax:
    df_temp = pd.DataFrame()
    for d in list_dlf:
        if "flux_hourly" in d and f"{r:.1f}" in d:
            flux = dlf(d, path_src, interest_var)
            flux.open_dlf()
            df_temp[d] = flux.df["NEE Daisy"]  
    df[f"{r:.1f}"] =  df_temp.mean(axis=1, skipna=True)

    dt = flux.df["dt"]
    
    plt.plot(dt, df[f"{r:.1f}"], label=f"{r:.1f}")
    
bande_crop(plt)
plt.title("Flux en fonction des différents Rmax")
plt.legend()
plt.grid(True)
plt.ylabel("NEE [umol CO2/m²/s]")
plt.xlabel("Date")

plt.show


df = pd.DataFrame()

plt.figure()
for p in prof_max:
    df_temp = pd.DataFrame()
    for d in list_dlf:
        if "flux_hourly" in d and f"{p:.1f}" in d:
            flux = dlf(d, path_src, interest_var)
            flux.open_dlf()
            df_temp[d] = flux.df["NEE Daisy"]  
    df[f"{p:.1f}"] =  df_temp.mean(axis=1, skipna=True)

    dt = flux.df["dt"]
    
    plt.plot(dt, df[f"{p:.1f}"], label=f"{p:.1f}")
    
bande_crop(plt)
plt.title("Flux en fonction des différents prof_max")
plt.legend()
plt.grid(True)
plt.ylabel("NEE [umol CO2/m²/s]")
plt.xlabel("Date")

plt.show
#%%
"Flux daily"

df = pd.DataFrame()

plt.figure()
for r in Rmax:
    df_temp = pd.DataFrame()
    for d in list_dlf:
        if "flux_daily" in d and f"{r:.1f}" in d:
            flux = dlf(d, path_src, interest_var)
            flux.open_dlf()
            df_temp[d] = flux.df["NEE Daisy"]  
    df[f"{r:.1f}"] =  df_temp.mean(axis=1, skipna=True)

    dt = flux.df["dt"]
    
    plt.plot(dt, df[f"{r:.1f}"], label=f"{r:.1f}")
plt.title("Flux en fonction des différents Rmax")
bande_crop(plt)
plt.legend()
plt.grid(True)
plt.ylabel("NEE [umol CO2/m²/s]")
plt.xlabel("Date")

plt.show


df = pd.DataFrame()

plt.figure()
for p in prof_max:
    df_temp = pd.DataFrame()
    for d in list_dlf:
        if "flux_daily" in d and f"{p:.1f}" in d:
            flux = dlf(d, path_src, interest_var)
            flux.open_dlf()
            df_temp[d] = flux.df["NEE Daisy"]  
    df[f"{p:.1f}"] =  df_temp.mean(axis=1, skipna=True)

    dt = flux.df["dt"]
    
    plt.plot(dt, df[f"{p:.1f}"], label=f"{p:.1f}")
bande_crop(plt)
plt.title("Flux en fonction des différents prof_max")
plt.legend()
plt.grid(True)
plt.ylabel("NEE [umol CO2/m²/s]")
plt.xlabel("Date")

plt.show

#%%
trad = dlf("trad_tot.dlf", path_trad, ["Surface_C"])
trad.open_dlf()

prof = [prof_max[0], prof_max[5], prof_max[-1]]

fig, axs = plt.subplots(nrows=1, ncols=len(prof), sharex=True, sharey=True)

for i, p  in enumerate(prof):
    for d in list_dlf:
        if str(p) in d and "flux_daily" in d:
            flux = dlf(d, path_src, interest_var)
            flux.open_dlf()
            dt = flux.df["dt"]
            rmax = flux.name[11:14]
            
            axs[i].plot(dt, flux.df["NEE Daisy"], label=rmax)
            
    axs[i].set_title("profmax = " + str(p)[0:-2] + "cm")
    bande_crop(axs[i])
    axs[i].grid(True)
    axs[i].xaxis.set_major_locator(mticker.MaxNLocator(nbins=6))  # moins de ticks
    axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    axs[i].set_xlabel("Date")
    
    if i != 0:
        axs[i].tick_params(axis='both', which='both', length=0)
    
    ax2 = axs[i].twinx()
    ax2.plot(trad.df["dt"], trad.df["Surface_C"], color="red", label="Surface_C")
    
    ax2.set_ylim(-12, 4)
    
    if i != len(prof) - 1:
        ax2.set_yticklabels([])
        ax2.tick_params(left=False, right=False)  
        ax2.spines['right'].set_visible(False) 
    else:
        ax2.set_ylabel("Surface_C")
    
axs[0].set_ylabel("NEE [umol CO2/m²/s]")
fig.suptitle("Flux en fonction de Rmax")
    

Rm = [Rmax[0], Rmax[4], Rmax[-1]]

fig, axs = plt.subplots(nrows=1, ncols=len(Rm), sharex=True, sharey=True)

for i, r  in enumerate(Rm):
    for d in list_dlf:
        if str(r) in d and "flux_daily" in d:
            flux = dlf(d, path_src, interest_var)
            flux.open_dlf()
            dt = flux.df["dt"]
            profm = flux.name[15:19]
            
            axs[i].plot(dt, flux.df["NEE Daisy"], label=profm)
            
    axs[i].set_title("Rmax = " + str(r) + "cm")
    bande_crop(axs[i])
    axs[i].grid(True)
    axs[i].xaxis.set_major_locator(mticker.MaxNLocator(nbins=6))  # moins de ticks
    axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    axs[i].set_xlabel("Date")
    
    if i != 0:
        axs[i].tick_params(axis='both', which='both', length=0)
    
    ax2 = axs[i].twinx()
    ax2.plot(trad.df["dt"], trad.df["Surface_C"], color="red", label="Surface_C")
    
    ax2.set_ylim(-12, 4)
    
    if i != len(prof) - 1:
        ax2.set_yticklabels([])
        ax2.tick_params(left=False, right=False)  
        ax2.spines['right'].set_visible(False) 
    else:
        ax2.set_ylabel("Surface_C")
    
axs[0].set_ylabel("NEE [umol CO2/m²/s]")
fig.suptitle("Flux en fonction de prof_max")
#%%    

"Soil Carbone"
prof = ["0_30", "30_60", "60_90"]
styles = {
    "0_30": "-",
    "30_60": "--",
    "60_90": ":"
}

results = {
    "0_30": {
        "AOM": pd.DataFrame(),
        "SMB": pd.DataFrame(),
        "SOM": pd.DataFrame(),
        "SOC": pd.DataFrame()
    },
    "30_60": {
        "AOM": pd.DataFrame(),
        "SMB": pd.DataFrame(),
        "SOM": pd.DataFrame(),
        "SOC": pd.DataFrame()
    },
    "60_90": {
        "AOM": pd.DataFrame(),
        "SMB": pd.DataFrame(),
        "SOM": pd.DataFrame(),
        "SOC": pd.DataFrame()
    }
}


fig, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
for r in Rmax:
    for d in list_dlf:
        if "bio" in d and f"{r:.1f}" in d:
            for p in prof:
                if p in d: 
                    AOM = pd.DataFrame()
                    SMB = pd.DataFrame()
                    SOM = pd.DataFrame()
                    SOC = pd.DataFrame()
                    print(d)
                    bio = dlf(d, path_src, interest_var)    
                    bio.open_dlf()
                    AOM[d] = bio.df["AOM_C"]   
                    SMB[d] = bio.df["SMB_C"]  
                    SOM[d] = bio.df["SOM_C"]  
                    SOC[d] = bio.df["Soil_C"]  
                
                results[p]["AOM"][f"{r:.1f}"] = AOM.mean(axis=1, skipna=True)
                results[p]["SMB"][f"{r:.1f}"] = SMB.mean(axis=1, skipna=True)
                results[p]["SOM"][f"{r:.1f}"] = SOM.mean(axis=1, skipna=True)
                results[p]["SOC"][f"{r:.1f}"] = SOC.mean(axis=1, skipna=True)

                dt = bio.df["dt"]
                
                axs[0].plot(dt, results[p]["AOM"][f"{r:.1f}"], linestyle=styles[p])
                axs[1].plot(dt, results[p]["SMB"][f"{r:.1f}"], linestyle=styles[p])
                axs[2].plot(dt, results[p]["SOM"][f"{r:.1f}"], linestyle=styles[p])
                axs[3].plot(dt, results[p]["SOC"][f"{r:.1f}"], linestyle=styles[p])

for i in range(len(axs)):
    axs[i].set_ylabel("t C/ha")
    bande_crop(axs[i])
    axs[i].grid(True)

axs[-1].set_xlabel("Date")
fig.suptitle("Stocks de carbone dans les différents pools et à différentes profondeurs \n en fonction des différents Rmax")
fig.show()


results = {
    "0_30": {
        "AOM": pd.DataFrame(),
        "SMB": pd.DataFrame(),
        "SOM": pd.DataFrame(),
        "SOC": pd.DataFrame()
    },
    "30_60": {
        "AOM": pd.DataFrame(),
        "SMB": pd.DataFrame(),
        "SOM": pd.DataFrame(),
        "SOC": pd.DataFrame()
    },
    "60_90": {
        "AOM": pd.DataFrame(),
        "SMB": pd.DataFrame(),
        "SOM": pd.DataFrame(),
        "SOC": pd.DataFrame()
    }
}


fig, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
for pm in prof_max:
    for d in list_dlf:
        if "bio" in d and f"{pm:.1f}" in d:
            for p in prof:
                if p in d: 
                    AOM = pd.DataFrame()
                    SMB = pd.DataFrame()
                    SOM = pd.DataFrame()
                    SOC = pd.DataFrame()
                    print(d)
                    bio = dlf(d, path_src, interest_var)    
                    bio.open_dlf()
                    AOM[d] = bio.df["AOM_C"]   
                    SMB[d] = bio.df["SMB_C"]  
                    SOM[d] = bio.df["SOM_C"]  
                    SOC[d] = bio.df["Soil_C"]  
                
                results[p]["AOM"][f"{pm:.1f}"] = AOM.mean(axis=1, skipna=True)
                results[p]["SMB"][f"{pm:.1f}"] = SMB.mean(axis=1, skipna=True)
                results[p]["SOM"][f"{pm:.1f}"] = SOM.mean(axis=1, skipna=True)
                results[p]["SOC"][f"{pm:.1f}"] = SOC.mean(axis=1, skipna=True)

                dt = bio.df["dt"]
                
                axs[0].plot(dt, results[p]["AOM"][f"{pm:.1f}"], linestyle=styles[p])
                axs[1].plot(dt, results[p]["SMB"][f"{pm:.1f}"], linestyle=styles[p])
                axs[2].plot(dt, results[p]["SOM"][f"{pm:.1f}"], linestyle=styles[p])
                axs[3].plot(dt, results[p]["SOC"][f"{pm:.1f}"], linestyle=styles[p])

for i in range(len(axs)):
    axs[i].set_ylabel("t C/ha")
    bande_crop(axs[i])
    axs[i].grid(True)

axs[-1].set_xlabel("Date")
fig.suptitle("Stocks de carbone dans les différents pools et à différentes profondeurs \n en fonction des différents profmax")
fig.show()

















