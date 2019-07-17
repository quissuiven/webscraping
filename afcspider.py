# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 18:02:03 2018

@author: Hong Wen
"""

#Overall Workflow
###############################
#1. Extract all urls from main page, and save in one file
#   > replace all to change to right format
#2. Read text files containing all urls into start_urls
#3. For each url, extract key info 
#   > identify unique element specific to info eg. ul picture img: attr(alt)
#   > for items to store in box, refer to entire var eg. 'Tags': tags
#4. Clean extracted info into desired format
#   > add url to sort

#import os                                                                #set working directory
#os.getcwd()
#os.chdir("C:\\Users\\Hong Wen\\brickset-scraper")

import scrapy
from urllib.parse import urljoin

class afcSpider(scrapy.Spider):
    name = 'afc'
    allowed_domains = ['m.asianfoodchannel.com']
#    start_urls = ['https://m.asianfoodchannel.com/en/lovetocook/martin-yans-asian-favorites/recipes/grilled-lamb-with-wild-betel-leaves','https://m.asianfoodchannel.com/en/lovetocook/family-kitchen-with-sherson/recipes/sambal-serai-quail-egg','https://m.asianfoodchannel.com/en/lovetocook/cooking-for-love/recipes/kari-lamb-shank-with-crispy-potato-strings']
#    start_urls = ['https://m.asianfoodchannel.com/en/lovetocook/family-kitchen-with-sherson/recipes','https://m.asianfoodchannel.com/en/lovetocook/cooking-for-love/recipes','https://m.asianfoodchannel.com/en/lovetocook/martin-yans-asian-favorites/recipes']
    

    f = open("recipes.txt", "r", encoding = "utf-16")                     #Read in file containing all urls. Encoding changes to right format
    start_urls = [url.strip() for url in f.readlines()]
#    print(start_urls[194])
    f.close()
#   
    
    custom_settings = {
       'FEED_URI' : 'afc/recipes.csv'                                    #Save to recipes.csv
    }


    def parse(self, response):                                           #receives request from start_url
        recipeURL = response.url                                         #include URL here to sort data
        recipeName = response.css('ul picture img::attr(alt)').extract()
        photoLink = response.css('ul picture img::attr(src)').extract()       
        tags = response.css('div[class="prepare-info"] ul li span::text').extract()
        ingredients = response.css('.list-item::text').extract()
        method = response.css('ol p::text').extract()
        

        for item in zip(recipeName, photoLink):           
           scraped_info = {
                 'Recipe URL': recipeURL,
                 'Recipe Name' : item[0],
                 'Photo Link' : item[1],
                 'Tags' : tags,                                          #ensures that all tags are extracted in one box
                 'Ingredients' : ingredients,
                 'Method' : method,

           }

           yield scraped_info
           
   
#    def parse(self, response):                                         #extract all urls from main page, and save it one file
#                                                                       
#        recipes = response.css('div[class="title alone"] a::attr(href)').extract()       
#
#        for item in zip(recipes):      
#           scraped_info = {
#                 'recipe' : item[0],
#           }
#
#           yield scraped_info
           
           


#Miscellaneous code
###############################
#   def parse(self, response):
#        recipes = response.xpath("//*[contains(@class, 'col-md-4')]/a/@href").extract()      #extracts url from main page
#        for p in recipes:
#            url = urljoin(response.url, p)
#            yield scrapy.Request(url, callback=self.parse_recipe)                            #for each url, extract corresponding data
#   
#   def parse_recipe(self, response):                                  
#
#        recipeName = response.css('ul picture img::attr(alt)').extract()
#        photoLink = response.css('ul picture img::attr(src)').extract()       
#        tags = response.css('div[class="prepare-info"] ul li span::text').extract()
#        ingredients = response.css('.list-item::text').extract()
#        method = response.css('ol p::text').extract()
#        
#
#        for item in zip(recipeName, photoLink):      
#           scraped_info = {
#                 'Recipe Name' : item[0],
#                 'Photo Link' : item[1],
#                 'Tags' : tags,
#                 'Ingredients' : ingredients,
#                 'Method' : method,
#
#           }
#
#           yield scraped_info 


