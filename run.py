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


def run_all():
    """Use with caution"""
    with open(ALL_CATEGORIES, 'rb') as jobs:
        categories = dict(json.loads(jobs.read()))
        jobs.close()
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

process_first = raw_input('Process json first? y/n ==> ')
run_all_tests = raw_input('Run all tests? y/n ==> ')

if process_first == 'y':
    process_all()

if run_all_tests == 'y':
    run_all()
else:
    spider = raw_input('Enter a spider to run: ')
    if spider == 'careerbuilder-job':
        keyword = raw_input('Enter a keyword to run: ')
    else:
        keyword = None
    process_one(spider, keyword)
