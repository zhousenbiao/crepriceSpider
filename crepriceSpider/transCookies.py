# -*- coding: utf-8 -*-

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = "UM_distinctid=15c0fcfe4452a4-0e4b1acb63848a-1c2d1f03-1fa400-15c0fcfe446d5f; cityredata=d19e6299f314d4efb30f1f272d1e2f1c; cityurl=977a8727891b53c; _ga=GA1.2.1798936149.1494913902; _gid=GA1.2.435672067.1496622492; _gat=1; __asc=44929ae015c77563cbea979bbc6; __auc=7ce7758e15c0fcfebc0053b8e30; CNZZDATA1253686598=1609493572-1494913717-%7C1496650051; city=hz"
    trans = transCookie(cookie)
    print trans.stringToDict()