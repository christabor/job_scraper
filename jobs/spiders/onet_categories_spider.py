from scrapy.spiders import Spider
from pyquery import PyQuery as Pq
from jobs import items


class ONetCategoriesSpider(Spider):

    name = 'onet_categories'
    root_url = 'http://www.onetonline.org/find/industry/'
    start_urls = []
    occupations = []

    def __init__(self, *args, **kwargs):
        super(ONetCategoriesSpider, self).__init__(*args, **kwargs)
        # Setup URLs
        self._get_category_urls()

    def _kword_url(self):
        return self.root_url.format()

    def _process_option(self, k, option):
        self.start_urls.append('{}?i={}&g=Go'.format(
            self.root_url, Pq(option).val()))

    def _get_category_urls(self):
        html = Pq(url=self.root_url, parser='html')
        # Get all category IDs from dropdown menu
        Pq(html).find('#content .formsub select option').each(
            self._process_option)

    def _extract_occupation(self, row_num, row):
        # First row is incorrectly used as a thead row.
        if row_num == 0:
            return
        data = {}

        def handle_td(k, td):
            # 0. # employed
            # 1. Code
            # 2. Occupation + link !IMPORTANT
            # 3. Project growth - as image
            # 4. Projected openings
            td = Pq(td)
            if k == 0:
                data['num_employed'] = td.text()
            if k == 1:
                data['code'] = td.text()
            if k == 2:
                subdata = {'job': td.text(), 'url': td.find('a').attr('href')}
                data['occupation'] = subdata
            if k == 3:
                data['projected_growth'] = td.find('img').attr('alt')
            if k == 4:
                data['projected_openings'] = td.text()

        Pq(row).find('td').each(handle_td)
        self.occupations.append(data)

    def _extract_occupations(self, html):
        html.find('#content table tr').each(self._extract_occupation)
        return self.occupations

    def parse(self, response):
        category = items.ONetCategory()
        html = Pq(response.body)
        category['url'] = response.url
        category['name'] = html.find('.reportdesc:eq(0)').text().replace(
            'Save Table ( XLS / CSV )', '')
        category['id'] = response.url.replace('{}?i'.format(
            self.root_url), '').replace(
                '&g=Go', '').replace('=', '').replace('.', '')
        category['bls_url'] = html.find(
            'div.reportdesc a:first').attr('href')
        category['occupation_data'] = self._extract_occupations(html)
        return category
