# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 17:19:51 2019

@author: qi.wang
"""

import scrapy
import time
import random
# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
     
    # Spider name
    name = 'amazon_reviews'
    # Domain names to scrape
    allowed_domains = ['amazon.in']
    with open('C:/Users/Qi.Wang/Desktop/source/data/link_pony.txt') as f:
        start_urls=f.readlines()
    # Creating list of urls to be scraped by appending page number a the end of base url
    
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
            next_page=response.css('li.a-last a::attr(href)').get()
            print(next_page)
            if next_page is not None:
                time.sleep(random.randint(20,100))
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse,dont_filter = True)
                
