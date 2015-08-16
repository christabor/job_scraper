from scrapy.item import Item, Field

"""
    ==== SCRAPING

    1. get all urls A-Z
    2. get all job links within each category
    3. follow each link and get metadata per job title (where applicable):
        -location
        -date
        -company
        -description
        -requirements
        -snapshot
            -pay
            -other pay
            -employment type
            -job type
            -education
            -experience
            -manages others
            -relocation
            -industry
            -required travel
            -job ID
    4. follow 'apply link' and find all fields:
        -field label
        -field input

        expected output:

            {jobs: [
                {
                    'title': 'FOO',
                    'url': 'url',
                    'metadata': {
                        'keys': 'values'
                    },
                    formfields: {
                        'keys': 'values'
                    }
                }
            ]}

    5. compile and output to file, PER job

    6. **OPTIONAL** graph output to find correlations

    ==== ANALYSIS
"""


class OnetJob(Item):
    # Root url: http://www.onetonline.org/link/summary/{JOB_ID}

    url = Field()
    alt_title = Field()
    job_sample = Field()
    summary = Field()
    # Sections on the website
    tasks = Field()
    tools = Field()
    technology = Field()
    knowledge = Field()
    skills = Field()
    abilities = Field()
    work_activities = Field()
    detailed_work_activities = Field()
    work_context = Field()
    job_zone = Field()
    education = Field()
    credentials = Field()
    interests = Field()
    work_styles = Field()
    work_values = Field()
    related_occupations = Field()
    wages_employment = Field()
    job_openings = Field()
    additional_info = Field()


class ONetCategory(Item):
    id = Field()
    name = Field()
    url = Field()
    # Bureau of Labor Statistics
    bls_url = Field()
    occupation_data = Field()


class JobDetail(Item):
    # define the fields for your item here like:
    url = Field()
    location = Field()
    date = Field()
    company = Field()
    description = Field()
    requirements = Field()
    snapshot = Field()
    pay = Field()
    other_pay = Field()
    employment_type = Field()
    job_type = Field()
    education = Field()
    experience = Field()
    manages_others = Field()
    relocation = Field()
    industry = Field()
    required_travel = Field()
    job_ID = Field()
    requirements = Field()
