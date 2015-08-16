import json
import os
from pyquery import PyQuery as Pq

hrefs = {}
ALL_CATEGORIES = 'fixtures/careerbuilder_all-job-categories.json'


class CareerBuilderHelper:

    @staticmethod
    def write_all_to_html():
        with open('index.html', 'rb') as htmlfile:
            html = Pq(htmlfile.read())
            html.find('a').each(CareerBuilderHelper._process_link)
        f = open(ALL_CATEGORIES, 'wb')
        f.write(json.dumps(hrefs))
        f.write('\n')
        f.close()

    @staticmethod
    def process_one(spider, keyword):
        cmd = ('scrapy crawl {spider} -a category={keyword} -o '
               'fixtures/{spider}/{keyword}.json -t json').format(
                   spider=spider, keyword=keyword)
        try:
            os.system(cmd)
        except OSError:
            pass

    @staticmethod
    def load_categories():
        with open(ALL_CATEGORIES, 'rb') as jobs:
            categories = dict(json.loads(jobs.read()))
            jobs.close()
        return categories

    @staticmethod
    def run_all():
        """Use with caution"""
        categories = CareerBuilderHelper.load_categories()
        for k, keywords in categories.iteritems():
            for keyword in keywords:
                CareerBuilderHelper.process_one('careerbuilder', keyword)

    @staticmethod
    def _process_link(k, link):
        # Sort by first letter
        url = Pq(link).attr('href').strip().replace(
            'jobs/keyword/', '').replace(
                '?Ipath=BJTSEO', '').replace(
                    'http://careerbuilder.com/', '').replace('/', '')
        letter = url[:1].upper()
        try:
            hrefs[letter].append(url)
        except KeyError:
            hrefs[letter] = []
