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
ITEM_PIPELINES = [
    'jobs.pipelines.FilterJobDetailsPipeline',
]

# Crawl responsibly by identifying yourself
# (and your website) on the user-agent
USER_AGENT = 'jobs scraping tool'

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
DOWNLOAD_DELAY = 0.2

# MongoDB pipeline
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'jobs'
MONGODB_COLLECTION = 'jobs'
MONGODB_ADD_TIMESTAMP = True

USE_DB = False

if USE_DB:
    ITEM_PIPELINES.append('scrapy_mongodb.MongoDBPipeline')
