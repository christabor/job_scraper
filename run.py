from pprint import pprint as ppr
from helpers import generic as gen
from helpers.careerbuilder import CareerBuilderHelper as Cb
from helpers.onetonline import OnetOnlineHelper as Onet

print('Enter a spider to run: ')
print(gen.get_spiders_list())
spider = raw_input('Spider: ==> ')

if spider == 'careerbuilder':
    process_first = raw_input('Process json first? y/n ==> ')
    run_all_tests = raw_input('Run all tests? y/n ==> ')
    if process_first == 'y':
        Cb.process_all()
    if run_all_tests == 'y':
        Cb.run_all()
    else:
        print('Enter a job title to run:')
        ppr(Cb.load_categories())
        keyword = raw_input('Title: ==> ')
        if keyword:
            Cb.process_one(spider, keyword)

elif spider == 'onet_categories':
    print('Not implemented...')
    ppr(Onet.load_onet_categories())

elif spider == 'onet_jobs':
    print('Not implemented...')
