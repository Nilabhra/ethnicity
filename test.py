import pickle

gender_classifier = pickle.load(open('gender_classifier.pkl', 'r'))
religion_classifier = pickle.load(open('religion_classifier.pkl', 'r'))
ethnicity_classifier_last_name = pickle.load(open('ethnicity_classifier_last_name.pkl', 'r'))
ethnicity_classifier_first_name = pickle.load(open('ethnicity_classifier_first_name.pkl', 'r'))

def gender_features(name):
    name = name.lower()
    first_name = name.split()[0]
    last_name = name.split()[-1]
    
    first_name_first = first_name[0]
    first_name_first_two = first_name[:2] if len(first_name) > 1 else None
    first_name_first_three = first_name[:3] if len(first_name) > 2 else None
    first_name_first_four = first_name[:4] if len(first_name) > 3 else None
    first_name_first_five = first_name[:5] if len(first_name) > 4 else None
    
    first_name_last = first_name[-1]
    first_name_last_two = first_name[-2:] if len(first_name) > 1 else None
    first_name_last_three = first_name[-3:] if len(first_name) > 2 else None
    first_name_last_four = first_name[-4:] if len(first_name) > 3 else None
    first_name_last_five = first_name[-5:] if len(first_name) > 4 else None
    
    if first_name != last_name:
        last_name_first = last_name[0]
        last_name_first_two = last_name[:2] if len(last_name) > 1 else None
        last_name_first_three = last_name[:3] if len(last_name) > 2 else None
        last_name_first_four = last_name[:4] if len(last_name) > 3 else None
        last_name_first_five = last_name[:5] if len(last_name) > 4 else None
        
        last_name_last = last_name[-1]
        last_name_last_two = last_name[-2:] if len(last_name) > 1 else None
        last_name_last_three = last_name[-3:] if len(last_name) > 2 else None
        last_name_last_four = last_name[-4:] if len(last_name) > 3 else None
        last_name_last_five = last_name[-5:] if len(last_name) > 4 else None
    else:
        last_name_first = None
        last_name_first_two = None
        last_name_first_three = None
        last_name_first_four = None
        last_name_first_five = None
        
        last_name_last = None
        last_name_last_two = None
        last_name_last_three = None
        last_name_last_four = None
        last_name_last_five = None
    
    features = {'first_name_first': first_name_first, 'first_name_first_two': first_name_first_two,
                'first_name_first_three': first_name_first_three, 'first_name_first_four': first_name_first_four,
                'first_name_first_five': first_name_first_five,
                'first_name_last': first_name_last, 'first_name_last_two': first_name_last_two,
                'first_name_last_three': first_name_last_three, 'first_name_last_four': first_name_last_four,
                'first_name_last_five': first_name_last_five,
                'last_name_first': last_name_first, 'last_name_first_two': last_name_first_two,
                'last_name_first_three': last_name_first_three, 'last_name_first_four': last_name_first_four,
                'last_name_last_five': last_name_first_five,
                'last_name_last': last_name_last, 'last_name_last_two': last_name_last_two,
                'last_name_last_three': last_name_last_three, 'last_name_last_four': last_name_last_four,
                'last_name_last_five': last_name_last_five}
    
    return features

#Note: These are useful for distinguishing between Muslim, Christian and Hindu names, but not for Hindu/Sikh/Jain/Buddhist names
def religion_features(name):
    name = name.lower()
    first_name = name.split()[0]
    last_name = name[len(first_name):].lstrip().rstrip()
    
    first_name_first = first_name[0]
    first_name_first_two = first_name[:2] if len(first_name) > 1 else None
    first_name_first_three = first_name[:3] if len(first_name) > 2 else None
    first_name_first_four = first_name[:4] if len(first_name) > 3 else None
    
    first_name_last = first_name[-1]
    first_name_last_two = first_name[-2:] if len(first_name) > 1 else None
    first_name_last_three = first_name[-3:] if len(first_name) > 2 else None
    first_name_last_four = first_name[-4:] if len(first_name) > 3 else None
    
    if first_name != last_name and len(last_name) > 0:
        last_name_first = last_name[0]
        last_name_first_two = last_name[:2] if len(last_name) > 1 else None
        last_name_first_three = last_name[:3] if len(last_name) > 2 else None
        last_name_first_four = last_name[:4] if len(last_name) > 3 else None
        
        last_name_last = last_name[-1]
        last_name_last_two = last_name[-2:] if len(last_name) > 1 else None
        last_name_last_three = last_name[-3:] if len(last_name) > 2 else None
        last_name_last_four = last_name[-4:] if len(last_name) > 3 else None
    else:
        last_name_first = None
        last_name_first_two = None
        last_name_first_three = None
        last_name_first_four = None
        
        last_name_last = None
        last_name_last_two = None
        last_name_last_three = None
        last_name_last_four = None
    
    features = {'prop_%s'%i: 1.*name.count(i)/len(name) for i in 'abcdefghijklmnopqrstuvwxyz'}
    features.update({'first_name_first': first_name_first, 'first_name_first_two': first_name_first_two,'first_name_first_three': first_name_first_three, 'first_name_first_four': first_name_first_four,
               'first_name_last': first_name_last, 'first_name_last_two': first_name_last_two,
               'first_name_last_three': first_name_last_three, 'first_name_last_four': first_name_last_four,
               'last_name_first': last_name_first, 'last_name_first_two': last_name_first_two,
               'last_name_first_three': last_name_first_three, 'last_name_first_four': last_name_first_four,
               'last_name_last': last_name_last, 'last_name_last_two': last_name_last_two,
               'last_name_last_three': last_name_last_three, 'last_name_last_four': last_name_last_four
               })
    
    return features

def ethnicity_features(name, kind='last'):
    if kind == 'last':
        if name is not None:
            name = name.split()[-1]
        else:
            return {'name_first': None, 'name_first_two': None, 'name_first_three': None, 'name_first_four': None,
                'name_last': None, 'name_last_two': None, 'name_last_three': None, 'name_last_four': None,
                'len_name': 0}
    elif kind == 'first':
        name = name.split()[0]
    name = name.lower()
    
    name_first = name[0]
    name_first_two = name[:2]# if len(name) > 1 else None
    name_first_three = name[:3]# if len(name) > 2 else None
    name_first_four = name[:4]# if len(name) > 3 else None

    name_last = name[-1]
    name_last_two = name[-2:]# if len(name) > 1 else None
    name_last_three = name[-3:]# if len(name) > 2 else None
    name_last_four = name[-4:]# if len(name) > 3 else None
    
    features = {'name_first': name_first, 'name_first_two': name_first_two,
                'name_first_three': name_first_three, 'name_first_four': name_first_four,
                'name_last': name_last, 'name_last_two': name_last_two,
                'name_last_three': name_last_three, 'name_last_four': name_last_four,
                'len_name': len(name)}
    
    return features

def get_likely_ethnicity(f, l, confounding_surname=False):
    max_l = max(l, key=l.get)
    max_f = max(f, key=f.get)
    if not confounding_surname:
        comb = {i: 0.35*f[i] + 0.65*l[i] for i in f}
    else:
        comb = {i: 0.65*f[i] + 0.35*l[i] for i in f}
    max_comb = max(comb.values())
    if max_comb > 0.8:
        conf = 'Confident'
    elif max_comb > 0.5:
        conf = 'Somewhat Confident'
    else:
        conf = 'Not Confident'
    if max(l.values()) > 0.98 and not confounding_surname:
        return max_l, comb, 'Very Confident'
    else:
        if max_l == max_f:
            return max_l, comb, conf
        else:
            return max(comb, key=comb.get), comb, conf

name = 'Ansar Kadri'

gender = gender_classifier.prob_classify(gender_features(name)).__dict__['_prob_dict']
print 'Gender:', {i: 2**gender[i] for i in gender}

religion = religion_classifier.prob_classify(religion_features(name)).__dict__['_prob_dict']
print 'Religion:', {i: 2**religion[i] for i in religion}

d = ethnicity_classifier_first_name.prob_classify(ethnicity_features(name, kind='first')).__dict__['_prob_dict']
first_name_stats = {i: 2**d[i] for i in d}

d = ethnicity_classifier_last_name.prob_classify(ethnicity_features(name, kind='last')).__dict__['_prob_dict']
last_name_stats = {i: 2**d[i] for i in d}

is_counfounding = {'Kumar', 'Singh'}
likely_ethnicity, comb_prob, conf = get_likely_ethnicity(first_name_stats, last_name_stats, 
                                                         confounding_surname = name.split()[-1] in is_counfounding)
print 'Ethnicity:', likely_ethnicity, 'Confidence:', conf