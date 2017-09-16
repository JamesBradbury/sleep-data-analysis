"""
Exploratory python/pandas code to look for correlations in sleep data.
"""

import pandas as pd
from csv import DictReader

essential_columns = {'Exercise (1-5)', 'Hours that night'}
non_float_columns = {'', 'Date'}
data_filename = 'local_data/sleepdata_latest.csv'


def jb_score(row):
    target = float(7.5)
    max_hours_beyond_target = float(row['Max possible (hrs)']) - target
    # row['Hours that night'] - row['Missed sleep']
    missed_sleep_under_target = max(target, float(row['Max possible (hrs)'])) - float(row['Missed sleep'])
    missed_sleep_over_target = float(row['Missed sleep']) - missed_sleep_under_target
    return float(row['Hours that night'] * 3) - (missed_sleep_under_target * 3) - missed_sleep_over_target


def try_float(s):
    try:
        return float(s)
    except ValueError:
        return s


input_list_of_dicts = []
print("Max:, Htn:, JB Score:")
with open(file=data_filename) as csv_file:
    for index, csv_row in enumerate(DictReader(f=csv_file)):
        csv_row = {k: try_float(v) for k, v in csv_row.items()}
        if all([csv_row[c] for c in essential_columns]):
            if float(csv_row['Hours that night']) > float(csv_row['Max possible (hrs)']):
                print("WARNING: Hours {} more than maximum {} for {}".format(csv_row['Hours that night'],
                                                                             csv_row['Max possible (hrs)'],
                                                                             csv_row['Date']))
            print("{}, {}, {}".format(csv_row['Max possible (hrs)'], csv_row['Hours that night'],
                                      jb_score(csv_row)))
            if float(csv_row['Max possible (hrs)']) < float(6):
                continue
            if float(csv_row['Missed sleep']) < float(0.25):
                # print("Rounding down {} for {}".format(row['Missed sleep'], row['Date']))
                csv_row['Missed sleep'] = float(0)
            input_list_of_dicts.append(csv_row)

df_csv = pd.read_csv(data_filename, parse_dates=True, infer_datetime_format=True)
print(set(df_csv.columns.values))
df_from_dict = pd.DataFrame(input_list_of_dicts, dtype=float)
df_from_dict.set_index('Date')
print(set(df_from_dict))

df_from_dict.dropna(subset=list(essential_columns), inplace=True)
print('Missed sleep:-', df_from_dict['Missed sleep'])

correlation = df_from_dict.corr()
print(list(correlation))
ms = correlation['Missed sleep']
ms_sorted = ms.sort_values()

for i, j in ms_sorted.iteritems():
    print(i.strip() + ', ' + str(j).strip())
print('----')
print(ms_sorted)

# htn = correlation['Hours that night']
# htn_sorted = htn.sort_values()
# print(htn)
# names = [n for n in dir(df.corr()) if not n.startswith('_')]



