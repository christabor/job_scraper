import json
import os
from pyquery import PyQuery as pq

hrefs = {}
ALL_CATEGORIES = 'all-job-categories.json'


def process_all():
    with open('index.html', 'rb') as htmlfile:
        html = pq(htmlfile.read())
        html.find('a').each(_process_link)
    f = open(ALL_CATEGORIES, 'wb')
    f.write(json.dumps(hrefs))
    f.write('\n')
    f.close()


def get_spiders_list():
    # Convention: 'name' attribute used for scrapy should match
    # the file name, minus the _spider string.
    files = [name.replace('_spider.py', '') for name in
             os.listdir('jobs/spiders') if name.endswith('py')
             and name != '__init__.py']
    return files


def process_one(spider, keyword):
    cmd = ('scrapy crawl {spider} '
           '-a category={keyword} -o '
           'data/{spider}/{keyword}.json -t json'.format(
                spider=spider,
                keyword=keyword))
    try:
        os.system(cmd)
    except OSError:
        pass


def load_all_categories():
    with open(ALL_CATEGORIES, 'rb') as jobs:
        categories = dict(json.loads(jobs.read()))
        jobs.close()
    return categories


def run_all():
    """Use with caution"""
    categories = load_all_categories()
    for k, keywords in categories.iteritems():
        for keyword in keywords:
            process_one(keyword)


def _process_link(k, link):
    # Sort by first letter
    url = pq(link).attr('href').strip().replace(
        'jobs/keyword/', '').replace('?Ipath=BJTSEO', '').replace(
        'http://careerbuilder.com/', '').replace('/', '')
    letter = url[:1].upper()
    try:
        hrefs[letter].append(url)
    except KeyError:
        hrefs[letter] = []
