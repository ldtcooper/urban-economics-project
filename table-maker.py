from typing import List, Tuple, Callable, Dict
import re
import os 
from pathlib import Path

summary = List[str]

R2_re = re.compile('Adj. R-squared:[ ]+(0\.\d{3})')
N_re = re.compile('No. Observations:[ ]+(\d{1,6})')
multi_space_re = re.compile('\s{2,}')

distances = {'br': 'BR', 'wilson': 'Wilson'}
subsets = {
    'under_100': 'MSAs Under 100 Tracts',
    'btw_100_500': 'MSAs 100-499 Tracts',
    'btw_500_1000': 'MSAs 500-999 Tracts',
    'larger_1000': 'MSAs 1000 or More Tracts',
    'total': 'All MSAs',
}

def extract_R2(f_lines: summary) -> str:
    r2_cell = [el for el in f_lines if 'Adj. R-squared' in el]
    return R2_re.search(r2_cell[0]).groups()[0]

def extract_N(f_lines: summary) -> str:
    N_cell = [el for el in f_lines if 'No. Observations:' in el]
    return N_re.search(N_cell[0]).groups()[0]

def put_dash_for_zero(count: int) -> str:
    return '-' if count == 0 else str(count)

def extract_fixed_effects_counts(f_lines: summary) -> Tuple[str, str]:
    msa_count = len([el for el in f_lines if el.startswith('C(msa_code)')])
    district_count = len([el for el in f_lines if el.startswith('C(LEAID)')])
    return (put_dash_for_zero(msa_count), put_dash_for_zero(district_count))

def extract_intercept(f_lines: summary) -> str:
    int_cell = [el for el in f_lines if el.startswith('Intercept')][0]
    cell_vals = [float(el) for el in multi_space_re.split(int_cell)[1:-1]]
    return (cell_vals[0], cell_vals[3]) # value + p_val

def handle_p_val(p_val: float) -> str:
    return '$<$0.001' if p_val < 0.001 else f'{p_val:.3f}'
        

def extract_line_builder(name: str) -> Callable:
    def extract_line(f_lines: summary) -> str:
        try:
            int_cell = [el for el in f_lines if el.startswith(name)][0]
            cell_vals = [float(el) for el in multi_space_re.split(int_cell)[1:-1]]
            return f'{cell_vals[0]} ({handle_p_val(cell_vals[3])})' # value + p_val
        except IndexError: # if this fails, then that value wasn't found
            return '-'
        
    return extract_line

extract_intercept = extract_line_builder('Intercept')
extract_distance = extract_line_builder('distance')
extract_distance_sq = extract_line_builder('np.power(distance, 2)')
extract_distance_cu = extract_line_builder('np.power(distance, 3)')
extract_transit = extract_line_builder('pub_trans_gt_10pct')
extract_built_1999_2000 = extract_line_builder('built_1999_2000')
extract_built_1995_1998 = extract_line_builder('built_1995_1998')
extract_built_1990_1994 = extract_line_builder('built_1990_1994')
extract_built_1970_1979 = extract_line_builder('built_1970_1979')
extract_built_1960_1969 = extract_line_builder('built_1960_1969')
extract_built_1950_1959 = extract_line_builder('built_1950_1959')
extract_built_1940_1949 = extract_line_builder('built_1940_1949')
extract_built_1939_earlier = extract_line_builder('built_1939_earlier')

def build_filename(reg_num: int, subset: str, dist: str) -> Path:
    # to work in both notebooks and scripts
    try:
        return Path(os.path.dirname(os.path.realpath(__file__))) / 'models' / f'reg-{reg_num}-{subset}_{dist}.txt'
    except NameError:
        return f'./models/reg-{reg_num}-{subset}_{dist}.txt'

def extract_file_data(reg_num: int, subset: str, dist: str) -> Dict[str, str]:
    with open(build_filename(reg_num, subset, dist)) as f:
        lines = f.readlines()
    r2 = extract_R2(lines)
    N = extract_N(lines)
    fixed_effects_counts = extract_fixed_effects_counts(lines)
    intercept = extract_intercept(lines)
    intercept = extract_intercept(lines)
    distance = extract_distance(lines)
    distance_sq = extract_distance_sq(lines)
    distance_cu = extract_distance_cu(lines)
    transit = extract_transit(lines)
    built_1999_2000 = extract_built_1999_2000(lines)
    built_1995_1998 = extract_built_1995_1998(lines)
    built_1990_1994 = extract_built_1990_1994(lines)
    built_1970_1979 = extract_built_1970_1979(lines)
    built_1960_1969 = extract_built_1960_1969(lines)
    built_1950_1959 = extract_built_1950_1959(lines)
    built_1940_1949 = extract_built_1940_1949(lines)
    built_1939_earlier = extract_built_1939_earlier(lines)

    return {
        'r2': r2, 
        'N': N, 
        'msa_fe': fixed_effects_counts[0], 
        'school_fe': fixed_effects_counts[1], 
        'intercept': intercept, 
        'intercept': intercept, 
        'distance': distance, 
        'distance_sq': distance_sq, 
        'distance_cu': distance_cu, 
        'transit': transit, 
        'built_1999_2000': built_1999_2000, 
        'built_1995_1998': built_1995_1998, 
        'built_1990_1994': built_1990_1994, 
        'built_1970_1979': built_1970_1979, 
        'built_1960_1969': built_1960_1969, 
        'built_1950_1959': built_1950_1959, 
        'built_1940_1949': built_1940_1949, 
        'built_1939_earlier': built_1939_earlier
    }

def get_table_data(dist: str, subset: str) -> Dict[str, str]:
        table_data = {
            'cities': subsets[subset],
            'dist': distances[dist]
        }

        for i in range(6):
            n = i + 1
            table_data[f'reg_{n}'] = extract_file_data(n, subset, dist)
        return table_data

def build_save_path(dist: str, subset: str) -> Path:
    try:
        return Path(os.path.dirname(os.path.realpath(__file__))) / 'assets' / 'tables' / f'tab-{dist}-{subset}.tex'
    except NameError:
        return f'./assets/tables/tab-{dist}-{subset}.tex' 

def build_table(dist: str, subset: str) -> List[str]:
    data = get_table_data(dist, subset)
    c = data['cities']
    d = data['dist']
    table_template = [
        r'\begin{landscape}',
        r'\thispagestyle{empty}',
        r'\newgeometry{left=2in, top=5.5in, bottom=1in}',
        r'\newpage',
        r'\begin{table}[h]\centering',
        r'\caption{\label{tab:table-' + dist + '_' + subset + '} Regression Results: ' + c + ' for ' + d + '-Distance}',
        r'\begin{tabular}{l|llllll}',
        r'\hline',
        r'& \multicolumn{1}{c}{\begin{tabular}[c]{@{}c@{}}Control for \\ Distance\end{tabular}} & \multicolumn{1}{c}{\begin{tabular}[c]{@{}c@{}}Control for \\ Local Amenities\end{tabular}} & \multicolumn{1}{c}{\begin{tabular}[c]{@{}c@{}}Control for \\ Public Transit\end{tabular}} & \multicolumn{1}{c}{\begin{tabular}[c]{@{}c@{}}Control for \\ Dwelling Age\end{tabular}} & \multicolumn{1}{c}{\begin{tabular}[c]{@{}c@{}}Include\\ Distance-Squared\end{tabular}} & \multicolumn{1}{c}{\begin{tabular}[c]{@{}c@{}}Include\\ Distance-Cubed\end{tabular}} \\ \hline',
        r'Distance & ' + data['reg_1']['distance'] + ' & ' + data['reg_2']['distance'] + ' & ' + data['reg_3']['distance'] + ' & ' + data['reg_4']['distance'] + ' & ' + data['reg_5']['distance'] + ' & ' + data['reg_6']['distance'] + r' \\',
        r'Distance-Squared &' + data['reg_1']['distance_sq'] + ' & ' + data['reg_2']['distance_sq'] + ' & ' + data['reg_3']['distance_sq'] + ' & ' + data['reg_4']['distance_sq'] + ' & ' + data['reg_5']['distance_sq'] + ' & ' + data['reg_6']['distance_sq'] + r' \\',
        r'Distance-Cubed &' + data['reg_1']['distance_cu'] + ' & ' + data['reg_2']['distance_cu'] + ' & ' + data['reg_3']['distance_cu'] + ' & ' + data['reg_4']['distance_cu'] + ' & ' + data['reg_5']['distance_cu'] + ' & ' + data['reg_6']['distance_cu'] + r' \\',
        r'Access to Public Transit in 2000 &' + data['reg_1']['transit'] + ' & ' + data['reg_2']['transit'] + ' & ' + data['reg_3']['transit'] + ' & ' + data['reg_4']['transit'] + ' & ' + data['reg_5']['transit'] + ' & ' + data['reg_6']['transit'] + r' \\',
        r'\% Buildings Built 1999-2000 &' + data['reg_1']['built_1999_2000'] + ' & ' + data['reg_2']['built_1999_2000'] + ' & ' + data['reg_3']['built_1999_2000'] + ' & ' + data['reg_4']['built_1999_2000'] + ' & ' + data['reg_5']['built_1999_2000'] + ' & ' + data['reg_6']['built_1999_2000'] + r' \\',
        r'\% Buildings Built 1995-1998 &' + data['reg_1']['built_1995_1998'] + ' & ' + data['reg_2']['built_1995_1998'] + ' & ' + data['reg_3']['built_1995_1998'] + ' & ' + data['reg_4']['built_1995_1998'] + ' & ' + data['reg_5']['built_1995_1998'] + ' & ' + data['reg_6']['built_1995_1998'] + r' \\',
        r'\% Buildings Built 1990-1994 &' + data['reg_1']['built_1990_1994'] + ' & ' + data['reg_2']['built_1990_1994'] + ' & ' + data['reg_3']['built_1990_1994'] + ' & ' + data['reg_4']['built_1990_1994'] + ' & ' + data['reg_5']['built_1990_1994'] + ' & ' + data['reg_6']['built_1990_1994'] + r' \\',
        r'\% Buildings Built 1970-1979 &' + data['reg_1']['built_1970_1979'] + ' & ' + data['reg_2']['built_1970_1979'] + ' & ' + data['reg_3']['built_1970_1979'] + ' & ' + data['reg_4']['built_1970_1979'] + ' & ' + data['reg_5']['built_1970_1979'] + ' & ' + data['reg_6']['built_1970_1979'] + r' \\',
        r'\% Buildings Built 1960-1969 &' + data['reg_1']['built_1960_1969'] + ' & ' + data['reg_2']['built_1960_1969'] + ' & ' + data['reg_3']['built_1960_1969'] + ' & ' + data['reg_4']['built_1960_1969'] + ' & ' + data['reg_5']['built_1960_1969'] + ' & ' + data['reg_6']['built_1960_1969'] + r' \\',
        r'\% Buildings Built 1950-1959 &' + data['reg_1']['built_1950_1959'] + ' & ' + data['reg_2']['built_1950_1959'] + ' & ' + data['reg_3']['built_1950_1959'] + ' & ' + data['reg_4']['built_1950_1959'] + ' & ' + data['reg_5']['built_1950_1959'] + ' & ' + data['reg_6']['built_1950_1959'] + r' \\',
        r'\% Buildings Built 1940-1949 &' + data['reg_1']['built_1940_1949'] + ' & ' + data['reg_2']['built_1940_1949'] + ' & ' + data['reg_3']['built_1940_1949'] + ' & ' + data['reg_4']['built_1940_1949'] + ' & ' + data['reg_5']['built_1940_1949'] + ' & ' + data['reg_6']['built_1940_1949'] + r' \\',
        r'\% Buildings Built 1939 or Earlier &' + data['reg_1']['built_1939_earlier'] + ' & ' + data['reg_2']['built_1939_earlier'] + ' & ' + data['reg_3']['built_1939_earlier'] + ' & ' + data['reg_4']['built_1939_earlier'] + ' & ' + data['reg_5']['built_1939_earlier'] + ' & ' + data['reg_6']['built_1939_earlier'] + r' \\',
        r'Intercept &' + data['reg_1']['intercept'] + ' & ' + data['reg_2']['intercept'] + ' & ' + data['reg_3']['intercept'] + ' & ' + data['reg_4']['intercept'] + ' & ' + data['reg_5']['intercept'] + ' & ' + data['reg_6']['intercept'] + r' \\',
        r'Observations &' + data['reg_1']['N'] + ' & ' + data['reg_2']['N'] + ' & ' + data['reg_3']['N'] + ' & ' + data['reg_4']['N'] + ' & ' + data['reg_5']['N'] + ' & ' + data['reg_6']['N'] + r' \\',
        r'MSA Fixed Effects &' + data['reg_1']['msa_fe'] + ' & ' + data['reg_2']['msa_fe'] + ' & ' + data['reg_3']['msa_fe'] + ' & ' + data['reg_4']['msa_fe'] + ' & ' + data['reg_5']['msa_fe'] + ' & ' + data['reg_6']['msa_fe'] + r' \\',
        r'School District Fixed Effects &' + data['reg_1']['school_fe'] + ' & ' + data['reg_2']['school_fe'] + ' & ' + data['reg_3']['school_fe'] + ' & ' + data['reg_4']['school_fe'] + ' & ' + data['reg_5']['school_fe'] + ' & ' + data['reg_6']['school_fe'] + r' \\',
        r'Adjusted $R^2$ &' + data['reg_1']['r2'] + ' & ' + data['reg_2']['r2'] + ' & ' + data['reg_3']['r2'] + ' & ' + data['reg_4']['r2'] + ' & ' + data['reg_5']['r2'] + ' & ' + data['reg_6']['r2'] + r' \\\hline',
        r'\end{tabular}',
        r'\end{table}',
        r'\newpage',
        r'\end{landscape}',
        r'\restoregeometry'
    ]
    return table_template

for s in subsets.keys():
    for d in distances.keys():
        with open(build_save_path(d, s), 'w') as f:
            f.writelines([f'{el}\n' for el in build_table(d, s)])