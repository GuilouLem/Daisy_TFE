# -*- coding: utf-8 -*-
"""
@author: Guillaume Lemaire
guillaume.lemaire@student.uliege.be
+32 496 550 774
"""
import logging
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go 
from pathlib import Path
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


LOGGER = logging.getLogger(__name__)

def bande_crop(axs, name=None):
    flux_periods = {"wheat17": ["2016-10-29", "2017-07-30"],
                    "mustard": ["2017-09-07", "2017-12-07"],
                    "potato": ["2018-04-23", "2018-09-11"],
                    "wheat19": ["2018-10-10", "2019-08-01"], 
                    "faba_oat": ["2019-08-19", "2019-12-03"], 
                    "beet": ["2020-04-01", "2020-11-13"]                            
                    }
    
    color_crop = {"wheat17": "xkcd:light green", 
                  "mustard": "xkcd:light blue",
                  "potato": "xkcd:light yellow",
                  "wheat19": "xkcd:light green",
                  "faba_oat": "xkcd:light pink", 
                  "beet": "xkcd:light orange"          
                  }
    if name is None:
        for per in flux_periods:
            axs.axvspan(flux_periods[per][0], flux_periods[per][1], color=color_crop[per], alpha=0.75)
    
    else:
        crop_periods = flux_periods[name]
        axs.axvspan(crop_periods[0], crop_periods[1], color=color_crop[name], alpha=0.75)
   
    return


class dlf:   
    def __init__(self, name, path, interest_var):
        """
        Initialize the class

        Parameters
        ----------
        name : str
            Name of the result file (include the '.dlf')
        path : _local.WindowsPath
            path source of the result case
        interset_var : list of str
            List with the variables for the graphs


        """
        
        try:
            self.path = os.path.join(path, name)
            self.name = name[:-4]
            self.list_skip = [10, 16]
            self.year = [2017, 2018, 2019, 2020]
            self.pattern = '|'.join(map(str, self.year))
            self.interest = ["year", "month", "mday", "day", "hour"] + interest_var.copy()
                        
            self.harvest = "harvest" in self.name
            self.crop = "crop" in self.name
            self.wheat17 = "wheat_2017" in self.name
            self.mustard = "mustard" in self.name
            self.potato = "potato" in self.name
            self.wheat19 = "wheat_2019" in self.name
            self.faba = "faba" in self.name
            self.oat = "oat" in self.name            
            self.beet = "beet" in self.name
            self.flux = "flux" in self.name
            self.daily = "daily" in self.name
            self.faba_oat = "faba_oat" in self.name
            if self.faba and self.oat:
                self.faba = False
                self.oat = False
            self.soil = any(word in self.name for word in ["trad", "bio"])
            self.bioinc = "bioincorporation" in self.name
            self.entire_year = any(word in self.name for word in ["trad", "bio", "flux"])
            
            if self.soil and "NetPhotosynthesis" in self.interest: 
                self.interest.remove("NetPhotosynthesis")

            self.flux_periods = {"wheat17": ["2016-10-27", "2017-09-07"],
                                 "mustard": ["2017-07-30", "2018-04-23"],
                                 "potato": ["2017-12-07", "2018-10-10"],
                                 "wheat19": ["2018-09-11", "2019-08-09"], 
                                 "faba_oat": ["2019-08-01", "2020-04-01"], 
                                 "beet": ["2019-12-04", "2020-11-15"]                            
                                 }
            
            self.dic_color = {"Soil_C": "Black",
                              "SOM_C": "green",
                              "SMB_C": "blue",
                              "AOM_C": "red",
                              "NetPhotosynthesis": "blue", 
                              "OM_CO2": "darkgoldenrod",
                              "NEE Daisy": "green",
                              "NEE ICOS": "blue",
                              "DS": "orange",
                              "DM tot": "green",
                              "DM épis": "blue",
                              "DM Organe": "blue",
                              "DM oat": "blue",
                              "DM faba": "cyan", 
                              "SOIL_C": "black", 
                              "TOP_C": "green", 
                              "REMOVED_C": "red"
                              }
            
            self.dic_label = {"Soil_C": "[t C/ha]",
                              "SOM_C": "[t C/ha]",
                              "SMB_C": "[t C/ha]",
                              "AOM_C": "[t C/ha]",
                              "NetPhotosynthesis": "NEE [umol CO2/m²/s]", 
                              "OM_CO2": "NEE [umol CO2/m²/s]",
                              "NEE Daisy": "NEE [umol CO2/m²/s]",
                              "NEE ICOS": "NEE [umol CO2/m²/s]",
                              "DS": "[-]",
                              "DM tot": "Biomasse [t/ha]",
                              "DM épis": "Biomasse [t/ha]",
                              "DM Organe": "Biomasse [t/ha]",
                              "DM oat": "Biomasse [t/ha]",
                              "DM faba": "Biomasse [t/ha]",
                              "SOIL_C": "[t C/ha]", 
                              "TOP_C": "[t C/ha]", 
                              "REMOVED_C": "[t C/ha]"
                              }
            
            self.dic_prof = {}
            
            if self.wheat17:
                self.start_date = pd.to_datetime("2016-10-29")
                self.end_date = pd.to_datetime("2017-07-30")
            elif self.mustard:
                self.start_date = pd.to_datetime("2017-09-07")
                self.end_date = pd.to_datetime("2017-12-07")
            elif self.potato:
                self.start_date = pd.to_datetime("2018-04-23")
                self.end_date = pd.to_datetime("2018-09-11")
            elif self.wheat19:
                self.start_date = pd.to_datetime("2018-10-10")
                self.end_date = pd.to_datetime("2019-08-01")
            elif self.faba or self.oat or self.faba_oat:
                self.start_date = pd.to_datetime("2019-08-09")
                self.end_date = pd.to_datetime("2019-12-03")
                self.interest.remove("DS")
            elif self.beet:
                self.start_date = pd.to_datetime("2020-04-01")
                self.end_date = pd.to_datetime("2020-11-13")
            else: 
                self.start_date = pd.to_datetime("2016-10-29")
                self.end_date = pd.to_datetime("2020-11-13")
            
            self.fpath = Path().resolve()
            self.path_icos = str(self.fpath).replace('Code', 'BE_LON')
            
            self.msg = "Init succes"
            self.bln = True
            
        except Exception as e:
            LOGGER.exception(e)
            self.msg = f"__init__ failed: {e}\n"
            self.bln = False
            print(self.msg)                             
            return
        
    def open_dlf(self):
        """
        Open the dlf file
        
        """
        try: 
            skip = 0
            
            with open(self.path, "r") as f:
                for line in f: 
                    if line.strip().startswith("year"):
                        break
                    skip += 1
                    
            self.df = pd.read_csv(self.path, sep="\t", skiprows=skip, header=0)
            self.df = self.df.replace(",", ".", regex=True)
            self.df = self.df.apply(lambda col: pd.to_numeric(col, errors="coerce"))
            
            if self.crop or self.wheat17 or self.mustard or self.potato or self.wheat19 or self.faba or self.oat or self.beet:
                self.df["DM tot"] = self.df["WLeaf"] + self.df["WStem"] + self.df["WSOrg"]
                if self.wheat17 or self.wheat19:
                    self.df["DM épis"] = self.df["WSOrg"]
                elif not self.faba or not self.oat:
                    self.df["DM Organe"] = self.df["WSOrg"]

            if self.flux:
                self.df["NEE Daisy"] = self.df["OM_CO2"] - self.df["NetPhotosynthesis"] 
            if self.daily:
                self.df["NEE Daisy"] = self.df["NEE Daisy"] / 24
                self.df["OM_CO2"] = self.df["OM_CO2"] / 24
                self.df["NetPhotosynthesis"] = self.df["NetPhotosynthesis"] / 24
            
            if self.soil and not self.bioinc:
                self.df["Soil_C"] = self.df["Soil_C"] / 1000
                self.df["SOM_C"] = self.df["SOM_C"] / 1000
                self.df["SMB_C"] = self.df["SMB_C"] / 1000
                self.df["AOM_C"] = self.df["AOM_C"] / 1000
                self.df["Surface_C"] = self.df["Surface_C"] / 1000
            if self.bioinc:
                self.df["SOIL_C"] = self.df["SOIL_C"] / 1000
                self.df["TOP_C"] = self.df["TOP_C"] / 1000
                self.df["REMOVED_C"] = self.df["REMOVED_C"] / 1000
            
            self.df = self.df.filter(items=self.interest)
            self.var = self.df.columns[4:]
            self.units = self.df.iloc[0].tolist()
            self.df = self.df.drop(0)
            
            if not self.harvest:
                self.df["dt"] = pd.to_datetime(dict(year=self.df["year"], month=self.df["month"], day=self.df["mday"], hour=self.df["hour"]))
                self.df = self.df[(self.df["dt"]>=self.start_date) & (self.df["dt"]<=self.end_date)]
                    
            return 
        
        except Exception as e:
            LOGGER.exception(e)
            self.msg = f"open_dlf failed: {e}\n"
            self.bln = False
            print(self.msg)                             
            return
    
    
    def open_ICOS(self):
        """
        Open the ICOS file

        """
        try:
            if self.flux:
                path_icos1 = os.path.join(self.path_icos, "BE-Lon_Results_2014-2019.txt")
                path_icos2 = os.path.join(self.path_icos, "BE-Lon_Results_2020.txt")
                df1 = pd.read_csv(path_icos1, sep="\t", dtype=str)
                df2 = pd.read_csv(path_icos2, sep="\t", dtype=str)
                self.var_icos = df1.columns[4:]
                self.units_icos = df1.iloc[0].tolist()
                df1 = df1.drop(0)
                df2 = df2.drop(0)
                
                self.icos = pd.concat([df1, df2])
                self.icos["NEE"] = self.icos["NEE"].astype(float)
                self.icos["NEE"] = self.icos["NEE"].replace(-9999, np.nan)
                
                form = "%Y-%-m-%d %H:%M:%S"
                date = "Date Time"
            
            elif self.crop or self.wheat17 or self.mustard or self.potato or self.wheat19 or self.beet or self.faba_oat:
                path_icos = os.path.join(self.path_icos, "BE-Lon_vegetation data.xlsx")
                self.icos = pd.read_excel(path_icos)
                    
                
                form = "%Y-%m-%d"
                date = "Date"
    
            
            if hasattr(self, "icos"):
                                
                if self.daily:
                    self.icos[date] = pd.to_datetime(self.icos[date], format=form)
                    self.icos = self.icos.groupby(self.icos[date].dt.date)["NEE"].mean()
                    self.icos = self.icos.to_frame()
                    self.icos = self.icos.reset_index()
                    self.icos["NEE"] = self.icos["NEE"].interpolate(method='linear')
                    
                self.icos[date] = pd.to_datetime(self.icos[date], format=form)                
                self.icos = self.icos[(self.icos[date]>=self.start_date) & (self.icos[date]<=self.end_date)]
                self.datetime = self.icos[date]
                    
                    
            return
    
        except Exception as e:
            LOGGER.exception(e)
            self.msg = f"open_ICOS failed: {e} for the {self.name}\n"
            self.bln = False
            print(self.msg)                             
            return
            
        
    def plot_graph(self):
        """
        Plot the graph of interest variables

        Only if the file isn't an havrest file

        """
        try:
            fig, ax1 = plt.subplots()
            ax2 = None
            
            dt = pd.to_datetime(dict(year=self.df["year"], month=self.df["month"], day=self.df["mday"], hour=self.df["hour"]))

            for v in self.var:
                self.df[v] = self.df[v].astype(float)
                if v in ["DM tot", "DM épis", "DM Organe"]:
                    if ax2 is None:
                        ax2 = ax1.twinx()
                    ax2.plot(dt, self.df[v], label=v, color=self.dic_color[v])
                    ax2.set_ylabel("Biomasse [t/ha]", color="green")
                    ax2.tick_params(axis='y', color="green")
                elif v =="DS":
                    ax1.plot(dt, self.df[v], label=v, color=self.dic_color[v])
                    ax1.set_ylabel("DS [-]", color=self.dic_color[v])
                    ax1.tick_params(axis='y', colors=self.dic_color[v])
                elif v == "REMOVED_C":
                    if ax2 is None:
                        ax2 = ax1.twinx()
                    ax2.plot(dt, self.df[v], label=v, color=self.dic_color[v])
                    ax2.set_ylabel(self.dic_label[v], color=self.dic_color[v])
                    # ax2.tick_params(axis='y', color=self.dic_color[v])
                else:
                    ax1.plot(dt, self.df[v], label=v, color=self.dic_color[v])
                    ax1.set_ylabel(self.dic_label[v])
                                
            ax1.xaxis.set_major_locator(mticker.MaxNLocator(nbins=6)) 
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            
            if self.entire_year:
                bande_crop(ax1)

            ax1.set_xlabel("Date")
            fig.legend(loc="upper left", bbox_to_anchor=[0.13, 0.88], borderaxespad=0.5)
            fig.suptitle(self.name)
            ax1.grid(True)
            
            return
            
        except Exception as e:
            LOGGER.exception(e)
            self.msg = f"plot_graph failed: {e}\n"
            self.bln = False
            print(self.msg)                             
            return
        
        
    def plot_graph_ICOS(self):
        
        try:

            fig, ax1 = plt.subplots()
            ax2 = None

                
            dt = pd.to_datetime(dict(year=self.df["year"], month=self.df["month"], day=self.df["mday"], hour=self.df["hour"]))

            
            for v in self.var:
                self.df[v] = self.df[v].astype(float)
                if v in ["DM tot", "DM épis", "DM Organe"] and not self.faba_oat:
                    if ax2 is None:
                        ax2 = ax1.twinx()
                    ax2.plot(dt, self.df[v], label=v, color=self.dic_color[v])
                elif v =="DS":
                    ax1.plot(dt, self.df[v], label=v, color=self.dic_color[v])
                    ax1.set_ylabel("DS [-]", color=self.dic_color[v])
                    ax1.tick_params(axis='y', colors=self.dic_color[v])
                else:
                    ax1.plot(dt, self.df[v], label=v, color=self.dic_color[v]) 
                    ax1.set_ylabel(self.dic_label[v])

            if self.flux:
                ax1.plot(self.datetime, self.icos["NEE"], label="NEE ICOS")
        
            if self.crop or self.wheat17 or self.mustard or self.potato or self.wheat19 or self.beet:
                ax2.errorbar(self.datetime, self.icos["Total_dry_biomass_avg (t/ha)"], yerr=self.icos["Total_dry_biomass_std (t/ha)"], color="green", fmt="o", capsize=3, label="DM tot (ICOS)")

                if self.wheat17 or self.wheat19:
                    ax2.errorbar(self.datetime, self.icos["Ears/flower/pod/fruits_dry_biomass_avg (t/ha)"], yerr=self.icos["Ears/flower/pod/fruits_dry_biomass_std (t/ha)"], color="blue", fmt="o", capsize=3, label="DM épis (ICOS)")
                ax2.set_ylabel("Biomasse [t/ha]", color="green")
                ax2.tick_params(axis='y', colors="green")
                
                if self.beet or self.potato:
                    ax2.errorbar(self.datetime, self.icos["Total_dry_BGB_avg (t/ha)"], yerr=self.icos["Total_dry_BGB_std (t/ha)"], color="blue", fmt="o", capsize=3, label="DM épis (ICOS)")
                ax2.set_ylabel("Biomasse [t/ha]", color="green")
                ax2.tick_params(axis='y', colors="green")
                
            if self.faba_oat:
                ax1.errorbar(self.datetime, self.icos["Total_dry_biomass_avg (t/ha)"], yerr=self.icos["Total_dry_biomass_std (t/ha)"], color="green", fmt="o", capsize=3, label="DM tot (ICOS)")
                ax1.set_ylabel("Biomasse [t/ha]", color="green")
                ax1.tick_params(axis='y', colors="green")
                
            ax1.xaxis.set_major_locator(mticker.MaxNLocator(nbins=6)) 
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            
            if self.entire_year:
                bande_crop(ax1)

            ax1.set_xlabel("Date")
            fig.legend(loc="upper left", bbox_to_anchor=[0.13, 0.88], borderaxespad=0.5)
            fig.suptitle(self.name)
            ax1.grid(True)
            if ax2 is not None:
                ax2.grid(True)

            return

    
        except Exception as e:
            LOGGER.exception(e)
            self.msg = f"plot_graph_ICOS failed: {e}\n"
            self.bln = False
            print(self.msg)                             
            return
        
        
    def plot_graph_ICOS_periods(self, subplot=True):
        try:
            if len(self.flux_periods) % 2 == 0:
                n_rows = int(len(self.flux_periods)/2)
            else: 
                n_rows = int(((len(self.flux_periods))/2) + 1)
            
            if subplot:
                fig, axs = plt.subplots(nrows=n_rows, ncols=2)
                i = 0
                j = 0
    
                for p in self.flux_periods:
                    if not self.flux:
                        print("Not a flux dataset")
                        break
                    
                    start = pd.to_datetime(self.flux_periods[p][0])
                    end = pd.to_datetime(self.flux_periods[p][1])
                    
                    daisy = self.df[(self.df["dt"]>=start) & (self.df["dt"]<=end)]
                    ICOS = self.icos[(self.icos["Date Time"]>=start) & (self.icos["Date Time"]<=end)]
                    datetime = self.datetime[(self.datetime>=start) & (self.datetime<=end)]
                    
                    
                    axs[i][j].plot(daisy["dt"], daisy["NEE Daisy"], color=self.dic_color["NEE Daisy"], label="NEE Daisy" if i==0 and j==0 else None)
                    axs[i][j].plot(datetime, ICOS["NEE"], color=self.dic_color["NEE ICOS"], label="NEE ICOS" if i==0 and j==0 else None)
                    
                    bande_crop(axs[i][j], name=p)
                    
                    axs[i][j].set_title(p)
                    axs[i][j].xaxis.set_major_locator(mticker.MaxNLocator(nbins=6))  # moins de ticks
                    axs[i][j].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                    axs[i][j].grid(True)
                    
                    if j==0:
                        j = 1
                    else:
                        j = 0
                        i += 1
                        
    
                fig.legend()
                fig.subplots_adjust(hspace=0.4)
                fig.suptitle("Flux par périodes")
                fig.show() 
        
            if not subplot:
                
                for p in self.flux_periods:
                    print(p)
                    if not self.flux:
                        print("Not a flux dataset")
                        break
                    plt.figure()
                    start = pd.to_datetime(self.flux_periods[p][0])
                    end = pd.to_datetime(self.flux_periods[p][1])
                    
                    daisy = self.df[(self.df["dt"]>=start) & (self.df["dt"]<=end)]
                    ICOS = self.icos[(self.icos["Date Time"]>=start) & (self.icos["Date Time"]<=end)]
                    datetime = self.datetime[(self.datetime>=start) & (self.datetime<=end)]
                    
                    
                    plt.plot(daisy["dt"], daisy["NEE Daisy"], color=self.dic_color["NEE Daisy"], label="NEE Daisy")
                    plt.plot(datetime, ICOS["NEE"], color=self.dic_color["NEE ICOS"], label="NEE ICOS")
                    # plt.xaxis.set_major_locator(mticker.MaxNLocator(nbins=6))  # moins de ticks
                    # plt.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                    
                    bande_crop(plt, name=p)
                    plt.grid(True)
    
                    plt.legend()
                    # plt.subplots_adjust(hspace=0.4)
                    plt.title(f"Flux {p}")
                    plt.show() 
                
        except Exception as e:
            LOGGER.exception(e)
            self.msg = f"plot_graph_ICOS_periods failed: {e}\n"
            self.bln = False
            print(self.msg)                             
            return


    def plot_tab(self):
        """
        Create a table of the interste variables 
        
        Only if the file is an harvest file

        """
        try:

            df = self.df.copy()
            
            fig = go.Figure(data= [go.Table(
                header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
                cells=dict(values=[df[col] for col in df.columns],
                fill_color='lavender',
                align='left'))
            ])
            
            fig.show(renderer="browser")
            
            
        except Exception as e: 
            LOGGER.exception(e)
            self.msg = f"plot_tab failed: {e}\n"
            self.bln = False
            print(self.msg)                             
            return
    
        return
        
    def process(self):
        """
        Main function to call to plot daisy result alone 
        
        """
        
        if self.bln:
            self.open_dlf()
            
            
        if self.bln:
            if not self.harvest:
                if self.df.shape[1] > 5:
                    self.plot_graph()
                else:
                    print(f"No intersest var in {self.name}")        
                    return 
                
            # if self.harvest:
            #     self.plot_tab()  
                
        return
    
    def process_comp(self):
        
        if self.bln:
            self.open_dlf()
        
        if self.bln:
            self.open_ICOS()
        
        if self.bln:
            if not self.harvest: 
                if self.df.shape[1] > 5:
                    if hasattr(self, "icos"):
                        self.plot_graph_ICOS()
                    else:
                        print(f"No ICOS data for {self.name}")
                else:
                    print(f"No intersest var in {self.name}")        
                    return 
                    