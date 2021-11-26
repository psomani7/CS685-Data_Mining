import json
import math
import numpy as np
import pandas as pd
import datetime as dt

from scipy.signal import find_peaks

covid = pd.read_csv("./districts.csv", low_memory=False)
covid.replace(float("NaN"), "0", inplace=True)
covid['Confirmed'] = covid['Confirmed'].astype(int)

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
days_in_each_month = [31, 30, 31, 30, 31, 31, 30, 31, 31, 31, 31, 28, 31, 30, 31, 31, 31]

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

State_id = sorted(set(covid['State']))
num_states = len(State_id)

dataframes_overall_weeks = []
cases_overall_weeks = []
dataframes_state_weeks = []
cases_state_weeks = []
dataframes_district_weeks = []
cases_district_weeks = []

dataframes_overall_months = []
cases_overall_months = []
dataframes_state_months = []
cases_state_months = []
dataframes_district_months = []
cases_district_months = []

for i in range(num_states):
    
    data = [[State_id[i], x] for x in range(1, num_weeks+1)]
    df = pd.DataFrame(data, columns = ['stateid', 'timeid'])
    dataframes_state_weeks.append(df)
    data = [0 for x in range(1, num_weeks+1)]
    cases_state_weeks.append(data)

    data = [[State_id[i], x] for x in range(1, num_months+1)]
    df = pd.DataFrame(data, columns = ['stateid', 'timeid'])
    dataframes_state_months.append(df)
    data = [0 for x in range(1, num_months+1)]
    cases_state_months.append(data)

for i in range(num_districts):

    data = [[District_id[i], x] for x in range(1, num_weeks+1)]
    df = pd.DataFrame(data, columns = ['districtid', 'timeid'])
    dataframes_district_weeks.append(df)
    data = [0 for x in range(1, num_weeks+1)]
    cases_district_weeks.append(data)

    data = [[District_id[i], x] for x in range(1, num_months+1)]
    df = pd.DataFrame(data, columns = ['districtid', 'timeid'])
    dataframes_district_months.append(df)
    data = [0 for x in range(1, num_months+1)]
    cases_district_months.append(data)

data = [['India', x] for x in range(1, num_weeks+1)]
df = pd.DataFrame(data, columns = ['overallid', 'timeid'])
dataframes_overall_weeks.append(df)
data = [0 for x in range(1, num_weeks+1)]
cases_overall_weeks.append(data)

data = [['India', x] for x in range(1, num_months+1)]
df = pd.DataFrame(data, columns = ['overallid', 'timeid'])
dataframes_overall_months.append(df)
data = [0 for x in range(1, num_months+1)]
cases_overall_months.append(data)

for index,row in covid.iterrows():
    date = dt.datetime.strptime(row['Date'], '%Y-%m-%d').date()
    if(date > end_date):
        break
    if(row['id']=='SKIP'):
        continue
    d_id = District_id.index(row['id'])
    s_id = State_id.index(row['State'])
    active_case = row['Confirmed'] - row['Recovered'] - row['Deceased']
    if(date <= week_end1):
        curr_week1 = (math.ceil((date - week_start1).days/7)-1)*2
        cases_overall_weeks[0][curr_week1] += active_case
        cases_state_weeks[s_id][curr_week1] += active_case
        cases_district_weeks[d_id][curr_week1] += active_case
    if(date <= week_end2):
        curr_week2 = math.ceil((date - week_start2).days/7)*2-1
        cases_overall_weeks[0][curr_week2] += active_case
        cases_state_weeks[s_id][curr_week2] += active_case
        cases_district_weeks[d_id][curr_week2] += active_case
    curr_month = 12*(date.year - month_start.year) + (date.month - month_start.month)
    if(date.day < 15):
        curr_month -= 1
    cases_overall_months[0][curr_month] += active_case
    cases_state_months[s_id][curr_month] += active_case
    cases_district_months[d_id][curr_month] += active_case

cases_overall_weeks = np.array(cases_overall_weeks)/7
cases_overall_months = np.array(cases_overall_months)/days_in_each_month
cases_state_weeks = np.array(cases_state_weeks)/7
cases_state_months = np.array(cases_state_months)/days_in_each_month
cases_district_weeks = np.array(cases_district_weeks)/7
cases_district_months = np.array(cases_district_months)/days_in_each_month

for i in range(num_districts):
    dataframes_district_weeks[i]['Cases'] = cases_district_weeks[i]
    dataframes_district_months[i]['Cases'] = cases_district_months[i]

for i in range(num_states):
    dataframes_state_weeks[i]['Cases'] = cases_state_weeks[i]
    dataframes_state_months[i]['Cases'] = cases_state_months[i]

dataframes_overall_weeks[0]['Cases'] = cases_overall_weeks[0]
dataframes_overall_months[0]['Cases'] = cases_overall_months[0]

def get_month_peaks(df, index, type):
    peak1 =df['Cases'][0:10].idxmax()+1
    peak2 =df['Cases'][10:].idxmax()+1
    return peak1, peak2

def get_week_peaks(df, index, type):
    peak1 =df['Cases'][:80].idxmax()+1
    peak2 =df['Cases'][80:].idxmax()+1
    return peak1, peak2

district_weeks_peak1 = []
district_weeks_peak2 = []
district_months_peak1 = []
district_months_peak2 = []

for i in range(num_districts):
    df = dataframes_district_weeks[i]
    peak1, peak2 = get_week_peaks(df, i, 0)
    district_weeks_peak1.append(peak1)
    district_weeks_peak2.append(peak2)
    df = dataframes_district_months[i]
    peak1, peak2 = get_month_peaks(df, i, 0)
    district_months_peak1.append(peak1)
    district_months_peak2.append(peak2)

state_weeks_peak1 = []
state_weeks_peak2 = []
state_months_peak1 = []
state_months_peak2 = []

for i in range(num_states):
    df = dataframes_state_weeks[i]
    peak1, peak2 = get_week_peaks(df, i, 1)
    state_weeks_peak1.append(peak1)
    state_weeks_peak2.append(peak2)
    df = dataframes_state_months[i]
    peak1, peak2 = get_month_peaks(df, i, 1)
    state_months_peak1.append(peak1)
    state_months_peak2.append(peak2)

overall_weeks_peak1 = []
overall_weeks_peak2 = []
overall_months_peak1 = []
overall_months_peak2 = []

df = dataframes_overall_weeks[0]
peak1, peak2 = get_week_peaks(df, 0, 2)
overall_weeks_peak1.append(peak1)
overall_weeks_peak2.append(peak2)
df = dataframes_overall_months[0]
peak1, peak2 = get_month_peaks(df, 0, 2)
overall_months_peak1.append(peak1)
overall_months_peak2.append(peak2)

district_peaks = pd.DataFrame(District_id, columns=['districtid'])
state_peaks = pd.DataFrame(State_id, columns=['stateid'])
overall_peaks = pd.DataFrame(['India'], columns=['overallid'])

district_peaks['wave1-weekid'] = district_weeks_peak1
district_peaks['wave2-weekid'] = district_weeks_peak2
district_peaks['wave1-monthid'] = district_months_peak1
district_peaks['wave2-monthid'] = district_months_peak2

state_peaks['wave1-weekid'] = state_weeks_peak1
state_peaks['wave2-weekid'] = state_weeks_peak2
state_peaks['wave1-monthid'] = state_months_peak1
state_peaks['wave2-monthid'] = state_months_peak2

overall_peaks['wave1-weekid'] = overall_weeks_peak1
overall_peaks['wave2-weekid'] = overall_weeks_peak2
overall_peaks['wave1-monthid'] = overall_months_peak1
overall_peaks['wave2-monthid'] = overall_months_peak2

district_peaks.to_csv('./output/district-peaks.csv',index=False)
state_peaks.to_csv('./output/state-peaks.csv',index=False)
overall_peaks.to_csv('./output/overall-peaks.csv',index=False)