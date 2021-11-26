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

North = ['JAMMU & KASHMIR', 'LADAKH', 'PUNJAB', 'HARYANA', 'HIMACHAL PRADESH', 'UTTARAKHAND', 'NCT OF DELHI', 'CHANDIGARH']
West = ['RAJASTHAN', 'GUJARAT', 'MAHARASHTRA', 'GOA', 'DADRA & NAGAR HAVELI', 'DAMAN & DIU']
Central = ['MADHYA PRADESH', 'UTTAR PRADESH', 'CHHATTISGARH']
East = ['BIHAR', 'WEST BENGAL', 'ODISHA', 'JHARKHAND']
South = ['KARNATAKA', 'TELANGANA', 'ANDHRA PRADESH', 'TAMIL NADU', 'KERALA', 'LAKSHADWEEP', 'PUDUCHERRY']
North_East = ['ASSAM', 'SIKKIM', 'MEGHALAYA', 'TRIPURA', 'ARUNACHAL PRADESH', 'MANIPUR', 'NAGALAND', 'MIZORAM', 'ANDAMAN & NICOBAR ISLANDS']

data_q7_1 = [['North','','',''],
             ['West','','',''],
             ['Central','','',''],
             ['East','','',''],
             ['South','','',''],
             ['North-East','','','']]
data_q7_2 = [['North','','',''],
             ['West','','',''],
             ['Central','','',''],
             ['East','','',''],
             ['South','','',''],
             ['North-East','','','']]

dicts1 = [{}, {}, {}, {}, {}, {}]
dicts2 = [{}, {}, {}, {}, {}, {}]

for file in files_c17[1:]:
    df = pd.read_excel(file)[5:]

    df[df.columns[4]] = pd.to_numeric(df[df.columns[4]])
    df[df.columns[5]] = pd.to_numeric(df[df.columns[5]])
    df[df.columns[6]] = pd.to_numeric(df[df.columns[6]])

    df[df.columns[9]] = pd.to_numeric(df[df.columns[9]])
    df[df.columns[10]] = pd.to_numeric(df[df.columns[10]])
    df[df.columns[11]] = pd.to_numeric(df[df.columns[11]])

    df[df.columns[14]] = pd.to_numeric(df[df.columns[14]])
    df[df.columns[15]] = pd.to_numeric(df[df.columns[15]])
    df[df.columns[16]] = pd.to_numeric(df[df.columns[16]])

    state_name = df.iloc[5,1]
    for index, row in df.iterrows():
        if(~isnan(row[4])):
            if state_name in North:
                if row[3] in dicts1[0].keys():
                    dicts1[0][row[3]]=dicts1[0][row[3]]+row[4]
                else:
                    dicts1[0][row[3]]=row[4]
                if row[3] in dicts2[0].keys():
                    dicts2[0][row[3]]=dicts2[0][row[3]]+row[4]
                else:
                    dicts2[0][row[3]]=row[4]
            elif state_name in West:
                if row[3] in dicts1[1].keys():
                    dicts1[1][row[3]]=dicts1[1][row[3]]+row[4]
                else:
                    dicts1[1][row[3]]=row[4]
                if row[3] in dicts2[1].keys():
                    dicts2[1][row[3]]=dicts2[1][row[3]]+row[4]
                else:
                    dicts2[1][row[3]]=row[4]
            elif state_name in Central:
                if row[3] in dicts1[2].keys():
                    dicts1[2][row[3]]=dicts1[2][row[3]]+row[4]
                else:
                    dicts1[2][row[3]]=row[4]
                if row[3] in dicts2[2].keys():
                    dicts2[2][row[3]]=dicts2[2][row[3]]+row[4]
                else:
                    dicts2[2][row[3]]=row[4]
            elif state_name in East:
                if row[3] in dicts1[3].keys():
                    dicts1[3][row[3]]=dicts1[3][row[3]]+row[4]
                else:
                    dicts1[3][row[3]]=row[4]
                if row[3] in dicts2[3].keys():
                    dicts2[3][row[3]]=dicts2[3][row[3]]+row[4]
                else:
                    dicts2[3][row[3]]=row[4]
            elif state_name in South:
                if row[3] in dicts1[4].keys():
                    dicts1[4][row[3]]=dicts1[4][row[3]]+row[4]
                else:
                    dicts1[4][row[3]]=row[4]
                if row[3] in dicts2[4].keys():
                    dicts2[4][row[3]]=dicts2[4][row[3]]+row[4]
                else:
                    dicts2[4][row[3]]=row[4]
            elif state_name in North_East:
                if row[3] in dicts1[5].keys():
                    dicts1[5][row[3]]=dicts1[5][row[3]]+row[4]
                else:
                    dicts1[5][row[3]]=row[4]
                if row[3] in dicts2[5].keys():
                    dicts2[5][row[3]]=dicts2[5][row[3]]+row[4]
                else:
                    dicts2[5][row[3]]=row[4]
            else:
                print("Nowhere")
        if(~isnan(row[9])):
            if state_name in North:
                if row[8] in dicts2[0].keys():
                    dicts2[0][row[8]]=dicts2[0][row[8]]+row[9]
                else:
                    dicts2[0][row[8]]=row[9]
            elif state_name in West:
                if row[8] in dicts2[1].keys():
                    dicts2[1][row[8]]=dicts2[1][row[8]]+row[9]
                else:
                    dicts2[1][row[8]]=row[9]
            elif state_name in Central:
                if row[8] in dicts2[2].keys():
                    dicts2[2][row[8]]=dicts2[2][row[8]]+row[9]
                else:
                    dicts2[2][row[8]]=row[9]
            elif state_name in East:
                if row[8] in dicts2[3].keys():
                    dicts2[3][row[8]]=dicts2[3][row[8]]+row[9]
                else:
                    dicts2[3][row[8]]=row[9]
            elif state_name in South:
                if row[8] in dicts2[4].keys():
                    dicts2[4][row[8]]=dicts2[4][row[8]]+row[9]
                else:
                    dicts2[4][row[8]]=row[9]
            elif state_name in North_East:
                if row[8] in dicts2[5].keys():
                    dicts2[5][row[8]]=dicts2[5][row[8]]+row[9]
                else:
                    dicts2[5][row[8]]=row[9]
            else:
                print("Nowhere")
        if(~isnan(row[14])):
            if state_name in North:
                if row[13] in dicts2[0].keys():
                    dicts2[0][row[13]]=dicts2[0][row[13]]+row[14]
                else:
                    dicts2[0][row[13]]=row[14]
            elif state_name in West:
                if row[13] in dicts2[1].keys():
                    dicts2[1][row[13]]=dicts2[1][row[13]]+row[14]
                else:
                    dicts2[1][row[13]]=row[14]
            elif state_name in Central:
                if row[13] in dicts2[2].keys():
                    dicts2[2][row[13]]=dicts2[2][row[13]]+row[14]
                else:
                    dicts2[2][row[13]]=row[14]
            elif state_name in East:
                if row[13] in dicts2[3].keys():
                    dicts2[3][row[13]]=dicts2[3][row[13]]+row[14]
                else:
                    dicts2[3][row[13]]=row[14]
            elif state_name in South:
                if row[13] in dicts2[4].keys():
                    dicts2[4][row[13]]=dicts2[4][row[13]]+row[14]
                else:
                    dicts2[4][row[13]]=row[14]
            elif state_name in North_East:
                if row[13] in dicts2[5].keys():
                    dicts2[5][row[13]]=dicts2[5][row[13]]+row[14]
                else:
                    dicts2[5][row[13]]=row[14]
            else:
                print("Nowhere")

for i in range(len(dicts1)):
    dicts1[i] = {k: v for k, v in dicts1[i].items() if k == k}
    my_dict = sorted(zip(dicts1[i].values(), dicts1[i].keys()), reverse=True)
    data_q7_1[i][1] = my_dict[0][1]
    data_q7_1[i][2] = my_dict[1][1]
    data_q7_1[i][3] = my_dict[2][1]
    
    dicts2[i] = {k: v for k, v in dicts2[i].items() if k == k}
    my_dict = sorted(zip(dicts2[i].values(), dicts2[i].keys()), reverse=True)
    data_q7_2[i][1] = my_dict[0][1]
    data_q7_2[i][2] = my_dict[1][1]
    data_q7_2[i][3] = my_dict[2][1]

df = pd.DataFrame(data_q7_1, columns = ['region', 'language-1', 'language-2', 'language-3'])
df.to_csv(output_folder+'region-india-a.csv', index=False)

df = pd.DataFrame(data_q7_2, columns = ['region', 'language-1', 'language-2', 'language-3'])
df.to_csv(output_folder+'region-india-b.csv', index=False)