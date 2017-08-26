"""
Exploratory python/pandas code to look for correlations in sleep data.
"""

import pandas as pd
from csv import DictReader

essential_columns = {'Exercise (1-5)', 'Hours that night'}
data_filename = 'local_data/sleepdata_latest.csv'

input_list_of_dicts = []
# Test we can read the CSV ok.
with open(file=data_filename) as csv_file:
    for index, row in enumerate(DictReader(f=csv_file)):
        # print([row[c] for c in row.keys()])
        if all([row[c] for c in essential_columns]):
            if float(row['Missed sleep']) < float(0.5):
                print("Rounding down {} for {}".format(row['Missed sleep'], row['Date']))
                row['Missed sleep'] = 0
            input_list_of_dicts.append(row)

df = pd.read_csv(data_filename, index_col='Date', parse_dates=True, infer_datetime_format=True)
# df = pd.DataFrame(input_list_of_dicts)
# df.set_index('Date')

df.dropna(subset=list(essential_columns), inplace=True)
#print('Missed sleep:-', df['Missed sleep'])

correlation = df.corr()
ms = correlation['Missed sleep']
ms_sorted = ms.sort_values()

for i, j in ms_sorted.iteritems():
    print(i.strip() + ', ' + str(j).strip())
print('----')
print(ms_sorted)

htn = correlation['Hours that night']
htn_sorted = htn.sort_values()
print(htn)


# names = [n for n in dir(df.corr()) if not n.startswith('_')]



