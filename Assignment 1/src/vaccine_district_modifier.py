import json
import numpy as np
import pandas as pd

cowin = pd.read_csv('./cowin_vaccine_data_districtwise.csv', low_memory=False)
cowin.replace(float("NaN"), "0", inplace=True)

dists = []
repeated_dist = []
repeated_index = []
d = {}
for index, row in cowin.iterrows():
    if row[3] in dists:
        repeated_dist.append(row[3])
        repeated_index.append(index)
        d[row[3]] = index
    else:
        dists.append(row[3])

cowin_modified = cowin.drop(repeated_index, inplace=False)

for index, row in cowin_modified.iterrows():
    if row[3] in repeated_dist:
        dup = d[row[3]]
        for i in range(6, len(row)):
            row[i] = int(row[i]) + int(cowin.iloc[dup, i])

cowin_modified.to_csv('./cowin_vaccine_data_modified_districtwise.csv', index=False)

dict_dist_to_key = {}
for index, row in cowin_modified.iterrows():
    dist = row[5]
    dist = dist.lower()
    dist = dist.replace("_", " ")
    dist = dist.replace("-", " ")
    dist = dist.replace("–", " ")
    
    dict_dist_to_key[dist] = row[3]

dict_dist_to_key['Q43086'] = 'BR_Aurangabad'
dict_dist_to_key['Q100157'] = 'CT_Bilaspur'
dict_dist_to_key['Q16056268'] = 'CT_Balrampur'
dict_dist_to_key['Q2086180'] = 'HP_Hamirpur'
dict_dist_to_key['Q1585433'] = 'RJ_Pratapgarh'

with open('./dist_to_key.json', 'w') as f:
    json.dump(dict(sorted(dict_dist_to_key.items())) ,f,indent = "\t")