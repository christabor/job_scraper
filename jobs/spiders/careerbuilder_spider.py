from scrapy.spider import Spider
from pyquery import PyQuery as pq
from jobs.items import JobDetail

root_url = 'http://www.careerbuilder.com/'
job_list_url = '{}jobs/keyword/__KEYWORD__?Ipath=BJTSE0'.format(root_url)
job_detail_url = '{}jobseeker/jobs/jobdetails.aspx?'.format(root_url)

detail_link_class = '.jt.prefTitle'


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
        # import pdb;pdb.set_trace()  # Leave in for easy debugging inline
        """This is unfortunately not dependable, nor can it be, with the
        the extremely arbitrary html layouts provided. Often times they are
        custom classes or tags tailored to each company, with a 'custom theme',
        so making it work perfectly without some kind of NLP or
        Machine Learning is probably impossible without a
        bunch of manual if/else type logic :("""
        html = pq(response.body)
        job = JobDetail()

        # Populate with custom fields
        job['url'] = response.url
        job['description'] = html('#pnlJobDescription').text()
        job['requirements'] = html.find('.section-body:first').find('li').text()
        job['pay'] = html.find(':contains("Base Pay")').next().text()
        job['other_pay'] = html.find(':contains("Other Pay")').next().text()
        job['employment_type'] = html.find(':contains("Employment Type")').next().text()
        job['job_type'] = html.find(':contains("Job Type")').next().text()
        job['education'] = html.find(':contains("Education")').next().text()
        job['experience'] = html.find(':contains("Experience")').next().text()
        job['manages_others'] = html.find(':contains("Manages Others")').next().text()
        job['relocation'] = html.find(':contains("Relocation")').next().text()
        job['industry'] = html.find(':contains("Industry")').next().text()
        job['required_travel'] = html.find(':contains("Required Travel")').next().text()
        job['job_ID'] = html.find(':contains("Job ID")').next().text()
        return job
