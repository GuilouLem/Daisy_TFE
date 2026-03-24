# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 10:01:14 2026

@author: Guillaume
"""

import subprocess
import os
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution 
from sklearn.metrics import mean_squared_error
import shutil
from DLF import *
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd
import matplotlib.pyplot as plt
import uuid


fpath = Path().resolve()
path_dai = os.path.join(fpath, "lonzee_calib.dai")
path_crop = os.path.join(fpath, "CROP_LTO_calib.dai")
path_results = path_crop.replace(r"Calib\CROP_LTO_calib.dai", r"results\calib")


# subprocess.run([r"C:\Program Files\daisy 7.1.0\bin\daisy.exe", path_dai])

periods = {"wheat17": ["2016-10-29", "2017-07-30"],
            "mustard": ["2017-09-07", "2017-12-07"],
            "potato": ["2018-04-23", "2018-09-11"],
            "wheat19": ["2018-10-10", "2019-08-01"], 
            "faba_oat": ["2019-08-19", "2019-12-03"], 
            "beet": ["2020-04-01", "2020-11-13"]                            
            }


Fm_beet = 7
Qeff_beet = 0.056
Fm_faba = 4
Qeff_faba = 0.04
Fm_oat = 3.5
Qeff_oat = 0.04
Fm_potato = 3
Qeff_potato = 0.045
Fm_mustard = 4
Qeff_mustard = 0.05


boundary = [(2, 8), (0.03, 0.08)]

data = dlf("flux_daily.dlf", path_results, ["NEE ICOS"])
data.path_icos = data.path_icos.replace(r"\Calib", r"")
data.open_ICOS()

NEE_data = data.icos
NEE_data = data.icos[["Date Time", "NEE"]]
NEE_data['Date Time'] = pd.to_datetime(NEE_data['Date Time'])
NEE_data.set_index('Date Time', inplace=True)

template = open(path_crop).read()
template_dai = open(path_dai).read()


# # Fm_mustard = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# Qeff_mustard = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]

# for b in Qeff_mustard:
#     crop_opti = open(path_crop).read()
#     crop_opti = crop_opti.replace("@Fm_beet@", str(Fm_beet))
#     crop_opti = crop_opti.replace("@Qeff_beet@", str(Qeff_beet))
#     crop_opti = crop_opti.replace("@Fm_faba@", str(Fm_faba))
#     crop_opti = crop_opti.replace("@Qeff_faba@", str(Qeff_faba))
#     crop_opti = crop_opti.replace("@Fm_oat@", str(Fm_oat))
#     crop_opti = crop_opti.replace("@Qeff_oat@", str(Qeff_oat))
#     crop_opti = crop_opti.replace("@Fm_potato@", str(Fm_potato))
#     crop_opti = crop_opti.replace("@Qeff_potato@", str(Qeff_potato))
#     crop_opti = crop_opti.replace("@Fm_mustard@", str(Fm_mustard))
#     crop_opti = crop_opti.replace("@Qeff_mustard@", str(b))
    
#     with open("run_current_CROP_LTO_calib.dai", "w") as f:
#         f.write(crop_opti)
    
#     subprocess.run([r"C:\Program Files\daisy 7.1.0\bin\daisy.exe", path_dai])
    
#     flux_model = dlf("flux_hourly.dlf", path_results, ["NEE Daisy"])
#     flux_model.open_dlf()
    
#     NEE_model = flux_model.df
#     NEE_model = NEE_model[["dt", "NEE Daisy"]]
#     NEE_model["dt"] = pd.to_datetime(NEE_model["dt"])
#     NEE_model.set_index("dt", inplace=True)
#     NEE_model = NEE_model.resample('D').mean()
    
#     NEE_model = NEE_model[periods["mustard"][0]:periods["mustard"][1]]
#     NEE_data_filt = NEE_data[periods["mustard"][0]:periods["mustard"][1]]
    
#     RMSE = np.sqrt(mean_squared_error(NEE_data_filt, NEE_model)).sum()
#     print(b, RMSE)
    
#     fig, axs = plt.subplots()
#     axs.plot(NEE_data_filt.index, NEE_data_filt["NEE"])
#     axs.plot(NEE_model.index, NEE_model["NEE Daisy"])
#     axs.grid(True)
#     fig.show()
        
    
def calib(params):
    uid = uuid.uuid4().hex
    run_dir = os.path.join(fpath, f"run_{uid}")
    os.makedirs(run_dir, exist_ok=True)
    crop_file = os.path.join(run_dir, f"CROP_{uid}.dai")
    dai_file = os.path.join(run_dir, f"dai_{uid}.dai")
    
    Fm_beet, Qeff_beet = params
    
    crop_opti = template
    crop_opti = crop_opti.replace("@Fm_beet@", str(Fm_beet))
    crop_opti = crop_opti.replace("@Qeff_beet@", str(Qeff_beet))
    crop_opti = crop_opti.replace("@Fm_faba@", str(Fm_faba))
    crop_opti = crop_opti.replace("@Qeff_faba@", str(Qeff_faba))
    crop_opti = crop_opti.replace("@Fm_oat@", str(Fm_oat))
    crop_opti = crop_opti.replace("@Qeff_oat@", str(Qeff_oat))
    crop_opti = crop_opti.replace("@Fm_potato@", str(Fm_potato))
    crop_opti = crop_opti.replace("@Qeff_potato@", str(Qeff_potato))
    crop_opti = crop_opti.replace("@Fm_mustard@", str(Fm_mustard))
    crop_opti = crop_opti.replace("@Qeff_mustard@", str(Qeff_mustard))
    
    dai_opti = template_dai
    dai_opti = dai_opti.replace("@flux_hourly@", f"C:/Users/Guillaume/Desktop/TFE/Code/Calib/run_{uid}/flux_hourly.dlf")
    dai_opti = dai_opti.replace("@crop_opti@", f"CROP_{uid}.dai")
    dai_opti = dai_opti.replace("@directory@", f"C:/Users/Guillaume/Desktop/TFE/Code/Calib/run_{uid}")
    
    with open(crop_file, "w") as f:
        f.write(crop_opti)
    
    with open(dai_file, "w") as f:
        f.write(dai_opti)
        
    subprocess.run(
        [r"C:\Program Files\daisy 7.1.0\bin\daisy.exe", dai_file],
        cwd=run_dir,
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    
    flux_model = dlf("flux_hourly.dlf", run_dir, ["NEE Daisy"])
    flux_model.open_dlf()
    
    NEE_model = flux_model.df
    NEE_model = NEE_model[["dt", "NEE Daisy"]]
    NEE_model["dt"] = pd.to_datetime(NEE_model["dt"])
    NEE_model.set_index("dt", inplace=True)
    NEE_model = NEE_model.resample('D').mean()
    
    NEE_model = NEE_model[periods["beet"][0]:periods["beet"][1]]
    NEE_data_filt = NEE_data[periods["beet"][0]:periods["beet"][1]]
    
    RMSE = np.sqrt(mean_squared_error(NEE_data_filt, NEE_model))
    
    shutil.rmtree(run_dir)
    
    return RMSE

Fm_mustard = 7.76
Qeff_mustard = 0.075
Fm_potato = 4.88
Qeff_potato = 0.031
Fm_faba = 2.18
Qeff_faba = 0.03
Fm_oat = 2.36
Qeff_oat = 0.033
Fm_beet = 4.63
Qeff_beet = 0.077

if __name__=='__main__':
    from multiprocessing import freeze_support
    freeze_support()

    opti = differential_evolution(calib, bounds=boundary, maxiter=10, popsize=5, workers=-1, 
                                  updating='deferred', polish=False, disp=False)

    print(f"final param: {opti.x} \nfinal RMSE: {opti.fun}")

#%%

# Fm_mustard = opti.x[0]
# Qeff_mustard = opti.x[1]

# crop_opti = open(path_crop).read()
# crop_opti = crop_opti.replace("@Fm_beet@", str(opti.x[0]))
# crop_opti = crop_opti.replace("@Qeff_beet@", str(opti.x[1]))
# crop_opti = crop_opti.replace("@Fm_faba@", str(opti.x[2]))
# crop_opti = crop_opti.replace("@Qeff_faba@", str(opti.x[3]))
# crop_opti = crop_opti.replace("@Fm_oat@", str(opti.x[4]))
# crop_opti = crop_opti.replace("@Qeff_oat@", str(opti.x[5]))
# crop_opti = crop_opti.replace("@Fm_potato@", str(opti.x[6]))
# crop_opti = crop_opti.replace("@Qeff_potato@", str(opti.x[7]))
# crop_opti = crop_opti.replace("@Fm_mustard@", str(opti.x[8]))
# crop_opti = crop_opti.replace("@Qeff_mustard@", str(opti.x[9]))



# fig, axs = plt.subplots()
# axs.plot(NEE_data.index, NEE_data["NEE"])
# axs.plot(NEE_model.index, NEE_model["NEE Daisy"])
# fig.show()
    
