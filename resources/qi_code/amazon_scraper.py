# -*- coding: utf-8 -*-

import urllib.request
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook
import datetime
from urllib.error import  URLError, HTTPError
import time


##this url request stuff can probably be separated into a different module
##tries to reach a page 3 times and returns the error if there is one

def request_url(url,no_tries=3):

    if no_tries == 0:
        print('URL request failed 3 times')
        return None
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            page = response.read()
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

def search_term_from_brand_string(brand_string):
    #for the search url, spaces are replaced with plus symbols
    #search_term_from_brand_string('my little pony')>>>'my+little+pony'
    search_term = brand_string.replace(' ','+')
    return search_term

def build_amz_search_url(search_term, page_no):
    url = ('https://www.amazon.co.uk/s?k={}&i=toys&rh=p_89%3{}{}&dc&page={}&crid=1SDTYPYXM70YV&qid=1561713015&rnid=1632651031&sprefix=my+li%2Ctoys%2C163&ref=sr_pg_{}').format (search_term,'A',search_term,page_no,page_no)
    return url

# build_amz_search_url('my+little+pony',2)

def get_search_page(item,page_no):
    time.sleep(2) #wait 2 seconds before fetching next page
    search_url = build_amz_search_url(item,page_no)
    page = request_url(search_url)
    return page

page=get_search_page('my+little+pony',2)

def get_result_links_from_search_page(page):
    url_list = []
    soup = BeautifulSoup(page, 'html.parser')
    boxes = soup.find_all(class_="s-expand-height s-include-content-margin s-border-bottom")
    for i,item in enumerate(boxes):
        url_list.append('https://www.amazon.co.uk'+item.find(class_="a-link-normal")['href'])
    return url_list

soup = BeautifulSoup(page, 'html.parser')
soup.find_all(class_="s-expand-height s-include-content-margin s-latency-cf-section s-border-bottom")

def build_review_url(url,page_no):
    review_url = url.replace('dp','product-reviews')+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=%s'%(page_no)
    return review_url

def write_url_list_to_csv(url_list,out_path,item):
    with open(out_path, 'w') as f:
        for url in url_list:
            f.write(','.join(item,url))

def get_links_from_brand_list(brand_list, out_path, max_results_pages):
    
    out_df = pd.DataFrame(columns=['item','page','url'])

    #define list of search terms to iterate over
    #I've put these in a csv so you can edit easily
    brand_df = pd.read_csv(brand_list)

    search_term_list = list(brand_df['brands'])

    i=0

    for brand in search_term_list:


        for page_no in list(range(1,max_results_pages)):


            search_term = search_term_from_brand_string(brand)

            search_page = get_search_page(search_term,page_no)

            if search_page==None:
                break

            search_result_links = get_result_links_from_search_page(search_page)
            for link in search_result_links:
                out_df.loc[i] = [brand,page_no,brand]
                i=i+1
    

    out_df.to_csv(out_path)


#define list of search terms to iterate over
#I've put these in a csv so you can edit easily
brand_list_path = 'resources/search_terms.csv'

#define out filepath (to save results to)
out_path = 'out/test.csv'

get_links_from_brand_list(brand_list_path,out_path,2)


