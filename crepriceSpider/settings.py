# -*- coding: utf-8 -*-

# Scrapy settings for crepriceSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crepriceSpider'

SPIDER_MODULES = ['crepriceSpider.spiders']
NEWSPIDER_MODULE = 'crepriceSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crepriceSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'crepriceSpider.middlewares.crepriceSpiderSpiderMiddleware': 543,
   'crepriceSpider.middlewares.UserAgentmiddleware': 543,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crepriceSpider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
COOKIES_ENABLED = True

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'scrapy_redis.pipelines.RedisPipeline': 300,
   'crepriceSpider.pipelines.MongodbPipeline': 400,
   'crepriceSpider.pipelines.CleanPipeline': 500,
}

MONGODB_SERVER = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = "crepriceSpider"

MONGODB_COLLECTION = "CityPageTest"
MONGODB_COLLECTION_TOWN = "TownPage"
MONGODB_COLLECTION_LIST = "ListPage"

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = True

DOWNLOADER_MIDDLEWARES = {
     'crepriceSpider.middlewares.UserAgentmiddleware': 400,
     'crepriceSpider.middlewares.CookieMiddleware': 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

REDIS_URL = 'redis://root:@127.0.0.1:6379/'
# REDIS_URL = 'redis://root:sa@123@127.0.0.1:6379/'

REDIRECT_ENABLED = False

HTTPERROR_ALLOWED_CODES = [302, 301]

DEPTH_LIMIT = 3
# 使用transCookie.py翻译出的Cookie字典
# COOKIE = {'city': 'hz', '__auc': '7ce7758e15c0fcfebc0053b8e30', '_ga': 'GA1.2.1798936149.1494913902', '__asc': '44929ae015c77563cbea979bbc6', '_gid': 'GA1.2.435672067.1496622492', 'cityredata': 'd19e6299f314d4efb30f1f272d1e2f1c', 'CNZZDATA1253686598': '1609493572-1494913717-%7C1496650051', 'UM_distinctid': '15c0fcfe4452a4-0e4b1acb63848a-1c2d1f03-1fa400-15c0fcfe446d5f', '_gat': '1', 'cityurl': '977a8727891b53c'}
