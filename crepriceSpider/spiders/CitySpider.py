# -*- coding:utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from crepriceSpider.items import CrepricecnItem
# import re

class CitySpider(Spider):
    name = "citySpider"
    allowed_domains = ['creprice.cn', '127.0.1.1:8000']
    start_urls = [
        # 本地服务器测试
        "http://127.0.1.1:8000/",
    ]

    cookies = {}

    # 发送给服务器的http头信息,有的网站需要伪装出浏览器头进行爬取
    headers = {
        # 'Cpnnection':'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def parse(self, response):
        infos = Selector(response).xpath('//div[@class="change_city"]/ul/li[@class="clearfix"]/div[@class="citylistbox"]/span')
        for info in infos:
            item = CrepricecnItem()

            item['city'] = info.xpath('.//a/@title').extract_first()
            item['citylink'] = info.xpath('.//a/@href').extract_first()
            item['shortname'] = item['citylink'] .split('/',3)[2]

            yield item

