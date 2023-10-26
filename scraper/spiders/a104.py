import scrapy
from scrapy.http import FormRequest
from scraper.items import A104Item
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class A104Spider(scrapy.Spider):
    name = "104"
    allowed_domains = ["www.104.com.tw"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW",
            "origin": "https://www.104.com.tw/",
            "referer": "https://www.104.com.tw/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
            "Content-Type": "application/json",
        }
    }

    start_url = "https://www.104.com.tw/jobs/search/list"

    def start_requests(self):
        # 預設頁面數量
        try:
            self.page = int(os.getenv("SCRAPY_PAGES"))
            if not 1 <= self.page <= 150:
                raise ValueError("檢查 env.SCRAPY_PAGES")
        except:
            print("變數有誤，預設爬取頁數 為 1。")
            self.page = 1

        for i in range(int(self.page)):
            yield FormRequest(
                url=self.start_url + f"?page={i+1}&isnew=0",
                method="GET",
                callback=self.parse,
            )

    def parse(self, response):
        body = json.loads(response.body)
        jobs = body["data"]["list"]
        item = A104Item()
        for job in jobs:
            item["jobName"] = job["jobName"]
            item["jobRole"] = job["jobRole"]
            item["jobAddrNoDesc"] = job["jobAddrNoDesc"]
            item["jobAddress"] = job["jobAddress"]
            item["description"] = job["description"]
            item["optionEdu"] = job["optionEdu"]
            item["periodDesc"] = job["periodDesc"]
            item["applyCnt"] = job["applyCnt"]
            item["custName"] = job["custName"]
            item["coIndustryDesc"] = job["coIndustryDesc"]
            item["salaryLow"] = job["salaryLow"]
            item["salaryHigh"] = job["salaryHigh"]
            item["appearDate"] = datetime.strptime(job["appearDate"], "%Y%m%d")
            item["jobLink"] = "https:" + job["link"]["job"].split("?")[0]
            item["remoteWorkType"] = job["remoteWorkType"]
            item["major"] = job["major"]
            item["salaryType"] = job["salaryType"]

            yield item
