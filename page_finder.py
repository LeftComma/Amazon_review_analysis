# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 11:26:16 2021

@author: gabri
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
Takes a search term - search term code
Builds a search url - build_amz_search_url function
Extracts the results of the search - regular code
Finds all the product links. Stores their urls and generic data - extract_product function
Cycle through a set number of pages of search results - TODO
Save it all to a xlsx file - regular code
"""

brand_string = "lego"

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Accept-Language': 'en-US, en;q=0.5'})


# TODO: Once this fully works, try messing around with how short I can get the search term
# Create an amazon link from the search term
def build_amz_search_url(brand_string, page_no):

    # Replace the spaces in the search term with plus symbols
    search_term = brand_string.replace(' ', '+')

    # And format them into an amazon url
    url = (
        f'https://www.amazon.co.uk/s?k={search_term}&i=toys&rh=p_89%3A{search_term}&dc&page={page_no}&crid=1SDTYPYXM70YV&qid=1561713015&rnid=1632651031&sprefix=my+li%2Ctoys%2C163&ref=sr_pg_{page_no}')
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
        price_parent = item.find('span', {'class': 'a-price'})
        price = float(price_parent.find(
            'span', {'class': 'a-offscreen'}).text.replace('£', ''))
    except AttributeError:
        price = "NA"

    # Rating and number of reviews
    # Some items have no ratings or reviews, if so we want to mark the reviews as 0 and rating as NA
    try:
        rating = item.i.text.replace('out of 5 stars', '').strip()
        review_count = int(
            item.find('span', {'class': 'a-size-base'}).text.replace(',', ''))
    except AttributeError:
        rating = "NA"
        review_count = 0
    except ValueError:
        '''
        # Value errors are thrown up because there are multiple things with the class a-size-base in the item
        # Only one of these is the actual number of ratings.
        # I could run this code and then extract the 2nd element, which is the number of ratings
        # However, the original code seems to work almost every time. This code at the stage it's currently at
        # creates more errors. Not totally sure why the original code works most of the time.
        # I'm going to just leave it, as something that can be changed if the errors are too big of a problem
        review_count = item.find_all(
            'span', {'class': 'a-size-base'})
        print(review_count)
        print(type(review_count))'''
        review_count = "Error"

    result = (description, url, price, rating, review_count)

    return result


# This generates a url using our function
url = build_amz_search_url(brand_string, 1)

# This calls the actual page (currently using a custom url)
r = requests.get(
    url=url, headers=headers, timeout=1)
# Test url for product_urls_changed.xlsx is 'https://www.amazon.co.uk/s?k=lego&qid=1633700647&ref=sr_pg_1'

# Create a soup object from the webpage
soup = BeautifulSoup(r.text, 'lxml')

# Create an empty list for the products
products = []

# Find all the product objects in the soup object
results = soup.find_all('div', {'data-component-type': 's-search-result'})

# Run our details extraction function on each product and add it to our list
for item in results:
    product = extract_product(item)
    products.append(product)

print(url)

# Convert our list to a pandas df and save it to an excel file
df = pd.DataFrame(products)
df.columns = ['name', 'url', 'price', 'rating', 'num_of_ratings']
df.to_excel('product_urls.xlsx', index=False)
