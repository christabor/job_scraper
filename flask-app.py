import json
from flask import Flask
from flask import render_template
from helpers.careerbuilder import CareerBuilderHelper
from helpers.onetonline import OnetOnlineHelper


app = Flask(__name__)
app.debug = True


@app.template_filter('islist')
def is_list(value):
    return isinstance(value, list)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/onetonline-job/<category_id>')
def onetonline_job(category_id):
    with open('fixtures/onet_jobs/{}.json'.format(category_id), 'rb') as jobs:
        data = json.loads(jobs.read())
        jobs.close()
    return render_template('onetonline_job.html', job=data)


@app.route('/onetonline')
def onetonline():
    files = OnetOnlineHelper.read_categories()
    return render_template('onetonline.html', categories=files)


@app.route('/careerbuilder')
def careerbuilder():
    files = CareerBuilderHelper.load_categories()
    return render_template('careerbuilder.html', files=files)


@app.route('/json/<jobfile>', methods=['GET'])
def getjson(jobfile=None):
    try:
        # Dangerous! Arbitrary file system access can be very dangerous.
        # Proceed with caution for production setups... you've been warned.
        with open('data/careerbuilder/{}'.format(jobfile), 'rb') as data:
            return data.read()
    except IOError:
            return json.dumps({
                'error': 'No JSON file could be found with that name.'})

if __name__ == '__main__':
    app.run()
