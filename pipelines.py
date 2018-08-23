# -*- coding: utf-8 -*-

"""
Created on Thu Jun 7 17:42:05 2018

@author: Qiyao Wei
"""
from scrapy.exceptions import DropItem
import pymongo
import settings

class DuplicatesPipeline(object):

    def __init__(self):
        self.seen = set()  #Sets are fun, so fun

    def process_item(self, item, spider):
        if item['res_link'] in self.seen:  #Duplicates
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.seen.add(item['res_link'])
            return item

class MongoPipeline(object):

    def __init__(self):
        self.mongo_uri = settings.MONGODB_URI
        self.mongo_db = settings.MONGODB_DATABASE

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['dianping_restaurant_sh'].insert_one(dict(item))  #Database collection name
        return item