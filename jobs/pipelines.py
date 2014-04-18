# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FilterJobDetailsPipeline(object):
    def process_item(self, item, spider):
        for k, el in item.iteritems():
            el = el.strip()
        return item
