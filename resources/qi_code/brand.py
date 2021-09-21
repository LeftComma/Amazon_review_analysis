# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:13:28 2019

@author: qi.wang
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
trend_data=pd.read_csv('C:/Users/Qi.Wang/Desktop/source/data/bqs_wave_9_10.csv',nrows=2311)
data=trend_data.fillna(0)
data=data.drop([column for column in data.columns if 'bq1_' not in column],axis=1)
toy_sum=data.sum()
