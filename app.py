import os
from flask import Flask, request, jsonify, make_response, render_template, render_template_string
import pickle
from utils import gender_features, religion_features, ethnicity_features, get_likely_ethnicity

app = Flask(__name__)
gender_classifier = pickle.load(open('models/gender_classifier.pkl', 'r'))
religion_classifier = pickle.load(open('models/religion_classifier.pkl', 'r'))
ethnicity_classifier_last_name = pickle.load(open('models/ethnicity_classifier_last_name.pkl', 'r'))
ethnicity_classifier_first_name = pickle.load(open('models/ethnicity_classifier_first_name.pkl', 'r'))

def get_results(name):
    gender = gender_classifier.prob_classify(gender_features(name)).__dict__['_prob_dict']
    religion = religion_classifier.prob_classify(religion_features(name)).__dict__['_prob_dict']
    
    d = ethnicity_classifier_first_name.prob_classify(ethnicity_features(name, kind='first')).__dict__['_prob_dict']
    first_name_stats = {i: 2**d[i] for i in d}
    d = ethnicity_classifier_last_name.prob_classify(ethnicity_features(name, kind='last')).__dict__['_prob_dict']
    last_name_stats = {i: 2**d[i] for i in d}

    is_counfounding = {'Kumar', 'Singh'}
    likely_ethnicity, comb_prob, conf = get_likely_ethnicity(first_name_stats, last_name_stats, 
                                                             confounding_surname = name.split()[-1] in is_counfounding)
    return {'gender_results': {i: 2**gender[i] for i in gender},
            'religion_results': {i: 2**religion[i] for i in religion},
            'likely_ethnicity': likely_ethnicity, 'confidence_ethnicity': conf}

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
    	return render_template('index.html')
    else:
    	name = request.form.get('name')
    	results = get_results(name)
        likely_gender = max(results['gender_results'], key=results['gender_results'].get)
        likely_religion = max(results['religion_results'], key=results['religion_results'].get)
    	return render_template('results.html', likely_gender = likely_gender.title(),
            likely_religion = likely_religion.title(),
            likely_ethnicity = results['likely_ethnicity'].title(),
            confidence_ethnicity = results['confidence_ethnicity'].title())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)