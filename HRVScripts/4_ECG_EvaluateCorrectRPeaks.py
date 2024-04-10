# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:25:57 2024

@author: suran
"""

import pyhrv 
import mne
import numpy as np
import biosppy
import numpy as np
import pyhrv.tools as tools
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os 
import biosppy
import pyhrv.frequency_domain as fd
from biosppy.signals import ecg
import csv
#import mplcursors
#%%
Subject=['S15']#, 'S2','S3', 'S4', 'S5','S6', 'S7','S8', 'S9','S10','S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19']

Condition=['11', '12', '13', '14', '15','16','17', '18','19','21', '22', '23', '24', '25','26','27','28', '29']


LoadRoot =  "D:/PhD Data/Affect/ECG/1-RawData/"
LoadFile=[]
for sub in Subject:
    for cond in Condition:
        #%%
        try:
            raw=mne.io.read_raw_fif("D:/PhD Data/Affect/ECG/1-RawData/" + sub +"_"+cond+"_raw.fif", preload=True)
            picks=mne.pick_types(raw.copy().info,ecg=True, stim=True)
            #picks.plot(scaling='auto')
            filt_raw=raw.copy().filter(l_freq=1,h_freq=40,method='iir',iir_params=dict(order=6,ftype='butter'),picks=picks) #remove slow drifts
            filt_raw2=filt_raw.notch_filter(freqs=[np.arange(50,200,50)], picks=picks)
            raw=filt_raw2
            rpeaks = np.asarray(pd.read_csv("D:/PhD Data/Affect/ECG/2-RPeaks/ECG_"+sub+"_"+cond+".csv")["0"])
            
                
            #%%
            timlen=round(len(raw.times)/5)
            
            for rounds in np.arange(1,6,1):
                    rpeaks_temp=[]
                    for i in rpeaks:
                        if i>(rounds-1)*timlen and i<rounds*timlen:
                            rpeaks_temp=np.append(rpeaks_temp,int((i)))
                          
                    amplitude=[]
                    for i in rpeaks_temp:
                        amplitude=np.append(amplitude,raw._data[0][int(i)])
                    plt.figure().set_figwidth(15)     
                    plt.plot(rpeaks_temp/1200,amplitude, "*")
                    plt.plot(raw.times[(rounds-1)*timlen:rounds*timlen],raw._data[0][(rounds-1)*timlen:rounds*timlen])
                    plt.savefig("D:/PhD Data/Affect/ECG/2-RPeaks_Plots/"+sub+"_"+cond+"_"+str(rounds)+".jpg", dpi=600)
                    plt.close("all")
        except:
            continue
        
        
        
        
        