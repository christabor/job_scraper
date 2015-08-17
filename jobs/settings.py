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
# https://github.com/sebdah/scrapy-mongodb
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'jobs'
MONGODB_COLLECTION = 'jobs'
MONGODB_ADD_TIMESTAMP = True

USE_DB = True
USE_REPLICA = False
MONGODB_REPLICA_SET = 'jobs-replica'

if USE_DB:
    ITEM_PIPELINES.append('scrapy_mongodb.MongoDBPipeline')

if USE_REPLICA:
    MONGODB_URI = ''  # Replica hosts
