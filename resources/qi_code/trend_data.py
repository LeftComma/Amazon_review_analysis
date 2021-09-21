# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:42:17 2019

@author: qi.wang
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
trend_data=pd.read_csv('C:/Users/Qi.Wang/Desktop/source/data/bqs_wave_9_10.csv',nrows=2311)

#total trend for toys
pre_data=trend_data.fillna(0)
data=pre_data.copy()
data=data.drop([column for column in data.columns if 'bq1_' not in column],axis=1)
sum_=pd.DataFrame(data.sum(),columns=['sum'])
order=sum_.sort_values(by='sum',ascending=False)
top_toys=order[:20]
group_data = list(top_toys['sum'])
group_names = list(top_toys.index)
fig,ax=plt.subplots()
ax.barh(group_names,group_data)

#trend for 9 and 10
data_9=pre_data.copy()
data_9=data_9.loc[data_9['trends_wave']==9]
data_9=data_9.drop([column for column in data_9.columns if 'bq1_' not in column],axis=1)
sum_9=pd.DataFrame(data_9.sum(),columns=['sum_9'])
order_9=sum_9.sort_values(by='sum_9',ascending=False)
top_toys_9=order_9[:20]
group_data_9 = list(top_toys_9['sum_9'])
group_names_9 = list(top_toys_9.index)

data_10=pre_data.copy()
data_10=data_10.loc[data_10['trends_wave']==10]
data_10=data_10.drop([column for column in data_10.columns if 'bq1_' not in column],axis=1)
sum_10=pd.DataFrame(data_10.sum(),columns=['sum'])
order_10=sum_10.sort_values(by='sum',ascending=False)
top_toys_10=order_10[:20]
group_data_10= list(top_toys_10['sum'])
group_names_10 = list(top_toys_10.index)

sum_9_10=sum_9.copy()
sum_9_10['sum_10']=sum_10['sum']
order_trends=sum_9_10.sort_values(by='sum_9',ascending=False)
feature_interest=order_trends[:20]

fig,ax=plt.subplots()
ax.errorbar(feature_interest.index,feature_interest['sum_9'],label='trends_9')
ax.errorbar(feature_interest.index,feature_interest['sum_10'],label='trends_10')


fig1,ax1=plt.subplots()
ax1.barh(group_names_9,group_data_9)

fig2,ax2=plt.subplots()
ax2.barh(group_names_10,group_data_10)

#group by age
age_group_number=trend_data.groupby('child_age_group').count()
age_group_number=age_group_number['unique_pid']

age_gender_group_number=trend_data.groupby(['child_age_group','child_gender']).count()
age_gender_group_number=age_gender_group_number['unique_pid']

#lego trend
data_lego=pre_data.copy()
data_lego=pre_data.drop([column for column in data_lego.columns if 'bq1_lego' not in column],axis=1)
data_lego['child_age_group']=pre_data['child_age_group']
lego_trend_set_kit=data_lego.groupby(['child_age_group','bq1_lego_blocks_set_kit']).count()[['bq1_lego_city']]
lego_trend_set_kit=lego_trend_set_kit.rename(index=str,columns={'bq1_lego_city':'lego_blocks_set_kit'})
lego_trend_lego_city=data_lego.groupby(['child_age_group','bq1_lego_friends']).count()
