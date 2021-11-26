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

data_q1 = []
data_q2_1 = []
data_q2_2 = []
data_q2_3 = []
data_q4_1 = []
data_q4_2 = []
for file in files_c17:
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
    df_sum = df.sum(axis=0, skipna=True, numeric_only=True)

    male1 = df_sum[1] - df_sum[4]
    male2 = df_sum[4] - df_sum[7]
    male3 = df_sum[7]
    male_total = df_sum[1]

    female1 = df_sum[2] - df_sum[5]
    female2 = df_sum[5] - df_sum[8]
    female3 = df_sum[8]
    female_total = df_sum[2]

    total1 = df_sum[0] - df_sum[3]
    total2 = df_sum[3] - df_sum[6]
    total3 = df_sum[6]
    total_total = df_sum[0]

    state_code = df.iloc[5,0]
    state_name = df.iloc[5,1]
    percent_one = total1/total_total*100
    percent_two = total2/total_total*100
    percent_three = total3/total_total*100
    data_q1.append([state_code, percent_one, percent_two, percent_three])

    male_p1 = male1/male_total*100
    male_p2 = male2/male_total*100
    male_p3 = male3/male_total*100
    female_p1 = female1/female_total*100
    female_p2 = female2/female_total*100
    female_p3 = female3/female_total*100
    
    p_value = stats.ttest_ind([male1/female1, male2/female2, male3/female3], [male_total/female_total, male_total/female_total, male_total/female_total],equal_var=False).pvalue
    # p_value = stats.ttest_ind([male_p1/female_p1, male_p2/female_p2, male_p3/female_p3], [male_total/female_total, male_total/female_total, male_total/female_total],equal_var=False).pvalue
    data_q2_1.append([state_code, male_p1, female_p1, p_value])
    data_q2_2.append([state_code, male_p2, female_p2, p_value])
    data_q2_3.append([state_code, male_p3, female_p3, p_value])

    data_q4_1.append([state_code, total3/total2])
    data_q4_2.append([state_code, total2/total1])

data_q4_1 = np.array(data_q4_1)
data_q4_1 = data_q4_1[data_q4_1[:, 1].argsort()]

data_q4_11 = [[data_q4_1[-1][0]],
             [data_q4_1[-2][0]],
             [data_q4_1[-3][0]],
             [data_q4_1[0][0]],
             [data_q4_1[1][0]],
             [data_q4_1[2][0]]]

data_q4_2 = np.array(data_q4_2)
data_q4_2 = data_q4_2[data_q4_2[:, 1].argsort()]

data_q4_21 = [[data_q4_2[-1][0]],
             [data_q4_2[-2][0]],
             [data_q4_2[-3][0]],
             [data_q4_2[0][0]],
             [data_q4_2[1][0]],
             [data_q4_2[2][0]]]

df = pd.DataFrame(data_q1, columns = ['state-code', 'percent-one', 'percent-two', 'percent-three'])
df.to_csv(output_folder+'percent-india.csv', index=False)

df = pd.DataFrame(data_q2_1, columns = ['state-code', 'male-percentage', 'female-percentage', 'p-value'])
df.to_csv(output_folder+'gender-india-a.csv', index=False)

df = pd.DataFrame(data_q2_2, columns = ['state-code', 'male-percentage', 'female-percentage', 'p-value'])
df.to_csv(output_folder+'gender-india-b.csv', index=False)

df = pd.DataFrame(data_q2_3, columns = ['state-code', 'male-percentage', 'female-percentage', 'p-value'])
df.to_csv(output_folder+'gender-india-c.csv', index=False)

df = pd.DataFrame(data_q4_11, columns = ['state-code'])
df.to_csv(output_folder+'3-to-2-ratio.csv', index=False, header=False)

df = pd.DataFrame(data_q4_21, columns = ['state-code'])
df.to_csv(output_folder+'2-to-1-ratio.csv', index=False, header=False)