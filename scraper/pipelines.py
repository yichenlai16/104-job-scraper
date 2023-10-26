# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from elasticsearch_dsl import Document, Text, Integer, Date, Keyword, connections
import os
from dotenv import load_dotenv

load_dotenv()


class JobItemDocument(Document):
    jobName = Text(
        analyzer="ik_max_word",
        fields={"raw": Keyword()},
    )
    jobRole = Integer()
    jobAddrNoDesc = Text()
    jobAddress = Text()
    description = Text(analyzer="ik_smart")
    optionEdu = Text()
    periodDesc = Text()
    applyCnt = Integer()
    custName = Text()
    coIndustryDesc = Text()
    salaryLow = Integer()
    salaryHigh = Integer()
    appearDate = Date()
    jobLink = Keyword()
    remoteWorkType = Integer()
    major = Text(multi=True)
    salaryType = Text()
    _created_at = Date()

    class Index:
        name = os.getenv("ELASTICSEARCH_INDEX")


class ElasticsearchPipeline(object):
    def __init__(self):
        self.ELASTICSEARCH_SERVERS = os.getenv("ELASTICSEARCH_SERVERS")
        self.ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")

        connections.create_connection(hosts=self.ELASTICSEARCH_SERVERS, timeout=20)
        JobItemDocument.init(index=self.ELASTICSEARCH_INDEX)

    def process_item(self, item, spider):
        data = dict(item)

        s = JobItemDocument.search().query(
            "bool",
            must=[
                {"match": {"jobName.raw": data["jobName"]}},
                {"match": {"jobLink": data["jobLink"]}},
            ],
        )

        response = s.execute()

        if response:
            raise DropItem("Duplicated")

        try:
            JobItemDocument(**data).save()
        except Exception as e:
            raise DropItem(f"Failed to save item to Elasticsearch: {e}")

        return item


# class MongoPipeline:
#     collection_name = "scrapy_items"

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get("MONGO_URI"),
#             mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         existing_item = self.db[self.collection_name].find_one(
#             {"jobLink": item["jobLink"]}
#         )
#         if existing_item is None:
#             self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
#         else:
#             print("Duplicate item found")
#         return item
