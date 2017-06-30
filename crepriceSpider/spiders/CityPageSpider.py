# -*- coding:utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from crepriceSpider.items import CrepriceCNLoader
# from scrapy import log
import datetime
from selenium import webdriver
from scrapy.http.request import Request
from crepriceSpider.cityID import cityID
import time
import redis
from crepriceSpider.settings import REDIS_URL
from itertools import chain
import requests

from pymongo import MongoClient
# SELECT a,b FROM users WHERE age=33
# db.users.find({age:33}, {a:1,b:1})

client = MongoClient('mongodb://root:root@127.0.0.1:27017/')
db = client.crepriceSpider
cityList = db.Citys.find({},{"shortname":1})

'''城市页面数据爬取'''
class CityPageSpider(RedisSpider):
    '''从redis队列中读取url.'''
    name = 'crespider'
    redis_key = 'crespider:start_urls'

    start_urls = []
    # 二手房和租金
    transaction = ['forsale', 'lease']
    for ID in cityList:
        for tran in transaction:
            url = "http://www.creprice.cn/market/%s/%s/ALL/11.html" % (ID["shortname"], tran)
            start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            # 休息10秒
            time.sleep(10)
            yield Request(url=url, callback=self.parse)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        # self.driver = webdriver.PhantomJS()
        # 每个页面加载时间不能超过60秒
        # self.driver.set_page_load_timeout(60)
        super(CityPageSpider, self).__init__(*args, **kwargs)

    '''将爬取失败的url放入redis,以便重新爬取'''
    def add_url_to_redis(self, url):
        reds = redis.Redis.from_url(REDIS_URL, db=0, decode_responses=True)
        reds.lpush(self.redis_key, url)

    '''获取房价走势和分布的表格数据'''
    def getTableInfo(self, url):
        r = requests.get(url=url)
        tabs = []
        if r.status_code == 200:
            time.sleep(5)
            selector = r.text
            if selector == '':
                return 'None'
            else:
                tables = selector.split('#')[1]
                tab = tables.split('\n')[1:-1]
                tabs.append(tab)
                return tabs

    '''爬取的内容'''
    def parse(self, response):
        el = CrepriceCNLoader(response=response, cookies=response.request.cookies)
        # 如果抓取不成功
        if response.status != 200:
            print ":::ERROR:::" + str(response.url).strip() + " 链接响应错误!!!!!! http状态码为:" + str(response.status).strip()
            time.sleep(10)
            self.add_url_to_redis(str(response.url).strip())

        else:
            # link
            el.add_value('link', str(response.url).strip())
            # 爬取时间
            el.add_value('crawl_time', datetime.datetime.now())

            # 省
            get_province = response.xpath('//div[contains(@class, "newcrumbs")]/a[3]/text()').extract()
            print get_province
            print get_province[0]
            print get_province[0][:-2]
            el.add_value('province', get_province[0][:-2])
            # 城市
            el.add_xpath('city', '//div[contains(@class, "logoBox_header")]/span[contains(@class, "lc_changecity")]/a/text()'.strip())
            # 城市简写字母
            city_short = str(response.url).strip().split('/')[4]
            el.add_value('city_short', city_short)
            # 用途
            el.add_value('usage', u'住宅')

            # 交易
            if str(response.url).strip().__contains__("forsale"):
                el.add_value('transaction', u'二手房')
                el.add_value('house_type', 'forsale')
                # 房价走势
                url_tend = "http://www.creprice.cn/market/chartsdata.html?city=%s&proptype=11&district=&sinceyear=1&flag=1&matchrand=a0b92382&based=price&dtype=line" % city_short
                # 房价分布
                url_dis = "http://www.creprice.cn/market/chartsdata.html?city=%s&proptype=11&district=&sinceyear=1&flag=1&matchrand=a0b92382&based=price&dtype=bar" % city_short
            else:
                el.add_value('transaction', u'租金')
                el.add_value('house_type', 'lease')
                # 房价走势
                url_tend = "http://www.creprice.cn/market/chartsdata.html?city=%s&proptype=11&district=&sinceyear=1&flag=2&matchrand=a0b92382&based=price&dtype=line" % city_short
                # 房价分布
                url_dis = "http://www.creprice.cn/market/chartsdata.html?city=%s&proptype=11&district=&sinceyear=1&flag=2&matchrand=a0b92382&based=price&dtype=bar" % city_short

            tend = self.getTableInfo(url_tend)
            el.add_value('housing_tend', tend)

            distribution = self.getTableInfo(url_dis)
            el.add_value('housing_distribution', distribution)

            info = response.xpath('//div[contains(@class, "tips-sy1 mb5")]')
            print(info)
            data = info[0].xpath('string(.)').extract()[0]
            print(data)
            if data.strip() == u'案例数量不足':
                el.add_value('areas_num', u'案例数量不足')
                el.add_value('realty_transfer', u'案例数量不足')
            else:
                strlist = data.split('|')

                are_num = filter(str.isdigit, strlist[0].encode('gbk'))
                print(filter(str.isdigit, strlist[0].encode('gbk')))

                # realty_trans = strlist[1].split(u'交易')
                if strlist == []:
                    el.add_value('areas_num', 'None')
                    el.add_value('realty_transfer', 'None')
                else:
                    # 楼盘小区个数
                    # el.add_xpath('areas_num', '//div[contains(@class, "tips-sy1 mb5")]/string()'.strip())
                    if are_num == '' and strlist[1][4:] != '':
                        el.add_value('areas_num', 'None')
                        el.add_value('realty_transfer', strlist[1][4:].strip())
                    elif are_num == '' and strlist[1][4:] == '':
                        el.add_value('areas_num', 'None')
                        el.add_value('realty_transfer', 'None')
                    else:
                        el.add_value('areas_num', are_num)
                        # 房产交易 单位:套次
                        el.add_value('realty_transfer', strlist[1][4:].strip())

            web_update = response.xpath('//div[contains(@class, "utitle")]/span[contains(@class, "time")]/text()').extract()
            # -----------------------------
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
                if price_li3==[]:
                    el.add_value('next_mouth_price', 'None')
                else:
                    el.add_value('next_mouth_price', price_li3[0])
            elif price[0] == u'上月':
                # 今日
                el.add_value('today_price', 'None')
                # 上月
                el.add_value('last_mouth_price', price_li1[0])
                # 未来
                if price_li2==[]:
                    el.add_value('next_mouth_price', 'None')
                else:
                    el.add_value('next_mouth_price', price_li2[0])
            else:
                el.add_value('today_price', 'None')
                el.add_value('last_mouth_price', 'None')
                el.add_value('next_mouth_price', 'None')



            # ---------------------------------------------
            if web_update == []:
                el.add_value('website_update', 'None')
                # # 上月房价
                # last_mouth_price = response.xpath('//div[contains(@class, "cityprice_sy1 city-price clearfix")]/'
                #                                   'ul[contains(@class, "price-r")]/li[1]/'
                #                                   'div[contains(@class, "pr-value fl")]/span[1]/text()').extract()
                # el.add_value('last_mouth_price', last_mouth_price[0])
                #
                # # 预测未来一个月价格
                # average = response.xpath(
                #     '//div[contains(@class, "cityprice_sy1 city-price clearfix")]/ul[contains(@class, "price-r")]/li[2]/span[contains(@class, "gray3")]/text()').extract()
            else:
                print web_update
                print web_update[0]
                print web_update[0][7:]
                # 网站数据更新时间
                el.add_value('website_update', web_update[0][7:])

            #     # 上月房价
            #     last_mouth_price = response.xpath('//div[contains(@class, "cityprice_sy1 city-price clearfix")]/'
            #                                       'ul[contains(@class, "price-r")]/li[2]/'
            #                                       'div[contains(@class, "pr-value fl")]/span[1]/text()').extract()
            #     # 预测未来一个月价格
            #     average = response.xpath(
            #         '//div[contains(@class, "cityprice_sy1 city-price clearfix")]/ul[contains(@class, "price-r")]/li[3]/span[contains(@class, "gray3")]/text()').extract()
            #
            #
            # if last_mouth_price == []:
            #     el.add_value('last_mouth_price', 'None')
            # else:
            #     el.add_value('last_mouth_price', last_mouth_price[0])

            # if average != []:
            #     print average[0]
            #     el.add_value('next_mouth_price', average[0])
            # else:
            #     el.add_value('next_mouth_price', 'None')


            # 近一月房价
            nearly_mouth_average = response.xpath('//div[contains(@class, "price40")]/span[contains(@class, "mr5 num")]/text()').extract()
            if nearly_mouth_average == []:
                el.add_value('nearly_mouth_average', 'None')
            else:
                el.add_value('nearly_mouth_average', nearly_mouth_average[0])

            # 新增房源
            new_add = response.xpath('//div[contains(@class, "price-l")]/p[contains(@class, "mt")]/span/text()').extract()
            if new_add == []:
                el.add_value('new_add', 'None')
            else:
                el.add_value('new_add', new_add[0][5:])

            # 近一年均价(平均单价)
            el.add_xpath('average_price', '//div[contains(@class, "menu")]/span[contains(@class, "pricedata smwz")]/span[contains(@class, "mr20")]/span/text()'.strip())


            if tend == '':
                el.add_value('start_days', 'None')
                el.add_value('end_days', 'None')
            else:
                # 统计开始年月,指的是查询当期,近一年统计的最早月份
                start_days = tend[0][0].split(',')[0]
                el.add_value('start_days', start_days)
                # 统计结束年月
                end_days = tend[0][-1].split(',')[0]
                el.add_value('end_days', end_days)

            # 区url
            urls = response.xpath('//div[contains(@class, "area-select")]/span[contains(@class, "city-n")]')
            url_n = []
            if urls:
                for linkn in urls:
                    url_n.append(linkn.xpath('./a/@href').extract())
            # 镇url
            urls_w = response.xpath('//div[contains(@class, "area-select")]/span[contains(@class, "city-w")]')
            url_w = []
            if urls_w:
                for link in urls_w:
                    url_w.append(link.xpath('./a/@href').extract())
            url = url_n + url_w
            # url_n.extend(url_w)
            town_urls = []
            town_urls.append(list(chain(*url)))
            # print(town_urls)
            el.add_value('town_url', town_urls)

            return el.load_item()