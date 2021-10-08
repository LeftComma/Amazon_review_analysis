# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 11:26:16 2021

@author: gabri
"""
import requests
from bs4 import BeautifulSoup

"""
Takes a search term - search term code
Builds a search url - build_amz_search_url function
Extracts the results of the search
Finds all the product links. Stores their urls and generic data
Cycle through a set number of pages of search results
Save it all to a xlsx file
"""

brand_string = "my little pony"

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Accept-Language': 'en-US, en;q=0.5'})


# TODO: Once this fully works, try messing around with how short I can get the search term
# Create an amazon link from the search term 
def build_amz_search_url(brand_string, page_no):
    
    # Replace the spaces in the search term with plus symbols
    search_term = brand_string.replace(' ','+')
    
    # And format them into an amazon url
    url = (f'https://www.amazon.co.uk/s?k={search_term}&i=toys&rh=p_89%3A{search_term}&dc&page={page_no}&crid=1SDTYPYXM70YV&qid=1561713015&rnid=1632651031&sprefix=my+li%2Ctoys%2C163&ref=sr_pg_{page_no}')
    return url

# Extract and return the information from a product
def extract_product(item):
    
    # Description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.co.uk' + atag.get('href')
    
    # Price
    # An item has no price if it's currently unavailable
    try: 
        price_parent = item.find('span', 'a-price')
        price = float(price_parent.find('span' 'a-offscreen').text.replace('£', ''))
    except AttributeError:
        price = "NA"
    
    # Rating and number of reviews
    # Some items have no ratings or reviews, if so we want to mark the reviews as 0 and rating as NA
    try:
        rating = item.i.text.replace('out of 5 stars', '').strip()
        print(rating)
        review_count = int(item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text)
    except AttributeError:
        rating = "NA"
        review_count = 0
    
    result = (description, url, price, rating, review_count)

    return result


url = build_amz_search_url(brand_string, 1)

r = requests.get(url = 'https://www.amazon.co.uk/s?k=lego&qid=1633700647&ref=sr_pg_1', headers = headers, timeout = 1)

soup = BeautifulSoup(r.text, 'lxml')

records = []
results = soup.find_all('div', {'data-component-type': 's-search-result'})

for item in results:
    record = extract_product(item)
    records.append(record)
    
print(records[0])