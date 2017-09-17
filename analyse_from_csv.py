"""
Exploratory python/pandas code to look for correlations in sleep data.
"""

import pandas as pd
from csv import DictReader

essential_columns = {'Exercise (1-5)', 'Hours that night'}
non_float_columns = {'', 'Date'}
data_filename = 'local_data/sleepdata_latest.csv'
target_sleep = float(8)
hours_noise_threshold = float(0.6)


def missed_sleep_scaled(row):
    useful_max = min(target_sleep, row['Max possible (hrs)'])
    if useful_max == float(0):
        # result is invalid.
        return -1
    max_expected_hours = min(target_sleep, row['Max possible (hrs)'])
    useful_missed_sleep = max_expected_hours - min(row['Hours that night'], target_sleep)
    if useful_missed_sleep <= hours_noise_threshold:
        useful_missed_reduced_noise = float(0)
    else:
        useful_missed_reduced_noise = useful_missed_sleep
    print("useful_missed_reduced_noise:", useful_missed_reduced_noise)
    return float(10) * useful_missed_reduced_noise / useful_max


def try_float(s):
    try:
        return float(s)
    except ValueError:
        return s


def analyse_sleep():
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
                                          missed_sleep_scaled(csv_row)))
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



