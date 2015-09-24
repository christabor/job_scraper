import os
import json

hrefs = {}
ALL_CATEGORIES = 'fixtures/onet_all-job-categories.json'


class OnetOnlineHelper:

    @staticmethod
    def read_categories():
        with open(ALL_CATEGORIES, 'rb') as jobs:
            data = json.loads(jobs.read())
            jobs.close()
            return data

    @staticmethod
    def load_categories(as_string=True):
        data = OnetOnlineHelper.read_categories()
        categories = []
        for category in data:
            if category is not None:
                if 'name' in category and category['name'] != '':
                    categories.append('{}. {}'.format(
                        category['id'], category['name']))
        if as_string:
            return '\n'.join(categories)
        return categories

    @staticmethod
    def load_occupations(category_id, as_string=True):
        occupations = []
        data = OnetOnlineHelper.get_occupations(category_id)
        for occupation in data:
            occupations.append('{} {} ({})'.format(
                occupation['code'],
                occupation['occupation']['job'],
                occupation['occupation']['url']))
        if as_string:
            return '\n'.join(occupations)
        return occupations

    @staticmethod
    def get_occupations(category_id):
        data = OnetOnlineHelper.read_categories()
        for category in data:
            if category is not None:
                if 'id' in category and category['id'] == category_id:
                    return category['occupation_data']

    @staticmethod
    def process_all_jobs(category_id):
        for occupation in OnetOnlineHelper.get_occupations(category_id):
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
