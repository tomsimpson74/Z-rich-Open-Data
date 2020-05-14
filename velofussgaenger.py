#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:51:03 2020

@author: tsimpson
"""

import datetime 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('2019_verkehrszaehlungen_werte_fussgaenger_velo.csv')
df['VELO_IN']=df['VELO_IN'].fillna(0)
df['VELO_OUT']=df['VELO_OUT'].fillna(0)
df['FUSS_IN']=df['FUSS_IN'].fillna(0)
df['FUSS_OUT']=df['FUSS_OUT'].fillna(0)
df['DATUM']= pd.to_datetime(df['DATUM']) 
df['JUST_DATE'] = df['DATUM'].dt.date


# Add a sum of all traffic variable = (sum of velos in and out and fussgaenger in and out)

Traffic_sum = df['VELO_IN']+df['VELO_OUT']+df['FUSS_IN']+df['FUSS_OUT']
Velo_sum = df['VELO_IN']+df['VELO_OUT']
Fuss_sum = df['FUSS_IN']+df['FUSS_OUT']

df['TRAFFIC_SUM'] = Traffic_sum
df['VELO_SUM'] = Velo_sum
df['FUSS_SUM'] = Fuss_sum


df2 = df.groupby(['JUST_DATE','FK_STANDORT'], as_index=False)[['TRAFFIC_SUM','VELO_SUM','FUSS_SUM']].sum()

    

numLocs = df2['FK_STANDORT'].nunique()

plt.figure(0)
for i in range(numLocs):
    plt.plot(df2.loc[df2['FK_STANDORT']==df2['FK_STANDORT'][i]]['JUST_DATE'],df2.loc[df2['FK_STANDORT']==df2['FK_STANDORT'][i]]['VELO_SUM'])
    
plt.figure(1)
for i in range(numLocs):
    plt.plot(df2.loc[df2['FK_STANDORT']==df2['FK_STANDORT'][i]]['JUST_DATE'],df2.loc[df2['FK_STANDORT']==df2['FK_STANDORT'][i]]['FUSS_SUM'])

## New thin
    
velosday = df2.pivot_table('VELO_SUM', ['JUST_DATE'], 'FK_STANDORT')
#velosday=velosday.dropna(axis=1)
velosday = velosday.fillna(0)
#velosday['JUST_DATE'] = velosday.index
velosday = velosday.rolling(7).mean()

plt.figure(2)
plt.plot(velosday.index,velosday[:],'.')



Fussday = df2.pivot_table('FUSS_SUM', ['JUST_DATE'], 'FK_STANDORT')
#velosday=velosday.dropna(axis=1)
Fussday = Fussday.fillna(0)
#velosday['JUST_DATE'] = velosday.index
Fussday = Fussday.rolling(7).mean()

plt.figure(3)
plt.plot(Fussday.index,Fussday[:],'.')
