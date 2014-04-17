from scrapy.spider import Spider
from pyquery import PyQuery as pq
from jobs.items import JobDetail

SAVE_ROOT = 'data/'
root_url = 'http://www.careerbuilder.com/'
job_list_url = '{}jobs/keyword/__KEYWORD__?Ipath=BJTSE0'.format(root_url)
job_detail_url = '{}jobseeker/jobs/jobdetails.aspx?'.format(root_url)

# Selectors
job_title_id = '#job-titles'
detail_link_class = '.jt.prefTitle'
detail_job_description_class = '.pnlJobDescription'
detail_container = '#CBBody_contentmain'


class CareerBuilderJobSpider(Spider):
    name = 'careerbuilder-job'
    urls = []

    def _kword_url(self, keyword):
        return job_list_url.replace('__KEYWORD__', keyword)

    def _process_link(self, k, link):
        self.urls.append(pq(link).attr('href'))

    def _get_category_urls(self, category):
        # Gets all the URLs for a
        # category to then be added to self.start_urls
        # TODO: follow next page via dropdown
        html = pq(url=self._kword_url(category), parser='html')
        pq(html).find(detail_link_class).each(self._process_link)

    def __init__(self, category=None, *args, **kwargs):
        super(CareerBuilderJobSpider, self).__init__(*args, **kwargs)
        # Setup links
        self._get_category_urls(str(category))
        # Re-assign them to the scrapy list
        self.start_urls = self.urls

    def parse(self, response):
        html = pq(response.body).find(detail_container)
        job = JobDetail()
        snapshot = html.find('.section-body:last')

        job['description'] = html('#pnlJobDescription > p').text()
        job['pay'] = snapshot.find('.snap-line').eq(0).text()
        job['other_pay'] = snapshot.find('.snap-line').eq(1).text()
        job['employment_type'] = snapshot.find('.snap-line').eq(2).text()
        job['job_type'] = snapshot.find('.snap-line').eq(3).text()
        job['education'] = snapshot.find('.snap-line').eq(4).text()
        job['experience'] = snapshot.find('.snap-line').eq(5).text()
        job['manages_others'] = snapshot.find('.snap-line').eq(6).text()
        job['relocation'] = snapshot.find('.snap-line').eq(7).text()
        job['industry'] = snapshot.find('.snap-line').eq(8).text()
        job['required_travel'] = snapshot.find('.snap-line').eq(9).text()
        job['job_ID'] = snapshot.find('.snap-line').eq(10).text()
        job['requirements'] = html.find(
            '.section-body:first').find('ul').text()
        return job
