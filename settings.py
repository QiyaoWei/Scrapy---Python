# -*- coding: utf-8 -*-

"""
Created on Thu Jun 7 17:42:05 2018

@author: Qiyao Wei
"""
BOT_NAME = 'dianping_restaurant_sh' #Required to recognize your bot, but usually by default

SPIDER_MODULES = ['dianping_restaurant_sh.spiders'] #Required to recognize your bot, but usually by default
NEWSPIDER_MODULE = 'dianping_restaurant_sh.spiders' #Required to recognize your bot, but usually by default

COOKIES_ENABLED = False #Don't use cookies unless you have to

#Process some connection errors
RETRY_ENABLED = True
RETRY_HTTP_CODES = [301, 302, 500, 502, 503, 504, 400, 403, 404, 408]
RETRY_TIMES = 1

#CHANGE FILE DESTINATION
#CHANGE FILE DESTINATION
LOG_FILE = '/Users/QiyaoWei/Desktop/f.txt' #Have scrapy's default logging all go into one file
#CHANGE FILE DESTINATION
#CHANGE FILE DESTINATION

#See pipelines.py
ITEM_PIPELINES = {
    'dianping_restaurant_sh.pipelines.MongoPipeline': 301, #Write into Mongodb database. Why 301? Think!
    'dianping_restaurant_sh.pipelines.DuplicatesPipeline': 300 #Filter duplicates
}

#See middlewares.py
DOWNLOADER_MIDDLEWARES = {
    'dianping_restaurant_sh.middlewares.MyHttpProxyMiddleware': 543, #Set proxy and headers authorization
    'dianping_restaurant_sh.middlewares.DemoDownloaderMiddleware': 543 #Default
}
SPIDER_MIDDLEWARES = {
    'dianping_restaurant_sh.middlewares.DemoSpiderMiddleware': 543 #Default
}

#Magic number here
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = CONCURRENT_REQUESTS

#See pipelines.py
MONGODB_IP = '127.0.0.1'
MONGODB_PORT = '27017'
MONGODB_URI = 'mongodb://{}:{}'.format(MONGODB_IP, MONGODB_PORT) #database address, usually default
MONGODB_DATABASE = 'dianping' #database name