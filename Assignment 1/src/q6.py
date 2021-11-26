import json
import math
import numpy as np
import pandas as pd
import datetime as dt
from scipy.signal import find_peaks

f = open('./dist_to_key.json')
dist_to_key = json.load(f)
double_districts = ['aurangabad', 'bilaspur', 'balrampur', 'hamirpur', 'pratapgarh']

census = pd.read_excel("./DDW_PCA0000_2011_Indiastatedist.xlsx")
cowin_d = pd.read_csv("./cowin_vaccine_data_modified_districtwise.csv", low_memory=False)
cowin_s = pd.read_csv("./cowin_vaccine_data_statewise.csv", low_memory=False)
cowin_s.replace(float("NaN"), "0", inplace=True)
cowin_d.replace(float("NaN"), "0", inplace=True)
cowin_d.drop(labels=[0], axis=0, inplace=True)

state_key = sorted(set(cowin_s['State']))
state_key.remove('India')
state_key.remove('Ladakh')
state_key.remove('Telangana')
state_key.remove('Dadra and Nagar Haveli and Daman and Diu')
cowin_s[['Male (Doses Administered)', 'Female (Doses Administered)']] = cowin_s[['Male (Doses Administered)', 'Female (Doses Administered)']].astype(int)
grouped = cowin_s.groupby('State')

days_in_each_month = [30, 28, 31, 30, 31, 30, 31]
days_until_this_month = [30, 58, 89, 119, 150, 180, 211]
num_months = 7
num_weeks = 31
num_states = len(state_key)
num_districts = len(cowin_d['District_Key'])
time_id_list = np.array([1 for x in range(num_districts)])

overall_census = []
state_census = []
district_census = []

sum=0
for index, row in census.iterrows():
    if (row['TRU']!='Total'):
        continue
    if (row['Level']=='STATE'):
        state_name = row['Name']
        if state_name == 'ANDAMAN & NICOBAR ISLANDS':
            state_name = 'Andaman and Nicobar Islands'
        elif state_name == 'JAMMU & KASHMIR':
            state_name = 'Jammu and Kashmir'
        elif state_name == 'NCT OF DELHI':
            state_name = 'Delhi'
        elif state_name == 'DADRA & NAGAR HAVELI':
            continue
        elif state_name == 'DAMAN & DIU':
            continue
        state_census.append([state_name, row['TOT_P'], row['TOT_M'], row['TOT_F']])
    elif (row['Level']=='DISTRICT'):
        dist_name = row['Name'].lower()

        if dist_name == double_districts[0]:
            if state_name.lower() == 'Bihar'.lower():
                dist_name = 'BR_Aurangabad'
            else:
                dist_name = 'MH_Aurangabad'
        elif dist_name == double_districts[1]:
            if state_name.lower() == 'Chhattisgarh'.lower():
                dist_name = 'CT_Bilaspur'
            else:
                dist_name = 'HP_Bilaspur'
        elif dist_name == double_districts[2]:
            if state_name.lower() == 'Chhattisgarh'.lower():
                dist_name = 'CT_Balrampur'
            else:
                dist_name = 'UP_Balrampur'
        elif dist_name == double_districts[3]:
            if state_name.lower() == 'Himachal Pradesh'.lower():
                dist_name = 'HP_Hamirpur'
            else:
                dist_name = 'UP_Hamirpur'
        elif dist_name == double_districts[4]:
            if state_name.lower() == 'Rajasthan'.lower():
                dist_name = 'RJ_Pratapgarh'
            else:
                dist_name = 'UP_Pratapgarh'
        elif dist_name in dist_to_key:
            dist_name = dist_to_key[dist_name]
        else:
            sum += 1
            continue
        district_census.append([dist_name, row['TOT_P'], row['TOT_M'], row['TOT_F']])
    else:
        overall_census.append([row['Name'], row['TOT_P'], row['TOT_M'], row['TOT_F']])

districts_from_census = [x[0] for x in district_census]
districts_from_cowin = cowin_d['District_Key']

# common_districts = []
districts_dose_ratio = []
districts_all_ratio = []
for index, row in cowin_d.iterrows():
    if(row['District_Key'] in districts_from_census):
        districts_dose_ratio.append([row['District_Key'], float(cowin_d.iloc[index, days_until_this_month[num_months-1]*10+2])/float(cowin_d.iloc[index, days_until_this_month[num_months-1]*10+1])])

for row in districts_dose_ratio:
    index = districts_from_census.index(row[0])
    pop_ratio = float(district_census[index][3])/float(district_census[index][2])
    districts_all_ratio.append([row[0], row[1], pop_ratio, row[1]/pop_ratio])

district_data = pd.DataFrame(districts_all_ratio, columns = ['districtid', 'vaccinationratio', 'populationratio', 'ratioofratios'])
district_data.sort_values(by=['ratioofratios'], inplace=True)
district_data.to_csv('./output/district-vaccination-population-ratio.csv', index=False)

states_from_census = [x[0].lower() for x in state_census]
states_from_cowin = state_key

states_dose_ratio = []
states_all_ratio = []
for state in states_from_cowin:
    df = grouped.get_group(state)
    states_dose_ratio.append([state, float(df.iloc[days_until_this_month[num_months-1]-1]['Female (Doses Administered)'])/float(df.iloc[days_until_this_month[num_months-1]-1]['Male (Doses Administered)'])])

for row in states_dose_ratio:
    index = states_from_census.index(row[0].lower())
    pop_ratio = float(state_census[index][3])/float(state_census[index][2])
    states_all_ratio.append([row[0], row[1], pop_ratio, row[1]/pop_ratio])

state_data = pd.DataFrame(states_all_ratio, columns = ['stateid', 'vaccinationratio', 'populationratio', 'ratioofratios'])
state_data.sort_values(by=['ratioofratios'], inplace=True)
state_data.to_csv('./output/state-vaccinated-population-ratio.csv', index=False)

overall_dose_ratio = []
overall_all_ratio = []

df = grouped.get_group('India')
overall_dose_ratio.append(['India', float(df.iloc[days_until_this_month[num_months-1]-1]['Female (Doses Administered)'])/float(df.iloc[days_until_this_month[num_months-1]-1]['Male (Doses Administered)'])])

for row in overall_dose_ratio:
    index = 0
    pop_ratio = float(overall_census[index][3])/float(overall_census[index][2])
    overall_all_ratio.append([row[0], row[1], pop_ratio, row[1]/pop_ratio])

overall_data = pd.DataFrame(overall_all_ratio, columns = ['overallid', 'vaccinationratio', 'populationratio', 'ratioofratios'])
overall_data.sort_values(by=['ratioofratios'], inplace=True)
overall_data.to_csv('./output/overall-vaccinated-population-ratio.csv', index=False)
