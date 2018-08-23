# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 17:42:05 2018

@author: QiyaoWei
"""
import scrapy
import sys
sys.path.append("..")
from dianping_restaurant_sh.items import DPFoodItem
from dianping_restaurant_sh.settings import CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_PER_DOMAIN
from scrapy.conf import settings

#We need some time to sleep, don't we?
#Should at least work for all major cities in China
class Scrapy(scrapy.Spider):

    name = "dianping_restaurant_sh"
    allowed_domains = ["dianping.com"]
    start_urls = ["http://www.dianping.com/shanghai"] #Start here, not so prone to blocking

    def parse(self, response):
        """
        :param response: start_urls
        :return: yield into restaurant collection page
        """
        u = response.xpath("//ul[@class='cata-hot-detail-item']/li[8]/a/@href").extract()[0] #Enter food page. Why 8? Don't ask me
        #Extract always returns a list
        #If you can't even find this, just start over, error_parse unnecessary
        yield scrapy.Request('http:' + u, callback = self.p)

    def p(self, response):
        """
        :param response: url from parse()
        :return: yield into different cuisine types
        """
        r = response.xpath("//div[@id='classfy']/a")

        for i in r:
            type = i.xpath("span/text()").extract()[0]
            url  = i.xpath("@href").extract()[0]
            yield scrapy.Request(url, callback = self.helper_parse1, dont_filter = True,
                                 meta={'err': 'type_one', 'type': type},
                                 errback = self.error_parse)

    # For getting the maximum number of restaurants. See if you can figure out what I mean
    def helper_parse1(self, response):
        """
        :param response: urls from p()
        :return: yield into corresponding cuisine subtypes (immediately scrape if not missing any restaurants)
        """
        type = response.request.meta['type']
        temp = response.xpath("//div[@class='page']/a/text()").extract()

        if ((len(temp) < 11) or (int(temp[9]) < 50)):
            yield scrapy.Request(response.url, callback = self.help_helper, dont_filter = True,
                                 meta={'err': 'type_four', 'type': type, 'subtype': 'NA', 'region': 'NA', 'subregion':'NA', 'counter': 0},
                                 errback = self.error_parse)
        else:
            r = response.xpath("//div[@id='classfy-sub']/a")
            #Some cuisine types don't even have a subtype
            if len(r) == 0:
                yield scrapy.Request(response.url, callback = self.helper_parse2, dont_filter = True,
                                     meta = {'err': 'type_two', 'type': type, 'subtype': 'NA'},
                                     errback = self.error_parse)
            else:
                for i in r:
                    subtype = i.xpath("span/text()").extract()[0]
                    url     = i.xpath("@href").extract()[0]
                    yield scrapy.Request(url, callback = self.helper_parse2, dont_filter = True,
                                         meta={'err': 'type_two', 'type': type, 'subtype': subtype},
                                         errback = self.error_parse)

    def helper_parse2(self, response):
        """
        :param response: urls from helper_parse1()
        :return: yield into different regions (immediately scrape if not missing any restaurants)
        """
        type    = response.request.meta['type']
        subtype = response.request.meta['subtype']
        temp    = response.xpath("//div[@class='page']/a/text()").extract()

        if ((len(temp) < 11) or (int(temp[9]) < 50)):
            yield scrapy.Request(response.url, callback = self.help_helper, dont_filter = True,
                                 meta={'err': 'type_four', 'type': type, 'subtype': subtype, 'region': 'NA', 'subregion': 'NA', 'counter': 0},
                                 errback = self.error_parse)
        else:
            r = response.xpath("//div[@id='region-nav']/a")
            for i in r:
                region = i.xpath("span/text()").extract()[0]
                url    = i.xpath("@href").extract()[0]
                yield scrapy.Request(url, callback = self.helper_parse3, dont_filter = True,
                                     meta={'err': 'type_three', 'type': type, 'subtype': subtype, 'region': region},
                                     errback = self.error_parse)

    def helper_parse3(self, response):
        """
        :param response: urls from helper_parse2()
        :return: yield into different subregions (immediately scrape if not missing any restaurants)
        """
        type    = response.request.meta['type']
        subtype = response.request.meta['subtype']
        region  = response.request.meta['region']
        temp    = response.xpath("//div[@class='page']/a/text()").extract()

        if ((len(temp) < 11) or (int(temp[9]) < 50)):
            yield scrapy.Request(response.url, callback = self.help_helper, dont_filter = True,
                                 meta={'err': 'type_four', 'type': type, 'subtype': subtype, 'region': region, 'subregion': 'NA', 'counter': 0},
                                 errback = self.error_parse)
        else:
            r = response.xpath("//div[@id='region-nav-sub']/a") #Some day I'll regret not try-excepting this
            for i in r:
                subregion = i.xpath("span/text()").extract()[0]
                url        = i.xpath("@href").extract()[0]
                yield scrapy.Request(url, callback = self.help_helper, dont_filter = True,
                                     meta={'err': 'type_four', 'type': type, 'subtype': subtype, 'region': region, 'subregion': subregion, 'counter': 0},
                                     errback = self.error_parse)

    #I did what I could
    #Actually scraping
    def help_helper(self, response):
        """
        :param response: urls from literally everywhere
        :return: yield items (results of scraping)
        """
        type      = response.request.meta['type']
        subtype   = response.request.meta['subtype']
        region    = response.request.meta['region']
        subregion = response.request.meta['subregion']
        counter   = response.request.meta['counter']

        #Setting CONCURRENT_REQUESTS based on total number of pages in a certain category. Ignorable, honestly
        p = response.xpath("//div[@class='page']/a")
        if len(p) > 5:
            m = p[-2].xpath("text()").extract()[0]
            settings.set(CONCURRENT_REQUESTS, int(m)//5)
            settings.set(CONCURRENT_REQUESTS_PER_DOMAIN, CONCURRENT_REQUESTS)

        r = response.xpath("//div[@class='shop-list J_shop-list shop-all-list']/ul/li")
        for i in r:
            item = DPItem()

            item['res_name'] = i.xpath("div[2]/div[1]/a[1]/h4/text()").extract()[0] if len(
                i.xpath("div[2]/div[1]/a[1]/h4/text()").extract()) > 0 else "N/A"
            item['res_link'] = i.xpath("div[2]/div[1]/a[1]/@href").extract()[0] if len(
                i.xpath("div[2]/div[1]/a[1]/@href").extract()) > 0 else "N/A"

            item['res_stars'] = i.xpath("div[2]/div[2]/span/@title").extract()[0] if len(
                i.xpath("div[2]/div[2]/span/@title").extract()) > 0 else "N/A"
            item['res_num_review'] = i.xpath("div[2]/div[2]/a[1]/b/text()").extract()[0] if len(
                i.xpath("div[2]/div[2]/a[1]/b/text()").extract()) > 0 else "N/A"
            item['res_avg_per'] = i.xpath("div[2]/div[2]/a[2]/b/text()").extract()[0] if len(
                i.xpath("div[2]/div[2]/a[2]/b/text()").extract()) > 0 else "N/A"

            item['res_taste_rank'] = i.xpath("div[2]/span/span[1]/b/text()").extract()[0] if len(
                i.xpath("div[2]/span/span[1]/b/text()").extract()) > 0 else "N/A"
            item['res_envir_rank'] = i.xpath("div[2]/span/span[2]/b/text()").extract()[0] if len(
                i.xpath("div[2]/span/span[2]/b/text()").extract()) > 0 else "N/A"
            item['res_service_rank'] = i.xpath("div[2]/span/span[3]/b/text()").extract()[0] if len(
                i.xpath("div[2]/span/span[3]/b/text()").extract()) > 0 else "N/A"

            item['res_type'] = i.xpath("div[2]/div[3]/a[1]/span/text()").extract()[0] if len(
                i.xpath("div[2]/div[3]/a[1]/span/text()").extract()) > 0 else "N/A"
            item['res_region'] = i.xpath("div[2]/div[3]/a[2]/span/text()").extract()[0] if len(
                i.xpath("div[2]/div[3]/a[2]/span/text()").extract()) > 0 else "N/A"
            item['res_address'] = i.xpath("div[2]/div[3]/span/text()").extract()[0] if len(
                i.xpath("div[2]/div[3]/span/text()").extract()) > 0 else "N/A"

            yield item

        url = response.xpath("//div[@class='page']/a[last()]/@href").extract()
        if len(url) == 0:
            pages = response.xpath("//div[@class='page']/a[last()]/text()").extract()
            if len(pages) == 0 and counter < 3: #Such a great way to prevent blank pages (no content)
                print("Incomplete:   " + response.url)
                counter += 1 #Why do I need a counter? Think!
                yield scrapy.Request(response.url, callback = self.help_helper, dont_filter = True,
                                     meta={'err': 'type_four', 'type': type, 'subtype': subtype, 'region': region, 'subregion': subregion, 'counter': counter},
                                     errback = self.error_parse)
            else:
                if len(pages) != 0:
                    print(type + " + " + subtype + " + " + region + " + " + subregion + ": " + pages[0])
                else:
                    print(type + " + " + subtype + " + " + region + " + " + subregion + ": " + "Not a full page")
        else:
            yield scrapy.Request(url[0], callback = self.help_helper, dont_filter = True,
                                 meta={'err': 'type_four', 'type': type, 'subtype': subtype, 'region': region, 'subregion': subregion, 'counter': 0},
                                 errback = self.error_parse)

    #You know, error_parse() is probably not necessary since I have RETRY turned on, but it's a neat secondary defense
    def error_parse(self, response):
        error_type = response.request.meta['err']

        if error_type == 'type_one':
            print("Error t1:   " + response.request.url)
            type = response.request.meta['type']
            yield scrapy.Request(response.request.url, callback = self.helper_parse1, dont_filter = True,
                                 meta = {'err': error_type, 'type': type},
                                 errback = self.error_parse)
        elif error_type == 'type_two':
            print("Error t2:   " + response.request.url)
            type    = response.request.meta['type']
            subtype = response.request.meta['subtype']
            yield scrapy.Request(response.request.url, callback = self.helper_parse2, dont_filter = True,
                                 meta = {'err': error_type, 'type': type, 'subtype': subtype},
                                 errback = self.error_parse)
        elif error_type == 'type_three':
            print("Error t3:   " + response.request.url)
            type    = response.request.meta['type']
            subtype = response.request.meta['subtype']
            region  = response.request.meta['region']
            yield scrapy.Request(response.request.url, callback = self.helper_parse3, dont_filter = True,
                                 meta = {'err': error_type, 'type': type, 'subtype': subtype, 'region': region},
                                 errback = self.error_parse)
        elif error_type == 'type_four':
            print("Error t4:   " + response.request.url)
            type      = response.request.meta['type']
            subtype   = response.request.meta['subtype']
            region    = response.request.meta['region']
            subregion = response.request.meta['subregion']
            yield scrapy.Request(response.request.url, callback = self.help_helper, dont_filter = True,
                                 meta = {'err': error_type, 'type': type, 'subtype': subtype, 'region': region, 'subregion': subregion, 'counter': 0},
                                 errback = self.error_parse)