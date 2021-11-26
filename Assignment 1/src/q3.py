import json
import math
import numpy as np
import pandas as pd
import datetime as dt

covid = pd.read_csv("./districts.csv", low_memory=False)
covid.replace(float("NaN"), "", inplace=True)

f = open('./dist_to_key.json')
dist_to_key = json.load(f)

double_districts = ['aurangabad', 'bilaspur', 'balrampur', 'hamirpur', 'pratapgarh']

start_date = dt.date(2020, 3, 15)
end_date = dt.date(2021, 8, 14)
week_start1 = start_date-dt.timedelta(days=1)
week_end1 = end_date
week_start2 = start_date+dt.timedelta(days=3)
week_end2 = end_date-dt.timedelta(days=3)
month_start = start_date-dt.timedelta(days=1)

num_weeks = (int)((week_end2 - week_start2 + week_end1 - week_start1).days/7)
num_months = 17

covid_state = covid['State']
covid_district = covid['District']
covid_id = []
for i in range(len(covid_district)):
    state = covid_state[i]
    dist = covid_district[i]
    dist = dist.lower()
    dist = dist.replace("_", " ")
    dist = dist.replace("-", " ")
    dist = dist.replace("–", " ")

    if dist==double_districts[0]:
        if state=='Bihar':
            covid_id.append('BR_Aurangabad')
        else:
            covid_id.append('MH_Aurangabad')
    elif dist==double_districts[1]:
        if state=='Chhattisgarh':
            covid_id.append('CT_Bilaspur')
        else:
            covid_id.append('HP_Bilaspur')
    elif dist==double_districts[2]:
        if state=='Chhattisgarh':
            covid_id.append('CT_Balrampur')
        else:
            covid_id.append('UP_Balrampur')
    elif dist==double_districts[3]:
        if state=='Himachal Pradesh':
            covid_id.append('HP_Hamirpur')
        else:
            covid_id.append('UP_Hamirpur')
    elif dist==double_districts[4]:
        if state=='Rajasthan':
            covid_id.append('RJ_Pratapgarh')
        else:
            covid_id.append('UP_Pratapgarh')
    elif dist in dist_to_key:
        covid_id.append(dist_to_key[dist])
    else:
        covid_id.append('SKIP')

covid['id'] = covid_id
District_id = sorted(set(covid['id']) - set(['SKIP']))
num_districts = len(District_id)

dataframes_weeks = []
cases_weeks = []
for i in range(1, num_weeks+1):
    data = [[x, i] for x in District_id]
    df = pd.DataFrame(data, columns = ['districtid', 'timeid'])
    dataframes_weeks.append(df)
    data = [0 for x in District_id]
    cases_weeks.append(data)

dataframes_months = []
cases_months = []
for i in range(1, num_months+1):
    data = [[x, i] for x in District_id]
    df = pd.DataFrame(data, columns = ['districtid', 'timeid'])
    dataframes_months.append(df)
    data = [0 for x in District_id]
    cases_months.append(data)

data = [[x, 1] for x in District_id]
dataframe_overall = pd.DataFrame(data, columns = ['districtid', 'timeid'])
cases_overall = [0 for x in District_id]

for index,row in covid.iterrows():
    date = dt.datetime.strptime(row['Date'], '%Y-%m-%d').date()
    if(date > end_date):
        break
    if row['id'] in District_id:
        index = District_id.index(row['id'])
    else:
        continue
    if(date <= week_end1):
        curr_week1 = (math.ceil((date - week_start1).days/7)-1)*2
        cases_weeks[curr_week1][index] = row['Confirmed']
    if(date <= week_end2):
        curr_week2 = math.ceil((date - week_start2).days/7)*2-1
        cases_weeks[curr_week2][index] = row['Confirmed']
    curr_month = 12*(date.year - month_start.year) + (date.month - month_start.month)
    if(date.day < 15):
        curr_month -= 1
    cases_months[curr_month][index] = row['Confirmed']
    cases_overall[index] = row['Confirmed']



for i in range(num_weeks):
    if(i>1):
        dataframes_weeks[i]['cases'] = np.maximum(np.array(cases_weeks[i])-np.array(cases_weeks[i-2]), np.zeros(len(District_id)))
    else:
        dataframes_weeks[i]['cases'] = np.array(cases_weeks[i])
for i in range(num_months):
    if(i>0):
        dataframes_months[i]['cases'] = np.maximum(np.array(cases_months[i])-np.array(cases_months[i-1]), np.zeros(len(District_id)))
    else:
        dataframes_months[i]['cases'] = np.array(cases_months[i])
dataframe_overall['cases'] = np.array(cases_overall)

dataframe_weeks = pd.concat(dataframes_weeks)
dataframe_months = pd.concat(dataframes_months)

dataframe_weeks['cases'] = dataframe_weeks['cases'].astype(int)
dataframe_months['cases'] = dataframe_months['cases'].astype(int)
dataframe_overall['cases'] = dataframe_overall['cases'].astype(int)

dataframe_weeks.sort_values(by = ['districtid', 'timeid'], inplace=True)
dataframe_months.sort_values(by = ['districtid', 'timeid'], inplace=True)
dataframe_overall.sort_values(by = ['districtid', 'timeid'], inplace=True)

dataframe_weeks.to_csv('./output/cases-week.csv', index=False)
dataframe_months.to_csv('./output/cases-month.csv', index=False)
dataframe_overall.to_csv('./output/cases-overall.csv', index=False)