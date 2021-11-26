import numpy as np
import pandas as pd
import datetime as dt
import math

cowin_d = pd.read_csv("./cowin_vaccine_data_modified_districtwise.csv", low_memory=False)
cowin_s = pd.read_csv("./cowin_vaccine_data_statewise.csv", low_memory=False)
cowin_s.replace(float("NaN"), "0", inplace=True)
cowin_d.replace(float("NaN"), "0", inplace=True)
cowin_d.drop(labels=[0], axis=0, inplace=True)

state_key = sorted(set(cowin_s['State']))
state_key.remove('India')
cowin_s[['Covaxin (Doses Administered)', 'CoviShield (Doses Administered)']] = cowin_s[['Covaxin (Doses Administered)', 'CoviShield (Doses Administered)']].astype(int)
grouped = cowin_s.groupby('State')

days_in_each_month = [30, 28, 31, 30, 31, 30, 31]
days_until_this_month = [30, 58, 89, 119, 150, 180, 211]
num_months = 7
num_weeks = 31
num_states = len(state_key)
num_districts = len(cowin_d['District_Key'])
time_id_list = np.array([1 for x in range(num_districts)])

districts_covaxin = cowin_d.iloc[:, [days_until_this_month[num_months-1]*10+4]].astype(float)
districts_covishield = cowin_d.iloc[:, [days_until_this_month[num_months-1]*10+5]].astype(float)
district_data = pd.DataFrame(cowin_d['District_Key'], columns=['District_Key'])
district_data['vaccineratio'] =  np.divide(districts_covishield, districts_covaxin)

district_data.rename(columns = {'District_Key':'districtid'}, inplace=True)
district_data.sort_values(by=['vaccineratio', 'districtid'], inplace=True)
district_data.replace(float("inf"), "NA", inplace=True)
district_data.to_csv('./output/district-vaccine-type-ratio.csv', index=False)

state_data = []
for a_state in state_key:
    df = grouped.get_group(a_state)
    state_covaxin = df.iloc[days_until_this_month[num_months-1]-1]['Covaxin (Doses Administered)'].astype(float)
    state_covishield = df.iloc[days_until_this_month[num_months-1]-1]['CoviShield (Doses Administered)'].astype(float)
    if state_covaxin==0:
        data = [a_state, float("inf")]
    else:
        data = [a_state, state_covishield/state_covaxin]
    state_data.append(data)
state_data = pd.DataFrame(state_data, columns=['stateid', 'vaccineratio'])

state_data.sort_values(by=['vaccineratio'], inplace=True)
state_data.replace(float("inf"), "NA", inplace=True)
state_data.to_csv('./output/state-vaccine-type-ratio.csv', index=False)


df = grouped.get_group('India')
overall_covaxin = df.iloc[days_until_this_month[num_months-1]-1]['Covaxin (Doses Administered)'].astype(float)
overall_covishield = df.iloc[days_until_this_month[num_months-1]-1]['CoviShield (Doses Administered)'].astype(float)
overall_data = [['India', overall_covishield/overall_covaxin]]

overall_data = pd.DataFrame(overall_data, columns=['overallid', 'vaccineratio'])
overall_data.to_csv('./output/overall-vaccine-type-ratio.csv', index=False)