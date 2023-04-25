import pandas as pd
import statsmodels.formula.api as smf
import os 
from pathlib import Path
import numpy as np

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

model_definitions = [
        "income ~ C(msa_code) + distance",
        "income ~ C(LEAID) + distance",
        "income ~ C(LEAID) + distance + pub_trans_gt_10pct",
        # built_1980_1989 ommitted 
        "income ~ C(LEAID) + distance + pub_trans_gt_10pct + built_1999_2000 + built_1995_1998 + built_1990_1994 +  built_1970_1979 + built_1960_1969 + built_1950_1959 + built_1940_1949 + built_1939_earlier",
        "income ~ C(LEAID) + distance + np.power(distance, 2) + pub_trans_gt_10pct + built_1999_2000 + built_1995_1998 + built_1990_1994 +  built_1970_1979 + built_1960_1969 + built_1950_1959 + built_1940_1949 + built_1939_earlier",
        "income ~ C(LEAID) + distance + np.power(distance, 2) + np.power(distance, 3) + pub_trans_gt_10pct + built_1999_2000 + built_1995_1998 + built_1990_1994 +  built_1970_1979 + built_1960_1969 + built_1950_1959 + built_1940_1949 + built_1939_earlier",
    ]

def run_regression(eq: str, data: pd.DataFrame, reg_number: int, reg_type: str) -> None: # saves to txt file
    reg = smf.wls(formula=eq, data=data, missing='drop').fit(method='qr')
    with open((dir_path / f'model-{reg_type}-{reg_number}-summary.txt'), 'w') as f:
        f.write(reg.summary().as_text())

def run_models(filename: str) -> None: #calls above
    print(f'Loading file {filename}...')
    data = pd.read_csv(
        dir_path / filename, 
        index_col=False,
        dtype={'msa_code': str, 'LEAID': str, 'pub_trans_gt_10pct': int}
        )
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.dropna(inplace=True)
    print('Data loaded!\n')

    for i, eq in enumerate(model_definitions):
        n = i + 1
        print(f'Running Regression {n}...')
        run_regression(eq, data, n, reg_type)
        print(f'Regression {n} Done!\n')
    print(f'{reg_type} models done!')

for dataset in os.listdir(dirpath / 'data'):
    run_models(dataset)