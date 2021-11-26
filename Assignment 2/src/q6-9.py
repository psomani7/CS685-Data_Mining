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

df_19 = pd.read_excel(files_c19[0])[5:]
df_08 = pd.read_excel(files_c08[0])[6:]

for i in range(6,45):
    df_08[df_08.columns[i]] = pd.to_numeric(df_08[df_08.columns[i]])

count=0
dicts_t = {}
dicts_m = {}
dicts_f = {}

for index, row in df_08.iterrows():

    if(row[4]!='Total'):
        continue
    if(row[5]!='All ages'):
        continue
    if(row[3]=='INDIA'):
        name = row[3]
    else:
        name = row[3].split('-')[1].split('(')[0].strip()

    list_total = [row[6], row[9], row[12], row[18], row[21], row[24], row[27]+row[30]+row[33]+row[36], row[39]]
    list_male = [row[7], row[10], row[13], row[19], row[22], row[25], row[28]+row[31]+row[34]+row[37], row[40]]
    list_female = [row[8], row[11], row[14], row[20], row[23], row[26], row[29]+row[32]+row[35]+row[38], row[41]]
        
    dicts_t[name]=list_total
    dicts_m[name]=list_male
    dicts_f[name]=list_female

data_q6_1 = []
data_q9_1 = []
data_q9_2 = []
data_q9_3 = []
state_name = 'INDIA'
count=0
max_p=0
max_mr1=0
max_fr1=0
max_mr2=0
max_fr2=0
max_mr3=0
max_fr3=0
max_p_literacy = ''
max_mr1_literacy = ''
max_fr1_literacy = ''
max_mr2_literacy = ''
max_fr2_literacy = ''
max_mr3_literacy = ''
max_fr3_literacy = ''
for index, row in df_19.iterrows():
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

    male_pop = dicts_m[state_name][count]
    female_pop = dicts_f[state_name][count]
    total_pop = dicts_t[state_name][count]
    curr_p = row[8]/total_pop*100
    curr_mr1 = (male_pop - row[6])/male_pop
    curr_fr1 = (female_pop - row[7])/female_pop
    curr_mr2 = (row[6] - row[9])/male_pop
    curr_fr2 = (row[7] - row[10])/female_pop
    curr_mr3 = row[9]/male_pop
    curr_fr3 = row[10]/female_pop

    if(curr_p > max_p):
        max_p = curr_p
        max_p_literacy = row[4]
    if(curr_mr1 > max_mr1):
        max_mr1 = curr_mr1
        max_mr1_literacy = row[4]
    if(curr_mr2 > max_mr2):
        max_mr2 = curr_mr2
        max_mr2_literacy = row[4]
    if(curr_mr3 > max_mr3):
        max_mr3 = curr_mr3
        max_mr3_literacy = row[4]
    if(curr_fr1 > max_fr1):
        max_fr1 = curr_fr1
        max_fr1_literacy = row[4]
    if(curr_fr2 > max_fr2):
        max_fr2 = curr_fr2
        max_fr2_literacy = row[4]
    if(curr_fr3 > max_fr3):
        max_fr3 = curr_fr3
        max_fr3_literacy = row[4]

    if(count==7):
        state_code = row[0]
        data_q6_1.append([state_code, max_p_literacy, max_p])
        data_q9_1.append([state_code, max_mr1_literacy, max_mr1, max_fr1_literacy, max_fr1])
        data_q9_2.append([state_code, max_mr2_literacy, max_mr2, max_fr2_literacy, max_fr2])
        data_q9_3.append([state_code, max_mr3_literacy, max_mr3, max_fr3_literacy, max_fr3])

df = pd.DataFrame(data_q6_1, columns = ['state/ut', 'literacy-group', 'percentage'])
df.to_csv(output_folder+'literacy-india.csv', index=False)

df = pd.DataFrame(data_q9_1, columns = ['state/ut', 'literacy-group-males', 'ratio-males', 'literacy-group-females', 'ratio-females'])
df.to_csv(output_folder+'literacy-gender-c.csv', index=False)

df = pd.DataFrame(data_q9_2, columns = ['state/ut', 'literacy-group-males', 'ratio-males', 'literacy-group-females', 'ratio-females'])
df.to_csv(output_folder+'literacy-gender-b.csv', index=False)

df = pd.DataFrame(data_q9_3, columns = ['state/ut', 'literacy-group-males', 'ratio-males', 'literacy-group-females', 'ratio-females'])
df.to_csv(output_folder+'literacy-gender-a.csv', index=False)