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


def enrich_missed_sleep(row):
    max_expected_hours = min(target_sleep, row['Max possible (hrs)'])
    if max_expected_hours == float(0):
        # result is invalid.
        return -1
    useful_missed_sleep = max_expected_hours - min(row['Hours that night'], target_sleep)
    if useful_missed_sleep <= hours_noise_threshold:
        useful_missed_reduced_noise = float(0)
    else:
        useful_missed_reduced_noise = useful_missed_sleep
    return float(10) * useful_missed_reduced_noise / max_expected_hours


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
                csv_row['MSScaled'] = enrich_missed_sleep(csv_row)
                if float(csv_row['Hours that night']) > float(csv_row['Max possible (hrs)']):
                    print("WARNING: Hours {} more than maximum {} for {}".format(csv_row['Hours that night'],
                                                                                 csv_row['Max possible (hrs)'],
                                                                                 csv_row['Date']))
                print("{}, {}, {}".format(csv_row['Max possible (hrs)'], csv_row['Hours that night'],
                                          enrich_missed_sleep(csv_row)))
                input_list_of_dicts.append(csv_row)

    df_from_dict = pd.DataFrame(input_list_of_dicts, dtype=float)
    df_from_dict.set_index('Date')
    print(set(df_from_dict))

    df_from_dict.dropna(subset=list(essential_columns), inplace=True)
    print('MSScaled:-', df_from_dict['MSScaled'])

    correlation = df_from_dict.corr()
    print(list(correlation))
    ms = correlation['MSScaled']
    ms_sorted = ms.sort_values()

    for i, j in ms_sorted.iteritems():
        print(i.strip() + ', ' + str(j).strip())
    print('----')
    print(ms_sorted)

    # recovery = correlation['EMFit total recovery']
    # tr_sorted = recovery.sort_values()
    # for i, j in tr_sorted.items():
    #     print(i.strip() + ', ' + str(j).strip())
    # print('----')

    # htn = correlation['Hours that night']
    # htn_sorted = htn.sort_values()
    # print(htn)
    # names = [n for n in dir(df.corr()) if not n.startswith('_')]


if __name__ == "__main__":
    analyse_sleep()
