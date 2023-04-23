import pandas as pd
import statsmodels.formula.api as smf
import os 
from pathlib import Path

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

model_definitions = [
        "income ~ distance + C(msa_code)",
        "income ~ distance + C(LEAID)",
        "income ~ distance + pub_trans_gt_10pct + C(LEAID)",
        # built_1980_1989 ommitted 
        "income ~ distance + pub_trans_gt_10pct + built_1999_2000 + built_1995_1998 + built_1990_1994 +  built_1970_1979 + built_1960_1969 + built_1950_1959 + built_1940_1949 + built_1939_earlier + C(LEAID)",
    ]

def run_regression(eq: str, data: pd.DataFrame, reg_number: int, reg_type: str) -> None: # saves to pickle
    reg = smf.ols(formula=eq, data=data).fit()
    with open((dir_path / f'model-{reg_type}-{reg_number}-summary.txt'), 'w') as f:
        f.write(reg.summary().as_text())

def run_models(reg_type: str) -> None: #calls above
    print(f'Loading Data for {reg_type} Models...')
    data = pd.read_csv(dir_path / f'msa_tracts_dist_{reg_type}.csv', index_col=False)
    data.dropna(inplace=True)
    print('Data loaded!\n')

    for i, eq in enumerate(model_definitions):
        n = i + 1
        print(f'Running Regression {n}...')
        run_regression(eq, data, n)
        print(f'Regression {n} Done!\n')
    print(f'{reg_type} models done!')

run_models('br')
run_models('wilson')