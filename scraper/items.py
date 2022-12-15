# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobName = scrapy.Field()
    custName = scrapy.Field()
    jobType = scrapy.Field()
    jobDesc = scrapy.Field()
    jobCategory = scrapy.Field()
    salaryLow = scrapy.Field()
    salaryHigh = scrapy.Field()
    salaryType = scrapy.Field()
    jobArea = scrapy.Field()
    jobAddress = scrapy.Field()
    jobUpDate = scrapy.Field()
    jobApplyCount = scrapy.Field()
    website = scrapy.Field()
    URL = scrapy.Field()
    jobId = scrapy.Field()

    pass
