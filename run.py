from pprint import pprint as ppr
import helpers

process_first = raw_input('Process json first? y/n ==> ')
run_all_tests = raw_input('Run all tests? y/n ==> ')

if process_first == 'y':
    helpers.process_all()

if run_all_tests == 'y':
    helpers.run_all()
else:
    print 'Enter a spider to run: '
    print helpers.get_spiders_list()
    spider = raw_input('Spider: ==> ')
    if spider == 'careerbuilder':
        print 'Enter a job title to run:'
        print ppr(helpers.load_all_categories())
        keyword = raw_input('Title: ==> ')
        if keyword:
            helpers.process_one(spider, keyword)
