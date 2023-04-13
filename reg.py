import pandas as pd
import statsmodels.formula.api as smf
import os 
from pathlib import Path

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

def run_regression(eq: str, data: pd.DataFrame, reg_number: int) -> None: # saves to pickle
    reg = smf.ols(formula=eq, data=data).fit()
    reg.save(dir_path / 'models' / f'model{reg_number}.py')

model_definitions = [
    # "income ~ distance + C(LEAID)",
    "income ~ distance + pub_trans_gt_10pct + C(LEAID) ",
    # built_1980_1989 ommitted 
    "income ~ distance + pub_trans_gt_10pct + built_1999_2000 + built_1995_1998 + built_1990_1994 +  built_1970_79 + built_1960_69 + built_1950_59 + built_1940_49 + built_1939_earlier + C(LEAID)",
]

print('Loading Data')
data = pd.read_csv(dir_path / 'msa_tracts_dist.csv', index_col=False)
data.dropna(inplace=True)

for i, eq in enumerate(model_definitions):
    n = i + 1
    print(f'Running Regression {n}...')
    run_regression(eq, data, n)
    print(f'Regression {n} Done!\n')
    input('Press any key to continue')