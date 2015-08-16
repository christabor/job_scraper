import json
from flask import Flask
from flask import render_template
import helpers


app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    files = helpers.load_all_categories()
    return render_template('index.html', files=files)


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
