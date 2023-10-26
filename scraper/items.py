# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class A104Item(scrapy.Item):
    # 工作名稱 Str
    jobName = scrapy.Field()
    # 工作型態 Int 1正職 2兼職 3高階
    jobRole = scrapy.Field()
    # 工作區域 Str
    jobAddrNoDesc = scrapy.Field()
    # 工作地址 Str
    jobAddress = scrapy.Field()
    # 工作描述 Str
    description = scrapy.Field()
    # 學歷要求 Str
    optionEdu = scrapy.Field()
    # 經歷要求 Str
    periodDesc = scrapy.Field()
    # 應徵人數 Int
    applyCnt = scrapy.Field()
    # 公司名稱 Str
    custName = scrapy.Field()
    # 公司產業 Str
    coIndustryDesc = scrapy.Field()
    # 最低薪水 Int
    salaryLow = scrapy.Field()
    # 最高薪水 Int
    salaryHigh = scrapy.Field()
    # 發布日期 Date
    appearDate = scrapy.Field()
    # URL
    jobLink = scrapy.Field()
    # 遠端工作 Int 0無法 1完全 2部分
    remoteWorkType = scrapy.Field()
    # 科系要求 Array
    major = scrapy.Field()
    # 薪水型態 Str H時薪 M月薪 Y年薪 ""面議/按件計酬
    salaryType = scrapy.Field()

    pass
