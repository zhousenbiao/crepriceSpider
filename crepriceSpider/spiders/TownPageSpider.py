# -*- coding:utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from crepriceSpider.items import TownPageLoader
import datetime
from scrapy.http.request import Request
import time
import redis
from crepriceSpider.settings import REDIS_URL

from pymongo import MongoClient

client = MongoClient('mongodb://root:root@127.0.0.1:27017/')
db = client.crepriceSpider

townUrlList = db.CityPageSpider.find({},{"town_url":1,"_id":0 })

import json


''' 镇区页面的房价信息 '''
class TownPageSpider(RedisSpider):
    '''从redis队列中读取url.'''
    name = 'townspider'
    redis_key = 'townspider:start_urls'

    start_urls = []
    i = 0
    for urls in townUrlList:
        python_to_json = json.dumps(urls)
        json_to_python = json.loads(python_to_json)
        i += 1
        print i
        for townlink in json_to_python['town_url']:
            url = "http://www.creprice.cn%s" % (townlink) #http://www.creprice.cn/market/aks/lease/AL/11.html
            print url
            start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            # 休息10秒
            time.sleep(10)
            yield Request(url=url, callback=self.parse)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(TownPageSpider, self).__init__(*args, **kwargs)

    '''将爬取失败的url放入redis,以便重新爬取'''
    def add_url_to_redis(self, url):
        # 镇区的url放入db3
        reds = redis.Redis.from_url(REDIS_URL, db=0, decode_responses=True)
        reds.lpush(self.redis_key, url)

    '''爬取的内容'''
    def parse(self, response):
        el = TownPageLoader(response=response, cookies=response.request.cookies)
        # 如果抓取不成功
        if response.status != 200:
            print ":::ERROR:::" + str(response.url).strip() + " 链接响应错误!!!!!! http状态码为:" + str(response.status).strip()
            time.sleep(10)
            print "将发生错误的链接放入redis进行重试!"
            self.add_url_to_redis(str(response.url).strip())
        else:
            # link
            el.add_value('link', str(response.url).strip())
            # 爬取时间
            el.add_value('crawl_time', datetime.datetime.now())
            web_update = response.xpath('//div[contains(@class, "utitle")]/span[contains(@class, "time")]/text()').extract()
            if web_update == []:
                el.add_value('website_update', 'None')
            else:
                print web_update
                print web_update[0]
                print web_update[0][7:]
                # 网站数据更新时间
                el.add_value('website_update', web_update[0][7:])
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
            qu_name = response.xpath(
                '//div[contains(@class, "area-select")]/span[contains(@class, "city-n")]/a[contains(@class, "hover")]/text()').extract()

            town_name = response.xpath(
                '//div[contains(@class, "area-select")]/span[contains(@class, "city-w")]/a[contains(@class, "hover")]/text()').extract()

            if qu_name==[]:
                # 镇区
                el.add_value('town', town_name[0])
            else:
                el.add_value('town', qu_name[0])

            el.add_value('town_short', short[6])

            el.add_value('house_type', short[5])
            # 用途
            el.add_value('usage', u'住宅')
            # 交易
            if str(response.url).strip().__contains__("forsale"):
                el.add_value('transaction', u'二手房')
            else:
                el.add_value('transaction', u'租金')

            # 近一月房价
            nearly_mouth_average = response.xpath(
                '//div[contains(@class, "price40")]/span[contains(@class, "mr5 num")]/text()').extract()
            if nearly_mouth_average == []:
                el.add_value('nearly_mouth_average', 'None')
            else:
                el.add_value('nearly_mouth_average', nearly_mouth_average[0])

            # 近一个月新增房源
            new_add = response.xpath(
                '//div[contains(@class, "price-l")]/p[contains(@class, "mt")]/span/text()').extract()
            if new_add == []:
                el.add_value('nearly_add', 'None')
            else:
                el.add_value('nearly_add', new_add[0][5:])

            price = response.xpath('//div[contains(@class, "cityprice_sy1 city-price clearfix")]/'
                                   'ul[contains(@class, "price-r")]/li[1]/span/text()').extract()
            # 今日房价
            price_li1 = response.xpath('//div[contains(@class, "cityprice_sy1 city-price clearfix")]/'
                                       'ul[contains(@class, "price-r")]/li[1]/'
                                       'div[contains(@class, "pr-value fl")]/span[1]/text()').extract()
            # 上月房价
            price_li2 = response.xpath('//div[contains(@class, "cityprice_sy1 city-price clearfix")]/'
                                       'ul[contains(@class, "price-r")]/li[2]/'
                                       'div[contains(@class, "pr-value fl")]/span[1]/text()').extract()
            # 预测(未来1月)
            price_li3 = response.xpath('//div[contains(@class, "cityprice_sy1 city-price clearfix")]/'
                                       'ul[contains(@class, "price-r")]/li[3]/span[2]/text()').extract()
            if price[0] == u'今日':
                # 今日
                el.add_value('today_price', price_li1[0])
                # 上月
                el.add_value('last_mouth_price', price_li2[0])
                # 未来
                if price_li3 == []:
                    el.add_value('next_mouth_price', 'None')
                else:
                    el.add_value('next_mouth_price', price_li3[0])
            elif price[0] == u'上月':
                # 今日
                el.add_value('today_price', 'None')
                # 上月
                el.add_value('last_mouth_price', price_li1[0])
                # 未来
                if price_li2 == []:
                    el.add_value('next_mouth_price', 'None')
                else:
                    el.add_value('next_mouth_price', price_li2[0])
            else:
                el.add_value('today_price', 'None')
                el.add_value('last_mouth_price', 'None')
                el.add_value('next_mouth_price', 'None')
            # 近一年的平均单价
            el.add_xpath('nearly_year_average', '//span[contains(@class,"pricedata smwz")]/span[contains(@class,"mr20")]/span/text()')

            return el.load_item()