# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class CleanPipeline(object):

    def __init__(self):
        self.has = set()

    def process_item(self, item, spider):
        print "------"
        if item.keys() >= 5:
            if item in self.has:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.has.add(item)
                return item

# mongodb存储
class MongodbPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )

        # connection = pymongo.MongoClient('mongodb://root:root@127.0.0.1:27017/')
        db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION_TOWN']]
        self.collection = db[settings['MONGODB_COLLECTION_LIST']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing{0}!'.format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg('成功添加信息!', level=log.DEBUG, spider=spider)

        return item

    # def testdb(self):
    #     # 网络上MongoHQ
    #     con = pymongo.Connection("paulo.mongohq.com",10042)
    #     db = con.mytest
    #     db.authenticate("root", "sa123")
    #     db.urllist.drop()