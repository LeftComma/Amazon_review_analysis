# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:53:46 2021

@author: gabri
"""
import requests
from bs4 import BeautifulSoup

# WHEN TESTING, REMEMBER TO OPEN THE SEARCH WINDOW IN A PRIVATE BROWSER
# OTHERWISE, YOU WON'T SEE THE SAME THING

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Accept-Language': 'en-GB, en;q=0.5'})


r = requests.get(url = 'https://www.amazon.co.uk/s?k=lego&page=2&qid=1633700699&ref=sr_pg_2', headers = headers, timeout = 1)

soup = BeautifulSoup(r.text, 'lxml')

results = soup.find_all('div', {'data-component-type': 's-search-result'})

# Print how many result we got
print(len(results))
# Save the first one as item
item = results[0]


# Extract the various parts of the item
# Description and url
atag = item.h2.a
description = atag.text.strip()
url = 'https://www.amazon.co.uk' + atag.get('href')

# Price
# An item has no price if it's currently unavailable
price_parent = item.find('span', {'class': 'a-price'})
price = float(price_parent.find('span', {'class': 'a-offscreen'}).text.replace('£', ''))

# Rating and number of reviews
# Some items have no ratings or reviews, if so we want to mark the reviews as 0 and rating as NA
rating = item.i.text.replace('out of 5 stars', '').strip()
review_count = int(item.find('span', {'class': 'a-size-base'}).text)


result = (description, url, price, rating, review_count)

print(result)
