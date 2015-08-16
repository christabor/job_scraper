from scrapy.spiders import Spider
from pyquery import PyQuery as Pq
from jobs import items


class ONetJobSpider(Spider):

    start_urls = []
    root_url = 'http://www.onetonline.org/find/industry/'
    name = 'onet_jobs'

    def __init__(self, url=None, *args, **kwargs):
        super(ONetJobSpider, self).__init__(*args, **kwargs)
        if url is not None:
            self.start_urls = [url]

    def _list(self, html, dom_selector, custom=None):
        items = []

        def handle_li(k, li):
            items.append(Pq(li).text())

        if custom is None:
            html.find(dom_selector).find('li').each(handle_li)
        else:
            custom.find('li').each(handle_li)
        return items

    def _table(self, html, dom_selector):
        items = []

        def handle_row(k, row):
            items.append(Pq(row).text())

        html.find(dom_selector).find('tr').each(handle_row)
        return items

    def parse(self, response):
        html = Pq(response.body)
        job = items.OnetJob()
        job['url'] = response.url
        job['alt_title'] = html.find('[class="titleb"]').text()
        job['job_sample'] = html.find(
            'p:contains("Sample of reported job titles:")').text()

        job['summary'] = html.find(
            '#realcontent').find('p:eq(0)').text()

        job['job_sample'] = job['job_sample'].replace(
            'Sample of reported job titles:', '').split(', ')

        job['tasks'] = self._list(html, '.section_Tasks .moreinfo')
        job['tools'] = self._list(
            html, '.section_ToolsTechnology .moreinfo:first')
        job['technology'] = self._list(
            html, '.section_ToolsTechnology .moreinfo:last')
        job['knowledge'] = self._list(html, '.section_Knowledge .moreinfo')
        job['skills'] = self._list(html, '.section_Skills .moreinfo')
        job['abilities'] = self._list(html, '.section_Abilities .moreinfo')
        job['work_activities'] = {
            'basic': self._list(html, '.section_WorkActivities .moreinfo'),
            'detailed': self._list(
                html, '.section_DetailedWorkActivities .moreinfo'),
        }
        job['work_context'] = self._list(
            html, '.section_WorkContext .moreinfo')

        job['job_zone'] = self._table(html, '#content table:first')
        job['education'] = self._table(html, '#content table:eq(1)')

        job['interests'] = self._list(html, None, custom=html.find(
            '[name="Interests"]').siblings('.moreinfo:first'))

        job['work_styles'] = self._list(
            html, '.section_WorkStyles .moreinfo')

        job['interests'] = self._list(html, None, custom=html.find(
            '[name="WorkValues"]').siblings('.moreinfo:eq(1)'))

        job['related_occupations'] = self._table(
            html, '.section_RelatedOccupations table')

        job['wages_employment'] = self._table(
            html, '[summary="Wages & Employment Trends information'
                  ' for this occupation"]')

        job['job_openings'] = ''
        job['additional_info'] = ''
        return job
