# -*- coding: utf-8 -*-

"""
Created on Fri Jun  8 10:11:02 2018

@author: QiyaoWei
"""
#Obviously what you should run is this file
#Easier than running scrapy from command line directly
from scrapy import cmdline
cmdline.execute("scrapy crawl dianping_restaurant_sh".split())