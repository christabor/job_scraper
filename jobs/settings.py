# Scrapy settings for jobs project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'jobs'
SPIDER_MODULES = ['jobs.spiders']
NEWSPIDER_MODULE = 'jobs.spiders'
ITEM_PIPELINES = {
    'jobs.pipelines.FilterJobDetailsPipeline': 0,
}

# Crawl responsibly by identifying yourself
# (and your website) on the user-agent
USER_AGENT = 'jobs scraping tool'

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
DOWNLOAD_DELAY = 0.2
