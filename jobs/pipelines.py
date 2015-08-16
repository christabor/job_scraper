# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from jobs import spiders
import pymongo


class FilterJobDetailsPipeline(object):

    def _strip_any(self, item):
        if item is None:
            return item
        if type(item) is str:
            return item.strip()
        elif type(item) is list:
            for _item in item:
                _item = _item.strip()
        elif type(item) is dict:
            for k, _item in item.iteritems():
                _item = _item.strip()
        return item

    def process_item(self, item, spider):
        cb = spiders.careerbuilder_spider.CareerBuilderJobSpider
        if cb.name == 'careerbuilder':
            for k, el in item.iteritems():
                # Replace duplicate key from matching
                # pseudoselector
                if type(el) is str:
                    el = el.strip().replace(k, '')
            return item
        else:
            return self._strip_any(item)


class MongoPipeline(object):

    collection_name = 'onet_job'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item
