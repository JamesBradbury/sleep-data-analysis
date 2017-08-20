"""
Exploratory python/pandas code to look for correlations in sleep data.
"""

import pandas as pd
from csv import DictReader

essential_columns = {'Date', 'Exercise (1-5)', 'Hours that night'}
data_filename = 'local_data/sleepdata_20Aug2017.csv'

# Test we can read the CSV ok.
with open(file=data_filename) as csv_file:
    for index, row in enumerate(DictReader(f=csv_file)):
        # print([row[c] for c in row.keys()])
        if all([row[c] for c in essential_columns]):
            print(index, row)

df = pd.read_csv(data_filename, index_col='Date', parse_dates=True)
# df['H-L'] = df.High - df.Low

print(df.describe())
print(df.corr())
