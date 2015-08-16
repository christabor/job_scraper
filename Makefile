onet_categories:
	@echo "Crawling all categories for ONet Online"
	scrapy crawl onet_categories -o onet_categories.json -t json

onet_jobs:
	@echo "Crawling all jobs for ONet Online"
	scrapy crawl onet_jobs -o onet_jobs.json -t json
