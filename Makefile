onet_categories:
	@echo "Crawling all categories for ONet Online"
	scrapy crawl onet_categories -o fixtures/onet_all-job-categories.json -t json

onet_jobs:
	@echo "Crawling all jobs for ONet Online"
	scrapy crawl onet_jobs -o -a url=$1 onet_jobs.json -t json
