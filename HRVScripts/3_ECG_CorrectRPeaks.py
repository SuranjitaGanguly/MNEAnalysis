# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:43:11 2024

@author: suran
This contains helper functions to add or omit particular r peaks
Just plot the data, find out the x coordinates (i.e. time point) of the r peak
either remove it or insert it
See the sections--->
-to find and remove a sample from rpeaks
-to add a sample in the r peak
"""
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

def removePoint(timept, sub, cond):
    
    # Change this based on the time point you find out

    rpeaks = np.asarray(pd.read_csv("D:/PhD Data/Affect/ECG/2-RPeaks/ECG_"+sub+"_"+cond+".csv")["0"])
    sample = timept*1200
    temp=abs(rpeaks-sample)
    indx=np.argmin(temp)

    rpeaks=rpeaks.tolist()
    rpeaks.pop(indx)
    rpeaks=np.asarray(rpeaks)
          
    amplitude=[]
    for i in rpeaks:
        amplitude=np.append(amplitude,raw._data[0][int(i)])
        
    '''
    plt.figure().set_figwidth(15)     
    plt.plot(rpeaks/1200,amplitude, "*")
    plt.plot(raw.times,raw._data[0])
    '''
    #
    rpeaks =  pd.DataFrame(rpeaks)
    rpeaks.to_csv("D:/PhD Data/Affect/ECG/2-RPeaks/ECG_"+sub+"_"+cond+".csv")

    '''
    plt.figure().set_figwidth(15)     
    plt.plot(rpeaks/1200,amplitude, "*")
    plt.plot(raw.times,raw._data[0])
    plt.close('all')
    '''
    #
    return


def addPoint(timept, sub, cond):
    
    rpeaks = np.asarray(pd.read_csv("D:/PhD Data/Affect/ECG/2-RPeaks/ECG_"+sub+"_"+cond+".csv")["0"])
    sample = round(timept*1200)
    temp=rpeaks-sample
    temp[temp < 0] = 0
    indx=np.argmin(temp)
    
    rpeaks=rpeaks.tolist()
    rpeaks.insert(indx-1, sample)
    rpeaks=np.asarray(rpeaks)
    
    amplitude=[]
    for i in rpeaks:
        amplitude=np.append(amplitude,raw._data[0][int(i)])
    
    
    plt.figure().set_figwidth(15)     
    plt.plot(rpeaks/1200,amplitude, "*")
    plt.plot(raw.times,raw._data[0])
    
    rpeaks =  pd.DataFrame(rpeaks)
    rpeaks.to_csv("D:/PhD Data/Affect/ECG/2-RPeaks/ECG_"+sub+"_"+cond+".csv")

    return
#  CHANGE THESE PARAMETERS FOR A PROPER VIEW!!!!!
'''

this is where your code starts!

'''
plt.close("all")
sub="S15"  # s15 - 16 horribly noisy havent done yet onwards
cond="16"#"22"
tmin=215
tmax=tmin+20
#plot this
raw=mne.io.read_raw_fif("D:/PhD Data/Affect/ECG/1-RawData/" + sub +"_"+cond+"_raw.fif", preload=True)
picks=mne.pick_types(raw.copy().info,ecg=True, stim=True)
#picks.plot(scaling='auto')
filt_raw=raw.copy().filter(l_freq=1,h_freq=40,method='iir',iir_params=dict(order=6,ftype='butter'),picks=picks) #remove slow drifts
filt_raw2=filt_raw.notch_filter(freqs=[np.arange(50,200,50)], picks=picks)
raw=filt_raw2

rpeaks = np.asarray(pd.read_csv("D:/PhD Data/Affect/ECG/2-RPeaks/ECG_"+sub+"_"+cond+".csv")["0"])
#rpeaks = np.asarray(pd.read_csv("C:/Users/suran/OneDrive - IIT Hyderabad/Desktop/Manuscripts/Affect_HRV/INI/INI/RPeaks/"+sub+cond+".csv")["0"])


rpeaks_temp=[]
for i in rpeaks:
    if i>tmin*1200 and i<tmax*1200:
        rpeaks_temp=np.append(rpeaks_temp,int((i)))

        
amplitude=[]
for i in rpeaks_temp:
    amplitude=np.append(amplitude,raw._data[0][int(i)])
    
    
    
plt.figure().set_figwidth(15)     
plt.plot(rpeaks_temp/1200,amplitude, "*")
plt.plot(raw.times[tmin*1200:tmax*1200],raw._data[0][tmin*1200:tmax*1200])


#%% to find an remove a sample from rpeaks
timept= 216.63
removePoint(timept, sub, cond)


#%% to add a sample in the r peak
timept= 213.92
addPoint(timept, sub, cond)


