# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 16:15:01 2021

@author: gabri
"""
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

# TODO: Reorganise it so it writes each product to the output file as it goes?

review_list = []

# Get a soup object from a url
def get_soup(url):
    time.sleep(1)
    
    # Having a header helps convince Amazon that we're not a bot
    headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                'Accept-Language': 'en-US, en;q=0.5'})
    
    # Make the request, timeout means it throw an error if it takes longer than 1 sec
    r = requests.get(url = url, headers = headers, timeout = 1)
    
    # Create a soup object, lxml is a fast and lenient HTML parser
    soup = BeautifulSoup(r.text, "lxml")
    
    return soup


def get_reviews(soup):
    # Find all the reviews, identified by their particular tag
    reviews = soup.find_all('div', {'data-hook': 'review'})
    
    # Throwing this in a try statement lets us skip reviews that break our code
    # The key example of these would be reviews in foreign languages
    try:
        for item in reviews:
            # Take the product's title from the overall object
            product = soup.title.text.replace('Amazon.co.uk:Customer reviews:', '').strip()
            
            # Extract each object by identifying it's tags
            title = item.find('a', {'data-hook': 'review-title'}).text.strip()
            rating = float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip())
            body = item.find('span', {'data-hook': 'review-body'}).text.strip()
            
            # Date requires slightly more processing, it returns a longer string of text
            # We can't use replace because that text can change based on country
            date = item.find('span', {'data-hook': 'review-date'}).text.strip()

            # Use regular expressions to extract the date
            date = re.search('[0-9].*$', date).group(0)
            # Convert it to a date type using pandas
            date = pd.to_datetime(date).date()
            
            # Helpfulness also requires more work
            try:
                # First, extract the text and strip it
                helpfulness = item.find('span', {'data-hook': 'helpful-vote-statement'}).text.strip()
                
                # If 1 person found it helpful, that's written as 'One'
                # So we'll search that using regex
                if re.match('One', helpfulness):
                    helpfulness = 1
                
                # If multiple people found it helpful, that's given as a digit
                else:
                    # Remove the unnecessary text and convert to an integer
                    helpfulness = int(helpfulness.replace(' people found this helpful', ''))
            
            # If no one found it helpful, then running the above code throws an error
            except AttributeError:
                helpfulness = 0
            
            review = {'product': product, 'title': title, 'rating': rating, 'helpfulness': helpfulness,
                      'date': date, 'body': body}
            
            review_list.append(review)
    
    # If we can't run our extraction code, just go to the next review
    except:
        pass

# This runs through the x pages of reviews
for x in range(1,10):
    soup = get_soup(f'https://www.amazon.co.uk/product-reviews/B07WD58H6R/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    get_reviews(soup)
    
    # Print to give feedback on the progress
    print(f'Getting page: {x}')
    print(len(review_list))
    
    # This tag is found when the "next page" option is unavailable
    # When that's the case we want to end our search
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

# Convert our list to a df and save it to an excel file
df = pd.DataFrame(review_list)
df.to_excel('product_reviews.xlsx', index=False)
