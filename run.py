from pprint import pprint as ppr
from helpers import generic as gen
from helpers.careerbuilder import CareerBuilderHelper as Cb
from helpers.onetonline import OnetOnlineHelper as Onet

print('Enter a spider to run: ')
print(gen.get_spiders_list())
spider = raw_input('Spider: ==> ')

# Careerbuilder
if spider == '1':
    process_first = raw_input('Write JSON to app first? y/n ==> ')
    run_all_tests = raw_input('Run all tests? y/n ==> ')
    if process_first == 'y':
        Cb.write_all_to_html()
    if run_all_tests == 'y':
        Cb.run_all()
    else:
        print('Enter a job title to run:')
        ppr(Cb.load_categories())
        keyword = raw_input('Title: ==> ')
        if keyword:
            Cb.process_one(spider, keyword)

# Onet categories
elif spider == '2':
    print('Pick a category to run:')
    print(Onet.load_categories())
    id = raw_input('Choose a job category ID ==> ')
    occupations = Onet.load_occupations(id)
    process_all = raw_input('Process all? y/n ==> ')
    if process_all == 'y':
        Onet.process_all_jobs(id)
    else:
        print('Occupations for ID {}'.format(id))
        print(occupations)
        code = raw_input('Pick a job code to run ==> ')
        if code:
            Onet.process_job(code)

# Onet jobs
elif spider == '3':
    print('Not implemented...')

else:
    print('"{}" is an invalid spider.'.format(spider))
