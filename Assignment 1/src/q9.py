import numpy as np
import pandas as pd
import datetime as dt
import math


census = pd.read_excel("./DDW_PCA0000_2011_Indiastatedist.xlsx")
cowin_s = pd.read_csv("./cowin_vaccine_data_statewise.csv", low_memory=False)
cowin_s.replace(float("NaN"), "0", inplace=True)

state_key = sorted(set(cowin_s['State']))
state_key.remove('India')
state_key.remove('Ladakh')
state_key.remove('Telangana')
state_key.remove('Dadra and Nagar Haveli and Daman and Diu')
cowin_s[['First Dose Administered']] = cowin_s[['First Dose Administered']].astype(float)
grouped = cowin_s.groupby('State')

days_in_each_month = [30, 28, 31, 30, 31, 30, 31]
days_until_this_month = [30, 58, 89, 119, 150, 180, 211]
num_months = 7
num_weeks = 31
end_date = dt.date(2021, 8, 14)

state_census = []

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
    else:
        continue

states_from_census = [x[0].lower() for x in state_census]
states_from_cowin = state_key

states_vaccine_data = []
states_full_data = []
for state in states_from_cowin:
    df = grouped.get_group(state)
    states_vaccine_data.append([state, df.iloc[days_until_this_month[num_months-1]-1]['First Dose Administered'],
                                df.iloc[days_until_this_month[num_months-1]-1]['First Dose Administered'] - df.iloc[days_until_this_month[num_months-1]-8]['First Dose Administered']])

for row in states_vaccine_data:
    index = states_from_census.index(row[0].lower())
    pop_left = float(state_census[index][1])- row[1]
    rate_day = row[2]/7
    delta = math.ceil(pop_left/rate_day)
    expected_date = end_date + dt.timedelta(days = delta)
    states_full_data.append([row[0], pop_left, row[2], expected_date.strftime("%d-%m-%y")])

state_data = pd.DataFrame(states_full_data, columns = ['stateid', 'populationleft', 'rateofvaccination', 'date'])
state_data.to_csv('./output/complete-vaccincation.csv', index=False)