# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 00:11:49 2022

@author: rohan
"""

#%% imports
import mat73
import matplotlib
from matplotlib import pyplot
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import mne
#from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch

#from mne.preprocessing import ICA
import numpy as np
import pandas as pd
import scipy
from scipy.io import loadmat
from scipy import fft
from scipy.fft import fft, fftfreq, ifft
from scipy.signal import butter, lfilter,filtfilt
import os
import os.path as op
import numpy as np
import pandas as pd
import mne
import h5py

#%%
Subject=[ 'S19']
Condition=['11', '12', '13', '14', '15','16','17', '18','19','21', '22', '23', '24', '25','26','27','28', '29']
#Condition=['11', '12', '13', '14', '15','16','17', '18','19']
#Subject=['S2']
#Condition =['25_1']
plt.close('all')
for sub in Subject:        
    for cond in Condition:
        #LoadRoot= "E:/AffectData/Data/Experiments/" + sub + '/'+sub+'_EEG_'+cond+'.mat'
        LoadRoot= 'D:/PhD Data/Affect/Data/Experiments/' + sub + '/'+sub+'_EEG_'+cond+'.mat'
        with h5py.File(LoadRoot, 'r') as file:
            a = list(file['y'])
        temp=np.transpose(np.array(a))
        
        time=temp[0,:]
        eegdat=temp[1:132,:]
        ref=temp[2,:]
        
        
        #%%
        #COnvert numpy array Enname2 into a list ---
        #Ename2=Ename2.tolist()
        #ch_names=Ename2
        ch_names=['ECG', 'STIM']
        Enum=[129,131]   
        Enum = [x - 1 for x in Enum]
        #Here we subtracted 1 from all the values in Enum because Enum holds exact electrode numbers......
        #......But eegdat is an array so it starts from 0. So, one number less than actual electrode num
        #-------------------------------------------
        eegdat_final=eegdat[Enum,:]
        eegdat=eegdat_final
        #eegdat2=np.concatenate((eegdat,Trig1200.reshape(1,eegdat.shape[1])))
        
        #%% Create the data structure
        sampling_freq=1200
        #ch_names=ch_names.tolist()
        ch_types=['ecg']*1+['stim']*1   #misc are our two reference channels
        info1=mne.create_info(ch_names=ch_names, ch_types=ch_types,sfreq=sampling_freq)  #- this gives error
        # to automatically set momtage ------info1.set_montage('standard_1020')
        print(info1)
        raw=mne.io.RawArray(eegdat,info1) #################################################

        #mne.viz.plot_raw(raw, scalings='auto', duration=10)
        SaveRoot= "D:/PhD Data/Affect/ECG/1-RawData/" + sub +"_"+cond+"_raw.fif"
        raw.save(fname=SaveRoot, overwrite='False')
        print(sub+"_"+cond+" is done")
        #raw.plot(scalings='auto')


