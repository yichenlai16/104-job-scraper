from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from elasticsearch import Elasticsearch
import os
import time

from dotenv import load_dotenv

load_dotenv()

# Check Elasticsearch Status
client = Elasticsearch(os.getenv("ELASTICSEARCH_SERVERS"))

status = client.ping()

while status == False:
    delay = 2
    time.sleep(delay)
    print(f"Reconnect Elasticsearch Server in {delay} Sec")
    status = client.ping()


# Start Scrapy
if status == True:
    process = CrawlerProcess(get_project_settings())
    process.crawl("104")
    process.start()
