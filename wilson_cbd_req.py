import requests
import pandas as pd
from tqdm.auto import tqdm
from typing import Dict
import os 
from pathlib import Path

def get_lat_lon_data() -> pd.DataFrame:
    wilson_cbd = pd.read_excel('./data/wilson_cbd.xlsx')
    wilson_cbd.dropna(inplace=True)
    wilson_cbd = wilson_cbd.iloc[:, [0,-2,-1]]
    wilson_cbd.columns = ['msa_id', 'lat', 'lon']
    wilson_cbd['msa_id'] = wilson_cbd['msa_id'].astype(int).astype(str)
    return wilson_cbd

def make_block_request(lat: float, lon: float) -> str:
    res = requests.get(f'https://geo.fcc.gov/api/census/block/find?latitude={lat}&longitude={lon}&censusYear=2010&format=json').json()
    return res['Block']['FIPS']

def convert_block_to_tract(block_fips: str) -> str:
    return block_fips[:-4]

def list_el_to_output(msa: str, lat: float, lon: float) -> Dict[str, str]:
    block_fips = make_block_request(lat=lat, lon=lon)
    tract_fips = convert_block_to_tract(block_fips)
    return {'msa_id': msa, 'tract_id': tract_fips}

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

ll_data = get_lat_lon_data()
fips_data = [list_el_to_output(msa, lat, lon) for msa, lat, lon in tqdm(list(ll_data.itertuples(index=False, name=None)))]
pd.DataFrame(fips_data).to_csv(dir_path / 'data' / 'wilson_cbd.csv', index=False)