from scrapy.spider import Spider
from pyquery import PyQuery as pq
from jobs.items import JobDetail

root_url = 'http://www.careerbuilder.com/'
job_list_url = '{}jobs/keyword/__KEYWORD__?Ipath=BJTSE0'.format(root_url)
job_detail_url = '{}jobseeker/jobs/jobdetails.aspx?'.format(root_url)

# Selectors
job_title_id = '#job-titles'
detail_link_class = '.jt.prefTitle'
detail_container = '#CBBody_contentmain'
custom_detail_container = '#JobDetails_ucJobDetailsSkin_tdJSCenter'


class CareerBuilderJobSpider(Spider):
    name = 'careerbuilder'
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
        """This is unfortunately not dependable, nor can it be, with the
        the extremely arbitrary html layouts provided. Often times they are
        custom classes or tags tailored to each company, with a 'custom theme',
        so making it work perfectly without some kind of NLP or
        Machine Learning is probably impossible without a
        bunch of manual if/else type logic :("""
        item = '.snap-line'
        resp = pq(response.body)
        html = resp.find(detail_container)
        job = JobDetail()
        # Try to re-evaulate for custom skinned pages
        if not html:
            html = resp.find(custom_detail_container)
        if not html:
            return job
        # Populate with custom fields
        job['description'] = html('#pnlJobDescription').text()
        job['requirements'] = html.find('.section-body:first').find('li').text()
        job['pay'] = html.find(item + ':contains("Base Pay")').text()
        job['other_pay'] = html.find(item + ':contains("Other Pay")').text()
        job['employment_type'] = html.find(item + ':contains("Employment Type")').text()
        job['job_type'] = html.find(item + ':contains("Job Type")').text()
        job['education'] = html.find(item + ':contains("Education")').text()
        job['experience'] = html.find(item + ':contains("Experience")').text()
        job['manages_others'] = html.find(item + ':contains("Manages Others")').text()
        job['relocation'] = html.find(item + ':contains("Relocation")').text()
        job['industry'] = html.find(item + ':contains("Industry")').text()
        job['required_travel'] = html.find(item + ':contains("Required Travel")').text()
        job['job_ID'] = html.find(item + ':contains("Job ID")').text()
        return job
