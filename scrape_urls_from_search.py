# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 11:26:16 2021

@author: gabri
"""
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# TODO: Once this fully works, try messing around with how short I can get the search term
# One of the examples uses 'https://www.amazon.com/s?k={search_term}&ref=nb_sb_noss_1'


# Create the url out of the brand string and page
def build_amz_search_url(brand_string, page_no):

    # Replace the spaces in the search term with plus symbols
    search_term = brand_string.replace(' ', '+')

    # And format them into an amazon url
    url = (
        f'https://www.amazon.co.uk/s?k={search_term}&i=toys&rh=p_89%3A{search_term}&dc&page={page_no}&crid=1SDTYPYXM70YV&qid=1561713015&rnid=1632651031&sprefix=my+li%2Ctoys%2C163&ref=sr_pg_{page_no}')

    return url


def extract_product(item, page):  # Extract the details from a single product
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
    # Some items have no rating, if so we want to mark the rating as NA
    try:
        rating = item.i.text.replace('out of 5 stars', '').strip()
    except AttributeError:
        rating = "NA"
        review_count = 0

    result = {'description': description, 'url': url, 'price': price,
              'rating': rating, 'page': page}

    return result


def scrape_searches(brand_string, max_pages, max_results):  # Run the main body of our code
    # Create a bool to tell us whether we've reached our max number of products
    max_hit = False

    # Create an empty list for the products
    products = []

    # Define the custom headers that stop Amazon thinking we're a bot
    headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                'Accept-Language': 'en-US, en;q=0.5'})

    for page in range(1, max_pages):
        print(f'Scraping page {page}')

        # This generates a url using our function
        url = build_amz_search_url(brand_string, page)
        # Test url for product_urls_changed.xlsx is 'https://www.amazon.co.uk/s?k=lego&qid=1633700647&ref=sr_pg_1'

        # This calls the actual page (currently using a custom url)
        time.sleep(2)
        # TODO: Maybe move the requests stuff to it's own function so I can do error handling
        r = requests.get(
            url=url, headers=headers, timeout=2)

        # Create a soup object from the webpage
        soup = BeautifulSoup(r.text, 'lxml')

        # Find all the product objects in the soup object
        results = soup.find_all(
            'div', {'data-component-type': 's-search-result'})

        # Run our details extraction function on each product and add it to our list
        for item in results:
            product = extract_product(item, page)
            products.append(product)

            # Extract the number of products scraped so far
            products_progress = len(products)

            if products_progress % 10 == 0:  # Print the progress every 10 products
                print(f'Scraped {products_progress} products')
            if products_progress >= max_results:  # If we've reached the max number of products, exit the loop
                max_hit = True
                break

        # Exit the loop if the max number of products has been reached
        if max_hit:
            break

    # Convert our list to a pandas df and save it to an excel file
    df = pd.DataFrame(products)
    df.to_excel('product_urls.xlsx', index=False)
    print('Data saved')


# Set our three variables
brand_string = "lego"
max_pages = 6
max_results = 65

# Call our main function
scrape_searches(brand_string, max_pages, max_results)
