import json

from flask import Flask
from flask import render_template
import csv
import os
import pandas as pd

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', name='abc')


@app.route('/names')
def names():
    df = pd.read_csv(os.path.join(APP_STATIC, 'metadata.csv'))
    data = ['%s_%s' % ('BB', val) for val in df.sort_values(by='SAMPLEID')['SAMPLEID'].tolist()]
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/otu')
def otu():
    data = []
    with open(os.path.join(APP_STATIC, 'otu.csv')) as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            data.append(row[1])

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/metadata/<sample>')
def metadata(sample):
    sample = sample.split('_')
    if len(sample) > 1:
        sample = sample[1]

    data = {}
    with open(os.path.join(APP_STATIC, 'metadata.csv')) as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            if row[0] == sample:
                data['ETHNICITY'] = row[2]
                data['GENDER'] = row[3]
                data['AGE'] = row[4]
                data['BBTYPE'] = row[6]
                data['LOCATION'] = row[7]
                data['SAMPLEID'] = row[0]

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/wfreq/<sample>')
def wfreq(sample):
    import pdb;
    pdb.set_trace()
    sample = sample.split('_')
    if len(sample) > 1:
        sample = sample[1]

    data = []
    with open(os.path.join(APP_STATIC, 'metadata.csv')) as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            if row[0] == sample:
                data.append(row[5])

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/samples/<sample>')
def sample(sample):
    data = {}
    df = pd.read_csv(os.path.join(APP_STATIC, 'samples.csv'))
    selected_sample = sample.upper()
    try:
        data['otu_ids'] = df.sort_values(by=selected_sample, ascending=False)['otu_id'].tolist()[:10]
        data['sample_values'] = df.sort_values(by=selected_sample, ascending=False)[selected_sample].tolist()[:10]
    except:
        data['sample_values'] = []
        data['otu_ids'] = []
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
