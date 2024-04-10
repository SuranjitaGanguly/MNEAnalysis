# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 19:31:37 2024

@author: suran
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

ep1=[12,25,50,62,75,100,112,125,150,162,175,200 ]   # This is where we have to input the number of epochs
#
Subject=['S1', 'S2','S3', 'S4', 'S5','S6', 'S7','S8', 'S9','S10','S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19']
Condition =["Index_S1", "Index_S2", "Index_S3",
            "Arm_S1", "Arm_S2", "Arm_S3",
            "Toe_S1", "Toe_S2", "Toe_S3",
            "Leg_S1", "Leg_S2", "Leg_S3",
            "Back_S1","Back_S2", "Back_S3",
            "Stomach_S1", "Stomach_S2", "Stomach_S3" ]#,

#parameters
lomb_peak_vlf=[]
lomb_peak_lf=[]
lomb_peak_hf=[]
lomb_abs_vlf=[]
lomb_abs_lf=[]
lomb_abs_hf=[]
lomb_rel_vlf=[]
lomb_rel_lf=[]
lomb_rel_hf=[]
lomb_log_vlf=[]
lomb_log_lf=[]
lomb_log_hf=[]
lomb_ratio=[]
lomb_total=[]

fft_peak_vlf=[]
fft_peak_lf=[]
fft_peak_hf=[]
fft_abs_vlf=[]
fft_abs_lf=[]
fft_abs_hf=[]
fft_rel_vlf=[]
fft_rel_lf=[]
fft_rel_hf=[]
fft_log_vlf=[]
fft_log_lf=[]
fft_log_hf=[]
fft_ratio=[]
fft_total=[]
Valence=[]
Arousal=[]
Subject1=[]
Stim=[]
Loc=[]
epname=[]

rating = pd.read_excel (r'D:\PhD Data\Affect\SubjectRatings.xlsx', sheet_name='Both')

for sub in Subject:
    for cond in Condition:
        for ep in ep1:
            try:
                    plt.close('all')
                    print("reading "+sub+"and condition "+cond)
                    rpeaks = np.asarray(pd.read_csv("D:/PhD Data/Affect/ECG/2-RPeaks_renamed/ECG_"+sub+"_"+cond+".csv")["0"])
                    print (sub+"_"+cond)
                    rpeaks=rpeaks/1200
                    
                    
                    
                    ''' extract the rpeaks only pertaining to the epochs'''
                    if cond[-1:]=='3':
                        eptime=1.05
                        nff=256
                    else:
                        eptime=2.5
                        nff=int((2.5/1.05)*256)
                    
                    rp=[]
                    for i in rpeaks: 
                        if i<101:
                            if i>(ep-20)*eptime and i<ep*eptime: #This loop says: if ep is 50, take ep between 25 and 50. Applies for all epochs. #Basically takes chunks of 25
                                rp.append(i)
                        else:
                            if i>10+((ep-20)*eptime) and i<10+(ep*eptime): #Added 10 seconds of rating time
                                rp.append(i)
                     
                    rpeaks=rp       
                    ''' omit this whole section if you want normal rpeaks throughout the time duration'''
                    
                    
                    
                    
                    if rpeaks!=[]:
                        rpeaks = list(dict.fromkeys(rpeaks))  # there are sometimes duplicate values -- I am removing those here
                
                        #nni = tools.nn_intervals(rpeaks)
                        #sometimes there were duplicates present in the rpeaks. That needs to be removed
                        result = fd.lomb_psd(rpeaks=rpeaks, nfft=nff)
                        result1 = fd.welch_psd(rpeaks=rpeaks, nfft=nff)
                    else:
                        result=np.nan
                        result1=np.nan
                    
                    '''
                    #If we want to compute using vustom freq bands
                    # Define custom frequency bands and add the ULF band
                    fbands = {'ulf': (0.0, 0.1), 'vlf': (0.1, 0.2), 'lf': (0.2, 0.3), 'hf': (0.3, 0.4)}
                    
                    # Compute the PSD with custom frequency bands
                    result = fd.lomb_psd(nni, fbands=fbands)
                    '''
                    
                    '''
                    for key in result1.keys():
                       print(key, result1[key])
                    '''   
                    try:
                        
                        lomb_peak_vlf.append(result['lomb_peak'][0])
                        lomb_peak_lf.append(result['lomb_peak'][1])
                        lomb_peak_hf.append(result['lomb_peak'][2])
                        
                        lomb_abs_vlf.append(result['lomb_abs'][0])
                        lomb_abs_lf.append(result['lomb_abs'][1])
                        lomb_abs_hf.append(result['lomb_abs'][2])
                        
                        lomb_rel_vlf.append(result['lomb_rel'][0])
                        lomb_rel_lf.append(result['lomb_rel'][1])
                        lomb_rel_hf.append(result['lomb_rel'][2])
                        
                        lomb_log_vlf.append(result['lomb_log'][0])
                        lomb_log_lf.append(result['lomb_log'][1])
                        lomb_log_hf.append(result['lomb_log'][2])
                        
                        lomb_ratio.append(result['lomb_ratio'])   
                        lomb_total.append(result['lomb_total'])
                        
                           
                    except:
                        lomb_peak_vlf.append(np.nan)
                        lomb_peak_lf.append(np.nan)
                        lomb_peak_hf.append(np.nan)
                        
                        lomb_abs_vlf.append(np.nan)
                        lomb_abs_lf.append(np.nan)
                        lomb_abs_hf.append(np.nan)
                        
                        lomb_rel_vlf.append(np.nan)
                        lomb_rel_lf.append(np.nan)
                        lomb_rel_hf.append(np.nan)
                        
                        lomb_log_vlf.append(np.nan)
                        lomb_log_lf.append(np.nan)
                        lomb_log_hf.append(np.nan)
                        
                        lomb_ratio.append(np.nan)   
                        lomb_total.append(np.nan)
                        
                    try:
                        fft_peak_vlf.append(result1['fft_peak'][0])
                        fft_peak_lf.append(result1['fft_peak'][1])
                        fft_peak_hf.append(result1['fft_peak'][2])
                        
                        fft_abs_vlf.append(result1['fft_abs'][0])
                        fft_abs_lf.append(result1['fft_abs'][1])
                        fft_abs_hf.append(result1['fft_abs'][2])
                        
                        fft_rel_vlf.append(result1['fft_rel'][0])
                        fft_rel_lf.append(result1['fft_rel'][1])
                        fft_rel_hf.append(result1['fft_rel'][2])
                        
                        fft_log_vlf.append(result1['fft_log'][0])
                        fft_log_lf.append(result1['fft_log'][1])
                        fft_log_hf.append(result1['fft_log'][2])
                        
                        fft_ratio.append(result1['fft_ratio'])   
                        fft_total.append(result1['fft_total'])
                       
                    except:
                                                          
                        
                        fft_peak_vlf.append(np.nan)
                        fft_peak_lf.append(np.nan)
                        fft_peak_hf.append(np.nan)
                        
                        fft_abs_vlf.append(np.nan)
                        fft_abs_lf.append(np.nan)
                        fft_abs_hf.append(np.nan)
                        
                        fft_rel_vlf.append(np.nan)
                        fft_rel_lf.append(np.nan)
                        fft_rel_hf.append(np.nan)
                        
                        fft_log_vlf.append(np.nan)
                        fft_log_lf.append(np.nan)
                        fft_log_hf.append(np.nan)
                        
                        fft_ratio.append(np.nan)   
                        fft_total.append(np.nan)
                        
                        
                        
                    epname.append("ep"+str(ep))                                              
                    df = rating.loc[rating['Subject'] == sub]
                    V_mean=np.mean(df[cond+"_V"])
                    A_mean=np.mean(df[cond+"_A"])
                    Valence.append(V_mean)
                    Arousal.append(A_mean)
                    Subject1.append(sub)
                    Stim.append(cond[-2:])
                    Loc.append(cond[:-3])
        
            
            except OSError:
                # This is to skip missing files and continue with the loop
                continue
        
        
headers=['Subject', 'Stim', 'Loc', 'Valence', 'Arousal','Epochs','lomb_peak_vlf','lomb_peak_lf','lomb_peak_hf','lomb_abs_vlf','lomb_abs_lf','lomb_abs_hf','lomb_rel_vlf','lomb_rel_lf','lomb_rel_hf','lomb_log_vlf','lomb_log_lf','lomb_log_hf','lomb_ratio','lomb_total',
         'welch_peak_vlf','welch_peak_lf','welch_peak_hf','welch_abs_vlf','welch_abs_lf','welch_abs_hf','welch_rel_vlf','welch_rel_lf','welch_rel_hf','welch_log_vlf','welch_log_lf','welch_log_hf','welch_ratio','welch_total'] 

df1=pd.DataFrame(columns=headers)
df1['Subject']=Subject1
df1['Stim']=Stim
df1['Loc']=Loc
df1['Valence']=Valence
df1['Arousal']=Arousal
df1['Epochs']=epname
df1['lomb_peak_vlf']=lomb_peak_vlf
df1['lomb_peak_lf']=lomb_peak_lf
df1['lomb_peak_hf']=lomb_peak_hf
df1['lomb_abs_vlf']=lomb_abs_vlf
df1['lomb_abs_lf']=lomb_abs_lf
df1['lomb_abs_hf']=lomb_abs_hf
df1['lomb_rel_vlf']=lomb_rel_vlf
df1['lomb_rel_lf']=lomb_rel_lf
df1['lomb_rel_hf']=lomb_rel_hf
df1['lomb_log_vlf']=lomb_log_vlf
df1['lomb_log_lf']=lomb_log_lf
df1['lomb_log_hf']=lomb_log_hf
df1['lomb_ratio']=lomb_ratio
df1['lomb_total']=lomb_total


#df1=pd.DataFrame(columns=headers)
df1['welch_peak_vlf']=fft_peak_vlf
df1['welch_peak_lf']=fft_peak_lf
df1['welch_peak_hf']=fft_peak_hf
df1['welch_abs_vlf']=fft_abs_vlf
df1['welch_abs_lf']=fft_abs_lf
df1['welch_abs_hf']=fft_abs_hf
df1['welch_rel_vlf']=fft_rel_vlf
df1['welch_rel_lf']=fft_rel_lf
df1['welch_rel_hf']=fft_rel_hf
df1['welch_log_vlf']=fft_log_vlf
df1['welch_log_lf']=fft_log_lf
df1['welch_log_hf']=fft_log_hf
df1['welch_ratio']=fft_ratio
df1['welch_total']=fft_total


#%%
df1.to_csv("D:/ECGMetrics_Separatedepochs_higherRes_SimilarFreqBins_trial"+".csv", sep=',', index=False, encoding='utf-8')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
