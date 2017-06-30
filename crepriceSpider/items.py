# -*- coding: utf-8 -*-
from scrapy.item import Item,Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

class CrepricecnItem(Item):
    city = Field()
    citylink = Field()
    shortname = Field()


# 全东莞
# http://www.creprice.cn/market/dg/forsale/ALL/11.html

# 格式:www.creprice.cn/market/{dg}/{forsale}/{ALL}/{11}.html

# 二手房:forsale
# 租金:lease
# 新楼盘: http://www.creprice.cn/market/newha/city/dg.html
# 住宅:11.html 商铺:22.html 办公:21.html
# 新楼盘,只能获取到:房价概况,平均单价 元/平方,统计楼盘个数

# 数据更新时间：2017年05月24日 12:07
# //*[@id="content"]/div[3]/div[1]/div[1]/span

# 租金
# http://www.creprice.cn/market/dg/lease/ALL/11.html
class ListItem(Item):
    link = Field()
    # 省份
    province = Field()
    # 城市
    city = Field()
    # 区
    district = Field()
    # 镇区
    town = Field()
    city_short = Field()


class TownPageItem(Item):
    # link
    link = Field()
    # 抓取时间
    crawl_time = Field()
    # 网站数据更新时间
    website_update = Field()
    # 省份
    province = Field()
    # 城市
    city = Field()
    # 镇区
    town = Field()

    city_short = Field()
    town_short = Field()
    house_type = Field()

    # 用途  住宅
    usage = Field()
    # 交易  二手房或者租金
    transaction = Field()
    # 近一个月房价
    nearly_mouth_average = Field()
    # 近一个月新增房源
    nearly_add = Field()
    # 今日房价
    today_price = Field()
    # 上月房价
    last_mouth_price = Field()
    # 预测未来一个月房价
    next_mouth_price = Field()

    # 近一年的平均单价：
    nearly_year_average = Field()
    # 平均总价：
    # 新增房源：


# 长安镇
# http://www.creprice.cn/market/dg/forsale/CA/11.html



# 房价走势
class HousingPriceItem(Item):

    # 唯一id
    # link
    link = Field()
    # 抓取时间
    crawl_time = Field()
    # 网站数据更新时间
    website_update = Field()
    # 省份
    province = Field()
    # 城市
    city = Field()

    city_short = Field()
    # 用途  住宅
    usage = Field()
    # 交易  二手房或者租金
    transaction = Field()

    house_type = Field()
    # div[@class="uibox2"]/div[@class="ucont2"]/div[@class="tips-sy1 mb5"]/
    # 分析使用样本： 楼盘小区 1587 个  房产交易 50.6万 套次

    # 分析使用样本 - 楼盘小区个数
    areas_num = Field()
    #  - 房产交易 单位:套次
    realty_transfer = Field()

    # 近一年均价 (平均单价) /div[@class="column-data-list"]/div[@class="columnbox"]/
    # div[@class="title"]/div[@class="menu"]/span[@class="pricedata smwz"]/span[@class="mr20"]/span/text()
    average_price = Field()

    # /div[@class="column-data-list"]/div[@class="columnbox"]/div[@class="cont dn"]/div[@class="data-info dn"]/

    # div[@class="data-box"]/
    # div[@class="wbox mb30 tables dn"]/div[@id="chart_price_line_table"]/table/tbody/tr

    # # 年月
    # days = Field()
    # # ./td[@class="first"]
    # # 供给价格
    # supply_price = Field()
    # # ./td 第二个
    # # 关注房价
    # focus_price = Field()
    # # ./td[@class="last"]

    # 房价走势
    housing_tend = Field()
    # 房价分布
    housing_distribution = Field()

    # 近一月房价
    nearly_mouth_average = Field()

    # 新增房源
    new_add = Field()

    # 今日房价
    today_price = Field()

    # 上月房价
    last_mouth_price = Field()

    # 预测未来一个月房价
    next_mouth_price = Field()

    # ### 房价分布 ###
    # 统计开始年月,指的是查询当期,近一年统计的最早月份
    start_days = Field()
    # 统计结束年月
    end_days = Field()
    #
    # # # 价格区间
    # # price_interval = Field()
    # # # 供给占比
    # # supply_ratio = Field()
    # # # 关注占比
    # # focus_ratio = Field()
    #
    # # 镇区URL
    town_url = Field()


class CrepriceCNLoader(ItemLoader):
    default_item_class = HousingPriceItem
    # default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()

class TownPageLoader(ItemLoader):
    default_item_class = TownPageItem
    # default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()



class ListPageLoader(ItemLoader):
    default_item_class = ListItem
    default_output_processor = TakeFirst()
    description_out = Join()

