import scrapy
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scraper.items import ScraperItem
import inspect
import requests
import json
from datetime import datetime
def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


class Spo104Spider(scrapy.Spider):
    name = 'spo-104'
    allowed_domains = ['www.104.com.tw']

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW',
            'origin': 'https://www.104.com.tw/',
            'referer': 'https://www.104.com.tw/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Content-Type': 'application/json',
        }}

    start_url = 'https://www.104.com.tw/jobs/search/list'

    def start_requests(self):
        yield FormRequest(url=self.start_url, method="GET", callback=self.parse)


    def parse(self, response):
        body = json.loads(response.body)
        # print(body)
        jobs = body['data']['list']

        for job in jobs:
            source_job_url = "https"+job['link']['job']
            source_company_url = "https"+job['link']['cust']

            source_job_website = str(source_job_url.split('/')[-3])
            source_job_cat = str(source_job_url.split('/')[-2])
            source_job_serialnumber = str(
                source_job_url.split('/')[-1].split('?')[0])
            metalist = [source_job_url, source_job_serialnumber]

            meta = dict()

            for i in range(len(metalist)):
                meta[retrieve_name(metalist[i])[0]] = metalist[i]

            yield FormRequest(('https://www.104.com.tw/job/ajax/content/'+source_job_serialnumber),
                              meta=meta,
                              callback=self.getJobDetail, dont_filter=False)

    def getJobDetail(self, response):

        body = json.loads(response.body)
        data = body['data']

        item = ScraperItem()

        item['URL'] = response.meta['source_job_url']
        item['website'] = "104"
        item['jobId'] = response.meta['source_job_serialnumber']
        item['jobName'] = data['header']['jobName']
        item['custName'] = data['header']['custName']
        item['jobUpDate'] = datetime.strptime(data['header']['appearDate'],'%Y/%m/%d')

        item['jobDesc'] = data['jobDetail']['jobDescription']
        item['jobCategory'] = [x['description']
                               for x in data['jobDetail']['jobCategory']]

        item['salaryLow'] = data['jobDetail']['salaryMin']
        item['salaryHigh'] = data['jobDetail']['salaryMax']

        salaryType = data['jobDetail']['salaryType']
        if salaryType == 10:
            item['salaryType'] = "面議"
        elif salaryType == 20:
            item['salaryType'] = "論件計酬"
        elif salaryType == 30:
            item['salaryType'] = "時薪"
        elif salaryType == 40:
            item['salaryType'] = "日薪"
        elif salaryType == 50:
            item['salaryType'] = "月薪"
        elif salaryType == 60:
            item['salaryType'] = "年薪"
        else:
            item['salaryType'] = ""

        # item['salaryType'] = data['jobDetail']['salaryType']

        jobType =  data['jobDetail']['jobType']
        if jobType == 1:
            item['jobType'] = '全職'
        elif jobType == 2:
            item['jobType'] = '兼職'
        elif jobType == 3:
            item['jobType'] = '高階'
        else:
            item['jobType'] = ''

        # item['jobType'] = data['jobDetail']['jobType']

        item['jobArea'] = data['jobDetail']['addressRegion']
        item['jobAddress'] = data['jobDetail']['addressDetail']


        yield item
