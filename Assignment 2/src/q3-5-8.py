import numpy as np
import pandas as pd
from scipy import stats
from math import isnan
import os
import glob

folder = os.getcwd()
# folder = '/content/drive/MyDrive/Sem7/DM-Ass2'
input_folder = folder + '/Input/'
output_folder = folder + '/Output/'
C08 = input_folder + 'C08/'
C14 = input_folder + 'C14/'
C17 = input_folder + 'C17/'
C18 = input_folder + 'C18/'
C19 = input_folder + 'C19/'
Census = input_folder + 'Census/'

os.chdir(C08)
files_c08 = []
for file in glob.glob("*"):
    files_c08.append(C08+file)
files_c08.sort()

os.chdir(C14)
files_c14 = []
for file in glob.glob("*"):
    files_c14.append(C14+file)
files_c14.sort()

os.chdir(C17)
files_c17 = []
for file in glob.glob("*"):
    files_c17.append(C17+file)
files_c17.sort()

os.chdir(C18)
files_c18 = []
for file in glob.glob("*"):
    files_c18.append(C18+file)
files_c18.sort()

os.chdir(C19)
files_c19 = []
for file in glob.glob("*"):
    files_c19.append(C19+file)
files_c19.sort()

os.chdir(Census)
files_census = []
for file in glob.glob("*"):
    files_census.append(Census+file)
files_census.sort()

census = pd.read_excel(files_census[0])

t_data = []
r_data = []
u_data = []
for index, row in census.iterrows():
    if (row['Level']=='DISTRICT'):
        continue
    if (row['TRU']=='Total'):
        t_data.append([row['Name'].upper(), row['TOT_P'], row['TOT_M'], row['TOT_F']])
    elif (row['TRU']=='Rural'):
        r_data.append([row['Name'].upper(), row['TOT_P'], row['TOT_M'], row['TOT_F']])
    elif (row['TRU']=='Urban'):
        u_data.append([row['Name'].upper(), row['TOT_P'], row['TOT_M'], row['TOT_F']])

t_df = pd.DataFrame(t_data, columns = ['Name', 'Total', 'Male', 'Female']).set_index('Name')
r_df = pd.DataFrame(r_data, columns = ['Name', 'Total', 'Male', 'Female']).set_index('Name')
u_df = pd.DataFrame(u_data, columns = ['Name', 'Total', 'Male', 'Female']).set_index('Name')

df_18 = pd.read_excel(files_c18[0])[5:]
df_14 = pd.read_excel(files_c14[0])[6:]

df_14[df_14.columns[5]] = pd.to_numeric(df_14[df_14.columns[5]])
df_14[df_14.columns[6]] = pd.to_numeric(df_14[df_14.columns[6]])
df_14[df_14.columns[7]] = pd.to_numeric(df_14[df_14.columns[7]])

data_q3_1 = []
data_q3_2 = []
data_q3_3 = []

state_name = 'INDIA'
count=0
for index, row in df_18.iterrows():
    if(row[4]!='Total'):
        continue
    if(row[2]==state_name):
        count=count+1
    else:
        state_name=row[2]
        count=1
    if(row[3]=='Rural'):
        rural1 = r_df.loc[state_name]['Total'] - row[5]
        rural2 = row[5] - row[8]
        rural3 = row[8]
        rural_total = r_df.loc[state_name]['Total']
    if(row[3]=='Urban'):
        urban1 = u_df.loc[state_name]['Total'] - row[5]
        urban2 = row[5] - row[8]
        urban3 = row[8]
        urban_total = u_df.loc[state_name]['Total']
    if(row[3]=='Total'):
        total1 = t_df.loc[state_name]['Total'] - row[5]
        total2 = row[5] - row[8]
        total3 = row[8]
        total_total = t_df.loc[state_name]['Total']

    if(count==3):
        state_code = row[0]
        urban_p1 = urban1/urban_total*100
        urban_p2 = urban2/urban_total*100
        urban_p3 = urban3/urban_total*100

        rural_p1 = rural1/rural_total*100
        rural_p2 = rural2/rural_total*100
        rural_p3 = rural3/rural_total*100

        p_value = stats.ttest_ind([urban1/rural1, urban2/rural2, urban3/rural3], [urban_total/rural_total, urban_total/rural_total, urban_total/rural_total], equal_var=False).pvalue
        # p_value = stats.ttest_ind([urban_p1/rural_p1, urban_p2/rural_p2, urban_p3/rural_p3], [urban_total/rural_total, urban_total/rural_total, urban_total/rural_total], equal_var=False).pvalue
        data_q3_1.append([state_code, urban_p1, rural_p1, p_value])
        data_q3_2.append([state_code, urban_p2, rural_p2, p_value])
        data_q3_3.append([state_code, urban_p3, rural_p3, p_value])

count=0
dicts_t = {}
dicts_m = {}
dicts_f = {}
list_total = [0] *11
list_male = [0] *11
list_female = [0] *11
transformer = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:7, 9:7, 10:7, 11:8, 12:8, 13:8, 14:8, 15:9, 16:9, 17:9, 18:10}
for index, row in df_14.iterrows():
    list_total[transformer[count]] = list_total[transformer[count]] + row[5]
    list_male[transformer[count]] = list_male[transformer[count]] + row[6]
    list_female[transformer[count]] = list_female[transformer[count]] + row[7]
    count = count + 1
    if(count>18):
        if(row[3]=='India'):
            name = row[3].upper()
        else:
            name = row[3].split('-')[1].split('(')[0].strip()
        dicts_t[name]=list_total
        dicts_m[name]=list_male
        dicts_f[name]=list_female
        list_total = [0] *11
        list_male = [0] *11
        list_female = [0] *11
        count=0

data_q5_1 = []
data_q8_1 = []
data_q8_2 = []
data_q8_3 = []
state_name = 'INDIA'
count=0
max_p=0
max_mr1=0
max_fr1=0
max_mr2=0
max_fr2=0
max_mr3=0
max_fr3=0
max_p_age = ''
max_mr1_age = ''
max_fr1_age = ''
max_mr2_age = ''
max_fr2_age = ''
max_mr3_age = ''
max_fr3_age = ''

for index, row in df_18.iterrows():
    if(row[3]!='Total'):
        continue
    if(row[4]=='Total'):
        continue
    if(row[2]==state_name):
        count=count+1
    else:
        state_name=row[2]
        count=1
        max_p=0
        max_mr1=0
        max_fr1=0
        max_mr2=0
        max_fr2=0
        max_mr3=0
        max_fr3=0

    male_pop = dicts_m[state_name][count+1]
    female_pop = dicts_f[state_name][count+1]
    total_pop = dicts_t[state_name][count+1]
    curr_p = row[8]/total_pop*100
    curr_mr1 = (male_pop - row[6])/male_pop
    curr_fr1 = (female_pop - row[7])/female_pop
    curr_mr2 = (row[6]-row[9])/male_pop
    curr_fr2 = (row[7]-row[10])/female_pop
    curr_mr3 = row[9]/male_pop
    curr_fr3 = row[10]/female_pop

    if(curr_p > max_p):
        max_p = curr_p
        max_p_age = row[4]
    if(curr_mr1 > max_mr1):
        max_mr1 = curr_mr1
        max_mr1_age = row[4]
    if(curr_mr2 > max_mr2):
        max_mr2 = curr_mr2
        max_mr2_age = row[4]
    if(curr_mr3 > max_mr3):
        max_mr3 = curr_mr3
        max_mr3_age = row[4]
    if(curr_fr1 > max_fr1):
        max_fr1 = curr_fr1
        max_fr1_age = row[4]
    if(curr_fr2 > max_fr2):
        max_fr2 = curr_fr2
        max_fr2_age = row[4]
    if(curr_fr3 > max_fr3):
        max_fr3 = curr_fr3
        max_fr3_age = row[4]

    if(count==9):
        state_code = row[0]
        data_q5_1.append([state_code, max_p_age, max_p])
        data_q8_1.append([state_code, max_mr1_age, max_mr1, max_fr1_age, max_fr1])
        data_q8_2.append([state_code, max_mr2_age, max_mr2, max_fr2_age, max_fr2])
        data_q8_3.append([state_code, max_mr3_age, max_mr3, max_fr3_age, max_fr3])

df = pd.DataFrame(data_q3_1, columns = ['state-code', 'urban-percentage', 'rural-percentage', 'p-value'])
df.to_csv(output_folder+'geography-india-a.csv', index=False)

df = pd.DataFrame(data_q3_2, columns = ['state-code', 'urban-percentage', 'rural-percentage', 'p-value'])
df.to_csv(output_folder+'geography-india-b.csv', index=False)

df = pd.DataFrame(data_q3_3, columns = ['state-code', 'urban-percentage', 'rural-percentage', 'p-value'])
df.to_csv(output_folder+'geography-india-c.csv', index=False)

df = pd.DataFrame(data_q5_1, columns = ['state/ut', 'age-group', 'percentage'])
df.to_csv(output_folder+'age-india.csv', index=False)

df = pd.DataFrame(data_q8_1, columns = ['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])
df.to_csv(output_folder+'age-gender-c.csv', index=False)

df = pd.DataFrame(data_q8_2, columns = ['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])
df.to_csv(output_folder+'age-gender-b.csv', index=False)

df = pd.DataFrame(data_q8_3, columns = ['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])
df.to_csv(output_folder+'age-gender-a.csv', index=False)