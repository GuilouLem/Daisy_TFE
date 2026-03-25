"""
@author: Guillaume Lemaire
guillaume.lemaire@student.uliege.be
+32 496 550 774
"""

import os
from pathlib import Path
from DLF import dlf
import pandas as pd

fpath = Path().resolve()
path_src = os.path.join(fpath, "results", "trad")
path_src = Path(path_src)


list_dlf = [f.name for f in path_src.glob("*.dlf")]



interest_var = [
                "Soil_C", "SOM_C", "SMB_C", "AOM_C", "SOIL_C", "TOP_C", "REMOVED_C", 
                "NetPhotosynthesis", "OM_CO2", "NEE Daisy", 
                "DS", "DM tot","DM épis", "DM Organe", "DM oat", "DM faba"
                ]


if "faba.dlf" in list_dlf:
    faba = dlf("faba.dlf", path_src, interest_var)
    faba.open_dlf()
    oat = dlf("oat.dlf", path_src, interest_var)
    oat.open_dlf()

"Regroupement des fichiers"
def regroup(ob1, ob2):
    name1 = "DM " + ob1.name
    name2 = "DM " + ob2.name
    
    dlf = pd.DataFrame({
        "year": ob1.df["year"],
        "month": ob1.df["month"],
        "mday": ob1.df["mday"],
        "hour": ob1.df["hour"],
        name1: ob1.df["DM tot"],
        name2: ob2.df["DM tot"], 
        "DM tot": (ob1.df["DM tot"] + ob2.df["DM tot"])        
        })
    
    dlf_name = ob1.name + "_" + ob2.name + ".dlf"
    print(dlf)
    dlf.to_csv(os.path.join(path_src, dlf_name), sep="\t",index=False)
    
    if os.path.exists(ob1.path):
        os.remove(ob1.path)
        os.remove(ob2.path)
        list_dlf.remove(ob1.name + ".dlf")
        list_dlf.remove(ob2.name + ".dlf")
        
    list_dlf.append(dlf_name)
    
    print("Regroup function succed")
    return

if os.path.exists(os.path.join(path_src, "faba.dlf")):
    regroup(faba, oat)
    list_dlf = [f.name for f in path_src.glob("*.dlf")]
    
if "crop_prod.dlf" in list_dlf:
    list_dlf.remove("crop_prod.dlf")
#%% Test pour une seule variable 
a = list_dlf[1] 
b = dlf(a, path_src, interest_var)

b.process()



#%% Test pour lecture Daisy de tous les fichiers

for d in list_dlf:
    print(d)
    objet = dlf(d, path_src, interest_var)
    objet.process()

#%%
a = list_dlf[6]
print(a)
b = dlf(a, path_src, interest_var)

b.process_comp()

b.plot_graph_ICOS_periods()


#%% Test pour la lecture et comparaison ICOS 
for d in list_dlf:
    objet = dlf(d, path_src, interest_var)
    objet.process_comp()