jobScraper
==========

Scraping tool that uses scrapy, pyquery and more
**What can it do?**
Well, it can currently execute a very large dataset of urls and automatically process them via command line. It will run a given set of urls, follow those, crawl each child page, and dump the results into JSON format.
So, give A-Z, you will get all job categories from A-Z, with all job listings, and all job listing details, as JSON -- a very large dataset indeed!

I'll probably add some D3js visualizations once I've fine tuned it all.

## Scrapers

### CareerBuilder

Scrapes all categories and jobs from CareerBuilder.com. The details can be inconsistent for specific jobs, since the site HTML structure for each job page is unique for each company, making it very inconsistent and harder to parse.

### OnetOnline

Scrapes all categories and occupation types form OnetOnline.org. This scraper
is the preferred one, since the site structure is more consistent and job data is more detailed. This site does not offer listings however, whereas CareerBuilder does.

## Command line structure

While the makefile provides some commands to quickly run scrapy jobs, the `run.py` file provides all command line access. All helper code for interacting with the user is provided here.

Each scraper job provides its own class for dealing with command line parsing of the structured data that was scraped. The general idea is that large JSON datasets are downloaded once, then parsed by the CLI and traversed directly, allowing programmatic access to the raw JSON itself, for future use.

## Persistence

By default, jobScraper is setup to handle storage to Mongo, as well as the default json flatfile. These can be used interchangeably, and a few helper scripts have been added for munging and backfilling data into mongo. The run script also allows navigating the downloaded json files and using them as options for the command line tool. The idea is to allow moving between raw json files, command line, and high-level persistent like Mongo.
