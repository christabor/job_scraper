import json
import os
from pyquery import PyQuery as pq

hrefs = {}


def process_all():
    with open('index.html', 'rb') as htmlfile:
        html = pq(htmlfile.read())
        html.find('a').each(_process_link)
    f = open('all-job-categories.json', 'wb')
    f.write(json.dumps(hrefs))
    f.write('\n')
    f.close()


def run_all():
    """Use with caution"""
    with open('all-job-categories.json', 'rb') as jobs:
        categories = dict(json.loads(jobs.read()))
        jobs.close()
        for k, keywords in categories.iteritems():
            for keyword in keywords:
                cmd = ('scrapy crawl careerbuilder-job '
                       '-a category={category} -o '
                       'data/{category}.json -t json'.format(category=keyword))
                print cmd
                try:
                    os.system(cmd)
                except OSError:
                    continue


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

process_first = raw_input('Process json first? YES/NO ==> ')
if process_first == 'YES':
    process_all()
run_all()
