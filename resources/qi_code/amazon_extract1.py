# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:45:03 2019

@author: qi.wang
"""

import scrapy
 
# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
     
    # Spider name
    name = 'amazon_reviews'
     
    # Domain names to scrape
    allowed_domains = ['amazon.in']
     
    # Base URL for the MacBook air reviews
    myBaseUrl = "https://www.amazon.com/product-reviews/B00EIFS8AC/ref=cm_cr_dp_d_cmps_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="
    start_urls=[]
    
    # Creating list of urls to be scraped by appending page number a the end of base url
    for i in range(1,64):
        start_urls.append(myBaseUrl+str(i))
    
    # Defining a Scrapy parser
    def parse(self, response):
            data = response.css('#cm_cr-review_list')
            date=data.css('.review-date')
            # Collecting product star ratings
            star_rating = data.css('.review-rating')
             
            # Collecting user reviews
            comments = data.css('.review-text')

            count = 0
             
            # Combining the results
            for review in star_rating:
                yield{'date':''.join(date[count].xpath('.//text()').extract()),
                      'stars': ''.join(review.xpath('.//text()').extract()),
                      'comment': ''.join(comments[count].xpath(".//text()").extract())
                     }
                count=count+1

