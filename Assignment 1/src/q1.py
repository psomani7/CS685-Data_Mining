import numpy as np
import pandas as pd
import json

f = open('./neighbor-districts.json')
data = json.load(f)
remove_as_per_ques = ['kheri', 'noklak', 'konkan_division', 'niwari', 'parbhani', 'pattanamtitta']

alter = pd.read_csv('./alter.csv', low_memory=False)
alter_list = alter.to_dict('split')['data']
alter_dict = {}
for _ in alter_list:
    alter_dict[_[0]] = _[1]

new_data = {}
for key, value in data.items():

    new_value = []
    for _ in value:
        name = _.split('/')[0].split('_district')[0]
        code = _.split('/')[1]
        if name not in remove_as_per_ques:
            if name in alter_dict:
                new_value.append(alter_dict[name] + "/" + code)
            else:
                new_value.append(name + "/" + code)

    name = key.split('/')[0].split('_district')[0]
    code = key.split('/')[1]
    if name not in remove_as_per_ques:
        if name in alter_dict:
            new_data[alter_dict[name] + "/" + code] = new_value
        else:
            new_data[name + "/" + code] = new_value

f = open('./dist_to_key.json')
dict_dist_to_key = json.load(f)

final_data = {}
for dist, value in new_data.items():

    new_value = []
    for neighbour in value:
        code = neighbour.split('/')[1]
        neighbour = neighbour.split('/')[0]
        neighbour = neighbour.lower()
        neighbour = neighbour.replace("_", " ")
        neighbour = neighbour.replace("-", " ")
        neighbour = neighbour.replace("–", " ")
        if code in dict_dist_to_key:
            new_value.append(dict_dist_to_key[code])
        elif neighbour in dict_dist_to_key:
            new_value.append(dict_dist_to_key[neighbour])

    code = dist.split('/')[1]
    dist = dist.split('/')[0]
    dist = dist.lower()
    dist = dist.replace("_", " ")
    dist = dist.replace("-", " ")
    dist = dist.replace("–", " ")
    if code in dict_dist_to_key:
        final_data[dict_dist_to_key[code]] = new_value
    elif dist in dict_dist_to_key:
        final_data[dict_dist_to_key[dist]] = new_value

with open('./neighbor-districts-modified.json', 'w') as f:
    json.dump(dict(sorted(final_data.items())), f, indent="\t")