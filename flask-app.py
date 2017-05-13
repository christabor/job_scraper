import json
from flask import Flask
from flask import request
from flask import render_template
from helpers.careerbuilder import CareerBuilderHelper
from helpers.onetonline import OnetOnlineHelper

app = Flask(__name__)
app.debug = True


@app.template_filter('blank')
def blank(value):
    return value == ''


@app.template_filter('islist')
def is_list(value):
    return isinstance(value, list)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/onet')
def onetonline():
    files = OnetOnlineHelper.read_categories()
    # Limit set since the number of categories is insane... lazy load?
    data = {
        'categories': files,
        'max': 4
    }
    return render_template('onetonline.html', **data)


@app.route('/onet/category/<category_id>')
def onetonline_category(category_id):
    files = OnetOnlineHelper.read_categories()
    # Ad-hoc way for now...
    data = {
        'categories': files,
        'id': str(category_id),
    }
    return render_template('onetonline-category.html', **data)


@app.route('/onet/dataviz')
def onet_dataviz():
    # TODO
    return render_template('onet_dataviz.html')


@app.route('/onet/job/<job_id>/detail')
def onet_jobdata(job_id):
    filedata = None
    with open('fixtures/onet_jobs/{}.json'.format(job_id), 'rb') as jobs:
        if 'as_json' in request.args:
            return json.dumps(jobs.read())
        data = json.loads(jobs.read())
        jobs.close()
    if 'as_json' in request.args:
        return filedata
    back_url = '/onet'
    if 'json_nav' in request.args:
        context = {
            'data': data[0],
            'back_url': back_url,
            'heading': 'Job: ' + job_id
        }
        return render_template(
            'json_view.html', **context)
    return render_template('onetonline_job.html', job=data)


@app.route('/onet/job/<job_id>/detail/key/<value>')
def onet_jobdata_key(job_id, value):
    filedata = None
    with open('fixtures/onet_jobs/{}.json'.format(job_id), 'rb') as currfile:
        filedata = dict(json.loads(currfile.read())[0])
        data = filedata[value]
    if 'as_json' in request.args:
        return json.dumps(data)
    context = {
        'data': data,
        'back_url': '/onet/job/{}/detail'.format(job_id),
        'heading': 'Job: ' + job_id
    }
    return render_template('json_view.html', **context)


@app.route('/careerbuilder')
def careerbuilder():
    files = CareerBuilderHelper.load_categories()
    return render_template('careerbuilder.html', files=files)


@app.route('/json/<spider>/<jobfile>', methods=['GET'])
def getjson(spider='onet_jobs', jobfile=None):
    try:
        # Dangerous! Arbitrary file system access can be very dangerous.
        # Proceed with caution for production setups... you've been warned.
        with open('data/{}/{}'.format(spider, jobfile), 'rb') as data:
            return data.read()
    except IOError:
            return json.dumps({
                'error': 'No JSON file could be found with that name.'})

if __name__ == '__main__':
    app.run()
