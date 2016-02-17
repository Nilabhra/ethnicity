import os
from flask import Flask, request, jsonify, make_response, render_template, render_template_string
import pickle
import json
from utils import gender_features, religion_features, ethnicity_features, get_likely_ethnicity

app = Flask(__name__)
gender_classifier = pickle.load(open('models/gender_classifier.pkl', 'r'))
religion_classifier = pickle.load(open('models/religion_classifier.pkl', 'r'))
ethnicity_classifier_last_name = pickle.load(open('models/ethnicity_classifier_last_name.pkl', 'r'))
ethnicity_classifier_first_name = pickle.load(open('models/ethnicity_classifier_first_name.pkl', 'r'))

first_name_cbse_counts = json.load(open('json_counts/first_name_cbse_counts.json', 'r'))
last_name_cbse_counts = json.load(open('json_counts/last_name_cbse_counts.json', 'r'))
first_name_gender = json.load(open('json_counts/first_name_gender.json', 'r'))
last_name_gender = json.load(open('json_counts/last_name_gender.json', 'r'))

first_name_simply_marry_counts = json.load(open('json_counts/first_name_simply_marry_counts.json', 'r'))
last_name_simply_marry_counts = json.load(open('json_counts/last_name_simply_marry_counts.json', 'r'))
first_name_religion = json.load(open('json_counts/first_name_religion.json', 'r'))
last_name_religion = json.load(open('json_counts/last_name_religion.json', 'r'))

def get_results(name):
    name = name.lower()
    first_name = name.split()[0]
    last_name = name.split()[-1] if ' ' in name else ''

    if first_name_cbse_counts.get(first_name, 0) >= 25 and max(first_name_gender[first_name].values()) > 0.98:
        gender = first_name_gender[first_name]
    elif last_name_cbse_counts.get(last_name, 0) >= 25 and max(last_name_gender[last_name].values()) > 0.98:
        gender = last_name_gender[last_name]
    else:
        gender = gender_classifier.prob_classify(gender_features(name)).__dict__['_prob_dict']
        gender = {i: 2**gender[i] for i in gender}

    if last_name_simply_marry_counts.get(last_name, 0) >= 5 and max(last_name_religion[last_name].values()) > 0.98:
        religion = last_name_religion[last_name]
    else:
        religion = religion_classifier.prob_classify(religion_features(name)).__dict__['_prob_dict']
        religion = {i: 2**religion[i] for i in religion}
    
    d = ethnicity_classifier_first_name.prob_classify(ethnicity_features(name, kind='first')).__dict__['_prob_dict']
    first_name_stats = {i: 2**d[i] for i in d}
    d = ethnicity_classifier_last_name.prob_classify(ethnicity_features(name, kind='last')).__dict__['_prob_dict']
    last_name_stats = {i: 2**d[i] for i in d}
    is_confounding = {'Kumar', 'Singh'}
    likely_ethnicity, comb_prob, conf = get_likely_ethnicity(first_name_stats, last_name_stats, 
                                                             confounding_surname = last_name in is_confounding)
    return {'gender_results': gender,
            'religion_results': religion,
            'likely_ethnicity': likely_ethnicity, 'confidence_ethnicity': conf}

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
    	return render_template('index.html')
    else:
    	name = request.form.get('name')
    	results = get_results(name)
        likely_gender = max(results['gender_results'], key=results['gender_results'].get)
        gender_prob = 100*max(results['gender_results'].values())
        if gender_prob == 100: gender_prob = 99.99
        likely_religion = max(results['religion_results'], key=results['religion_results'].get)
        religion_prob = 100*max(results['religion_results'].values())
        if religion_prob == 100: religion_prob = 99.99
    	return render_template('results.html',
            likely_gender = likely_gender.title(),
            gender_prob = gender_prob,
            likely_religion = likely_religion.title(),
            religion_prob = religion_prob,
            likely_ethnicity = results['likely_ethnicity'].title(),
            confidence_ethnicity = results['confidence_ethnicity'].title())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
