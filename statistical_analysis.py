import os

import pandas as pd
import scipy.stats as stats

src =  r'D:\BiGART_results'

files = ['bigart_0_1_2_3_4_patient.csv',
        'bigart_15_16_17_18_19_patient.csv']


d1 = pd.read_csv(os.path.join(src, files[0])).sort_values('patient_ids')

d2 = pd.read_csv(os.path.join(src, files[1])).sort_values('patient_ids')


diff = d1['f1_score'] - d2['f1_score']

s = stats.wilcoxon(
    diff,
    zero_method='wilcox',
    correction=False,
    alternative='two-sided',
    mode='auto'

)

print('Wilcoxon', s)

s2 = stats.mannwhitneyu(
    d1['f1_score'], d2['f1_score'],
    alternative='two-sided',
)
print('mannwhitneyu', s2)
