import os
import json

hrefs = {}
ALL_CATEGORIES = 'fixtures/onet_all-job-categories.json'


class OnetOnlineHelper:

    @staticmethod
    def load_categories():
        with open(ALL_CATEGORIES, 'rb') as jobs:
            categories = []
            data = json.loads(jobs.read())
            for category in data:
                if category is not None:
                    if 'name' in category and 'name' in category:
                        if category['name'] != '':
                            categories.append('{}. {}'.format(
                                category['id'], category['name']))
            return '\n'.join(categories)

    @staticmethod
    def load_occupations(category_id):
        occupations = []
        data = OnetOnlineHelper._get_occupations(category_id)
        for occupation in data:
            occupations.append('{} {} ({})'.format(
                occupation['code'],
                occupation['occupation']['job'],
                occupation['occupation']['url']))
        return '\n'.join(occupations)

    @staticmethod
    def _get_occupations(category_id):
        with open(ALL_CATEGORIES, 'rb') as jobs:
            data = json.loads(jobs.read())
            for category in data:
                if category is not None:
                    if 'id' in category and category['id'] == category_id:
                        return category['occupation_data']

    @staticmethod
    def process_all_jobs(category_id):
        for occupation in OnetOnlineHelper._get_occupations(category_id):
            code = occupation['code']
            json_file = 'fixtures/{spider}/{code}.json -t json'.format(
                spider='onet_jobs', code=code)
            cmd = ('scrapy crawl {spider} -a id={code} -o {json_file}').format(
                json_file=json_file, spider='onet_jobs', code=code)
            try:
                os.system(cmd)
            except OSError:
                pass

    @staticmethod
    def process_job(code):
        json_file = 'fixtures/{spider}/{code}.json -t json'.format(
            spider='onet_jobs', code=code)
        cmd = ('scrapy crawl {spider} -a id={code} -o {json_file}').format(
            json_file=json_file, spider='onet_jobs', code=code)
        try:
            os.system(cmd)
        except OSError:
            pass
