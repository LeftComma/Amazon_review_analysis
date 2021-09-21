# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:45:10 2019

@author: qi.wang
"""

import urllib.request
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook
import datetime
from urllib.error import  URLError, HTTPError
import time

def request_url(url,no_tries=3):

    if no_tries == 0:
        print('URL request failed 3 times')
        return None
    try:
        page = urllib.request.urlopen(url)
        print('Request successful:'+url)
        return page

    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        no_tries = no_tries-1
        time.sleep(1)
        request_url(url,no_tries)

    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        no_tries = no_tries-1
        time.sleep(1)
        request_url(url,no_tries)




out_path = 'test.xlsx'


items = ['peppa+pig',' pj+mask','paw+patrol']

links = []
for item in items:
    for page in list(range(1,75)):
        url = ('https://www.amazon.co.uk/s?k={}&i=toys&rh=p_89%3{}{}&dc&page={}&crid=1SDTYPYXM70YV&qid=1561713015&rnid=1632651031&sprefix=my+li%2Ctoys%2C163&ref=sr_pg_{}').format (item,'A',item,page,page)
        page = request_url(url)
        if page == None:
            print('Page is None')
        soup = BeautifulSoup(page, 'html.parser')
        boxes = soup.find_all(class_="s-expand-height s-include-content-margin s-border-bottom")
        for i,item in enumerate(boxes):
            links.append('https://www.amazon.co.uk'+item.find(class_="a-link-normal")['href'])
        time.sleep(20)
    i=0
    for link in links:
        links[i] = link.replace('dp','product-reviews')+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
        i+=1
    file='link_{}.txt'.format(item)
    with open(file, 'w') as f:
        for it in links:
            f.write("%s\n" % it)
