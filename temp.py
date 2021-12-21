# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 16:15:01 2021

@author: gabri
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

df1 = []

for i in range(4):
    info = {'i': i, '2i': i*2, 'i+1': i+1}
    df1.append(info)

df1 = pd.DataFrame(df1)
print(df1)

df2 = []
for i in range(4):
    new_info = {'i': i, 'constant': 66, '3i': i*3}
    df2.append(new_info)

df2 = pd.DataFrame(df2)
print(df2)

df3 = pd.merge(df1, df2)
print(df3)
