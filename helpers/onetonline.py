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
                    if 'name' in category and 'url' in category:
                        categories.append('{}. {}'.format(
                            category['id'], category['name']))
            jobs.close()
            return '\n'.join(categories)
