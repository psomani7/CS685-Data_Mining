import numpy as np
import pandas as pd
import datetime as dt
import math
from scipy.signal import find_peaks

cowin_d = pd.read_csv("./cowin_vaccine_data_modified_districtwise.csv", low_memory=False)
cowin_s = pd.read_csv("./cowin_vaccine_data_statewise.csv", low_memory=False)
cowin_s.replace(float("NaN"), "0", inplace=True)
cowin_d.replace(float("NaN"), "0", inplace=True)
cowin_d.drop(labels=[0], axis=0, inplace=True)

state_key = sorted(set(cowin_s['State']))
state_key.remove('India')
cowin_s[['First Dose Administered', 'Second Dose Administered']] = cowin_s[['First Dose Administered', 'Second Dose Administered']].astype(int)
grouped = cowin_s.groupby('State')

days_in_each_month = [30, 28, 31, 30, 31, 30, 31]
days_until_this_month = [30, 58, 89, 119, 150, 180, 211]
num_months = 7
num_weeks = 31
num_states = len(state_key)
num_districts = len(cowin_d['District_Key'])
time_id_list = np.array([1 for x in range(num_districts)])

dataframes_dist_weeks = []
dataframes_dist_months = []
for i in range(num_weeks):
    dataframes_dist_weeks.append(pd.DataFrame(cowin_d['District_Key'], columns=['District_Key']))
for i in range(num_months):
    dataframes_dist_months.append(pd.DataFrame(cowin_d['District_Key'], columns=['District_Key']))

for i in range(num_weeks):
    column = np.array([9+70*i])
    dataframes_dist_weeks[i]['timeid'] = time_id_list*(i+1)
    dataframes_dist_weeks[i]['dose1'] = cowin_d.iloc[:,column].astype(int)
    dataframes_dist_weeks[i]['dose2'] = cowin_d.iloc[:,column+1].astype(int)
for i in range(num_months):
    column = np.array([days_until_this_month[i]*10-1])
    dataframes_dist_months[i]['timeid'] = time_id_list*(i+1)
    dataframes_dist_months[i]['dose1'] = cowin_d.iloc[:,column].astype(int)
    dataframes_dist_months[i]['dose2'] = cowin_d.iloc[:,column+1].astype(int)

district_data_weeks = pd.concat(dataframes_dist_weeks, ignore_index=True)
district_data_months = pd.concat(dataframes_dist_months, ignore_index=True)

district_data_weeks[['dose1', 'dose2']] = district_data_weeks[['dose1', 'dose2']].diff(periods = num_districts).fillna(district_data_weeks[['dose1', 'dose2']]).astype(int)
district_data_months[['dose1', 'dose2']] = district_data_months[['dose1', 'dose2']].diff(periods = num_districts).fillna(district_data_months[['dose1', 'dose2']]).astype(int)

district_data_weeks.rename(columns = {'District_Key': 'districtid'}, inplace=True)
district_data_weeks.sort_values(by = ['districtid', 'timeid'], inplace=True)
district_data_months.rename(columns = {'District_Key': 'districtid'}, inplace=True)
district_data_months.sort_values(by = ['districtid', 'timeid'], inplace=True)

district_data_weeks.to_csv('./output/district-vaccinated-count-week.csv', index=False)
district_data_months.to_csv('./output/district-vaccinated-count-month.csv', index=False)

dataframes_state_weeks = []
dataframes_state_months = []

for a_state in state_key:
    df = grouped.get_group(a_state)
    data = [[a_state, i+1, df.iloc[7*i]['First Dose Administered'], df.iloc[7*i]['Second Dose Administered']] for i in range(num_weeks)]
    df_weeks = pd.DataFrame(data, columns = ['stateid', 'timeid', 'dose1', 'dose2'])
    df_weeks[['dose1', 'dose2']] = df_weeks[['dose1', 'dose2']].diff(1).fillna(df_weeks[['dose1', 'dose2']]).astype(int)
    dataframes_state_weeks.append(df_weeks)
    data = [[a_state, i+1, df.iloc[days_until_this_month[i]-1]['First Dose Administered'], df.iloc[days_until_this_month[i]-1]['Second Dose Administered']] for i in range(num_months)]
    df_months = pd.DataFrame(data, columns = ['stateid', 'timeid', 'dose1', 'dose2'])
    df_months[['dose1', 'dose2']] = df_months[['dose1', 'dose2']].diff(1).fillna(df_months[['dose1', 'dose2']]).astype(int)
    dataframes_state_months.append(df_months)

state_data_weeks = pd.concat(dataframes_state_weeks, ignore_index=True)
state_data_months = pd.concat(dataframes_state_months, ignore_index=True)

state_data_weeks.sort_values(by = ['stateid', 'timeid'], inplace=True)
state_data_months.sort_values(by = ['stateid', 'timeid'], inplace=True)

state_data_weeks.to_csv('./output/state-vaccinated-count-week.csv', index=False)
state_data_months.to_csv('./output/state-vaccinated-count-month.csv', index=False)

df = grouped.get_group('India')
data = [['India', i+1, df.iloc[7*i]['First Dose Administered'], df.iloc[7*i]['Second Dose Administered']] for i in range(num_weeks)]
df_weeks = pd.DataFrame(data, columns = ['overallid', 'timeid', 'dose1', 'dose2'])
df_weeks[['dose1', 'dose2']] = df_weeks[['dose1', 'dose2']].diff(1).fillna(df_weeks[['dose1', 'dose2']]).astype(int)
overall_data_weeks=df_weeks
data = [['India', i+1, df.iloc[days_until_this_month[i]-1]['First Dose Administered'], df.iloc[days_until_this_month[i]-1]['Second Dose Administered']] for i in range(num_months)]
df_months = pd.DataFrame(data, columns = ['overallid', 'timeid', 'dose1', 'dose2'])
df_months[['dose1', 'dose2']] = df_months[['dose1', 'dose2']].diff(1).fillna(df_months[['dose1', 'dose2']]).astype(int)
overall_data_months=df_months

overall_data_weeks.sort_values(by = ['overallid'], inplace=True)
overall_data_months.sort_values(by = ['overallid'], inplace=True)

overall_data_weeks.to_csv('./output/overall-vaccinated-count-week.csv', index=False)
overall_data_months.to_csv('./output/overall-vaccinated-count-month.csv', index=False)