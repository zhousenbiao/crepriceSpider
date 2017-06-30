# crepriceSpider
中国房价行情平台creprice.cn爬虫，基于scrapy、redis、mongodb进行开发

开发环境：
Ubuntu 16.04.2 LTS 64位
Python 2.7.12

安装pip与setuptools
#sudo apt-get install python-pip -y
#pip install  setuptools
#pip install setuptools --upgrade

安装Scrapy
#pip install Scrapy==1.3.3

安装redis模块
#pip install redis==2.10.5

安装scrapy-redis模块
#pip install scrapy-redis==0.6.8

安装mongodb模块
#pip install pymongo==3.4.0

另外，要先安装好redis和mongodb数据库
启动redis
./redis-server redis.conf
客户端
redis-cli -h 127.0.0.1 -p 6379 -a tdw@123

启动mongodb
./mongod -f mongodb.conf
客户端
./mongo 127.0.0.1:27017/admin -u root -psa123

运行爬虫
scrapy crawl listspider

redis-cli lpush listspider:start_urls "http://www.creprice.cn/market/dg/forsale/ALL/11.html"
