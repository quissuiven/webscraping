# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 18:02:03 2018

@author: Hong Wen
"""

import scrapy
from bs4 import BeautifulSoup
import urllib.request
import requests
from lxml import html

'''
This script takes in a .txt file containing URLs to check through.
The parse function receives the request from start_urls and extracts 'data-origin-img' links from each url.
For each of these image links, the make_soup function would be called to parse the HTML file and test whether the image is broken.
If it is broken, the variable broken_images would increase by 1.
After all the image links are checked, the recipe URL and number of broken images would be stored in a dictionary, which will be output as a CSV file.

To use the script, change the txt file accordingly and run 'scrapy foldername --afcspider2.py' (without single quote).
To improve the speed of the scraper, change variables in custom_settings based on your CPU utilization rate (ideally 80-90%).
'''

class afcSpider2(scrapy.Spider):
    name = 'afc2'
#    start_urls = ['https://www.asianfoodchannel.com/en/categories/japanese']     
    f = open("recipes2.txt", "r", encoding = "utf-16")                   
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    custom_settings = {                                 
       'CONCURRENT_REQUESTS_PER_DOMAIN' : 80,
       'CONCURRENT_REQUESTS' : 150,
       'REACTOR_THREADPOOL_MAXSIZE' : 80, 
       'COOKIES_ENABLED' : False,
       'RETRY_ENABLED' : False,
       'REDIRECT_ENABLED' : False,
       'LOG_ENABLED' : False,
       'LOG_LEVEL' : 'INFO',
       'FEED_URI' : 'afc2/recipes2.csv'  
    }  
            
    def make_soup(self,url):
#            html = urllib.request.urlopen(url).read()
#            parse_only = SoupStrainer("script")
#            return BeautifulSoup(html, 'lxml',parse_only = parse_only)
#            return BeautifulSoup(html, 'html5lib')
            page = requests.get(url)
            return html.fromstring(page.content)
        
    def parse(self, response):                                           #receives request from start_url
            recipeURL = response.url                                         #include URL here to sort data
        
            broken_images = 0 
            
            photoLink = response.css('img::attr(data-origin-img)').extract()   
            
            for each_photo_link in photoLink:  
                    full_link = 'https:' + each_photo_link
                    try:
                        self.make_soup(full_link)                        
                    except:
                        broken_images += 1

                
            yield{
                  'Recipe URL': recipeURL,
                  'broken_images' : broken_images,
            }
                    


    def close(self, reason):  

            starttime = self.crawler.stats.get_value('start_time')
            endtime = self.crawler.stats.get_value('finish_time')
            print("Total run time: " + str(endtime - starttime))

