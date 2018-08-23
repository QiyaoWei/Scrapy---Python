# -*- coding: utf-8 -*-

"""
Created on Thu Jun 7 17:42:05 2018

@author: Qiyao Wei
"""
import scrapy

class DPFoodItem(scrapy.Item):
    #All the things we want to save while scraping
    res_name             = scrapy.Field()
    res_link             = scrapy.Field()
    res_stars            = scrapy.Field()
    res_num_review       = scrapy.Field()
    res_avg_per          = scrapy.Field()
    res_taste_rank       = scrapy.Field()
    res_envir_rank       = scrapy.Field()
    res_service_rank     = scrapy.Field()
    res_type             = scrapy.Field()
    res_region           = scrapy.Field()
    res_address          = scrapy.Field()