# -*- coding:utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from crepriceSpider.items import ListPageLoader
from scrapy.http.request import Request
import time
import redis
from crepriceSpider.settings import REDIS_URL
from itertools import chain
from pymongo import MongoClient

client = MongoClient('mongodb://root:root@127.0.0.1:27017')
db = client.crepriceSpider
cityList = db.Citys.find({},{"shortname":1})

import json

''' 镇区页面的房价信息 '''
class ListSpider(RedisSpider):
    '''从redis队列中读取url.'''
    name = 'listspider'
    redis_key = 'listspider:start_urls'

    start_urls = []
    for ID in cityList:
        url = "http://www.creprice.cn/market/%s/forsale/ALL/11.html" % (ID["shortname"])
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            # 休息10秒
            time.sleep(10)
            yield Request(url=url, callback=self.parse)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(ListSpider, self).__init__(*args, **kwargs)

    '''将爬取失败的url放入redis,以便重新爬取'''
    def add_url_to_redis(self, url):
        reds = redis.Redis.from_url(REDIS_URL, db=0, decode_responses=True)
        reds.lpush(self.redis_key, url)


    '''爬取的内容'''
    def parse(self, response):
        el = ListPageLoader(response=response, cookies=response.request.cookies)
        # 如果抓取不成功
        if response.status != 200:
            print ":::ERROR:::" + str(response.url).strip() + " 链接响应错误!!!!!! http状态码为:" + str(response.status).strip()
            time.sleep(10)
            print "将发生错误的链接放入redis进行重试!"
            self.add_url_to_redis(str(response.url).strip())
        else:
            # link
            el.add_value('link', str(response.url).strip())
            # 省
            get_province = response.xpath('//div[contains(@class, "newcrumbs")]/a[3]/text()').extract()
            print get_province
            print get_province[0]
            print get_province[0][:-2]
            el.add_value('province', get_province[0][:-2])
            short = str(response.url).strip().split('/')
            el.add_value('city_short', short[4])
            # 城市
            el.add_xpath('city', '//div[contains(@class, "logoBox_header")]/span[contains(@class, "lc_changecity")]/a/text()'.strip())

            # 区url
            urls = response.xpath('//div[contains(@class, "area-select")]/span[contains(@class, "city-n")]')
            if urls:
                for linkn in urls:
                    short_name = linkn.xpath('./a/@href').extract()
                    name = linkn.xpath('./a/text()').extract()
                    short_list=[]
                    for short in short_name:
                        short_list.append(short.split('/')[4])
                    dict1 = dict(zip(name, short_list))
                    print dict1
                    el.add_value('district', dict1)
            # 镇url
            urls_w = response.xpath('//div[contains(@class, "area-select")]/span[contains(@class, "city-w")]')
            if urls_w:
                for link in urls_w:
                    short_name = link.xpath('./a/@href').extract()
                    name = link.xpath('./a/text()').extract()
                    short_list=[]
                    for short in short_name:
                        # print short.split('/')[4]
                        short_list.append(short.split('/')[4])
                    dict2 = dict(zip(name, short_list))
                    print dict2
                    el.add_value('town', dict2)

            return el.load_item()