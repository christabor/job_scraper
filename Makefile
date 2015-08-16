onet_categories:
	@echo "Crawling all categories for ONet Online"
	trap "rm fixtures/onet_all-job-categories.json -t json" SIGHUP SIGINT SIGTERM
	scrapy crawl onet_categories -o fixtures/onet_all-job-categories.json -t json

onet_jobs:
	@echo "Crawling all jobs for ONet Online"
	trap "rm fixtures/onet_jobs.json" SIGHUP SIGINT SIGTERM
	scrapy crawl onet_jobs -o -a url=$1 fixtures/onet_jobs.json -t json
