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
cowin_s[['First Dose Administered', 'Second Dose Administered']] = cowin_s[['First Dose Administered', 'Second Dose Administered']].astype(float)
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

# print(sum)
districts_from_census = [x[0] for x in district_census]
districts_from_cowin = cowin_d['District_Key']

# common_districts = [value for value in districts_from_cowin if value in districts_from_cowin]
districts_doses = []
districts_ratio = []
for index, row in cowin_d.iterrows():
    if row['District_Key'] in districts_from_census:
        districts_doses.append([row['District_Key'], float(cowin_d.iloc[index, days_until_this_month[num_months-1]*10-1]), float(cowin_d.iloc[index, days_until_this_month[num_months-1]*10])])

for row in districts_doses:
    index = districts_from_census.index(row[0])
    districts_ratio.append([row[0], row[1]/district_census[index][1], row[2]/district_census[index][1]])

district_data = pd.DataFrame(districts_ratio, columns = ['districtid', 'vaccinedose1ratio', 'vaccinedose2ratio'])
district_data.sort_values(by=['vaccinedose1ratio', 'vaccinedose2ratio'], inplace=True)
district_data.to_csv('./output/district-vaccinated-dose-ratio.csv', index=False)

states_from_census = [x[0].lower() for x in state_census]
states_from_cowin = state_key

states_doses = []
states_ratio = []
for state in states_from_cowin:
    df = grouped.get_group(state)
    states_doses.append([state, df.iloc[days_until_this_month[num_months-1]-1]['First Dose Administered'], df.iloc[days_until_this_month[num_months-1]-1]['Second Dose Administered']])

for row in states_doses:
    index = states_from_census.index(row[0].lower())
    states_ratio.append([row[0], row[1]/state_census[index][1], row[2]/state_census[index][1]])

state_data = pd.DataFrame(states_ratio, columns = ['stateid', 'vaccinedose1ratio', 'vaccinedose2ratio'])
state_data.sort_values(by=['vaccinedose1ratio', 'vaccinedose2ratio'], inplace=True)
state_data.to_csv('./output/state-vaccinated-dose-ratio.csv', index=False)

overall_doses = []
overall_ratio = []

df = grouped.get_group('India')
overall_doses.append(['India', df.iloc[days_until_this_month[num_months-1]-1]['First Dose Administered'], df.iloc[days_until_this_month[num_months-1]-1]['Second Dose Administered']])

for row in overall_doses:
    index = 0
    overall_ratio.append([row[0], row[1]/overall_census[index][1], row[2]/overall_census[index][1]])

overall_data = pd.DataFrame(overall_ratio, columns = ['overallid', 'vaccinedose1ratio', 'vaccinedose2ratio'])
overall_data.sort_values(by=['vaccinedose1ratio'], inplace=True)
overall_data.to_csv('./output/overall-vaccinated-dose-ratio.csv', index=False)