import json
from census import Census 
import us
from typing import Tuple

def load_api_key() -> str:
    with open('./secrets.json', 'r') as f:
        secrets = json.load(f)

    return secrets['API_KEY']

def get_tract_data(c: Census, tract_vars: Tuple[str], year: int) -> None:
    tract_data = []

    for state in us.STATES:
        tract_data += c.acs5.state_county_tract(tract_vars, state_fips=state.fips, county_fips=Census.ALL, tract=Census.ALL, year=year)
    
    with open(f'./data/tract_data_{year}.json', 'w') as f:
        json.dump(tract_data, f)

API_KEY = load_api_key()

# Define the variables to retrieve
# get these here: https://api.census.gov/data/2019/acs/acs5/variables.html
mean_inc = "B19019_001E"
num_public_transit = "B08301_010E"
population = "B01003_001E"
# building_const = [f'B25034_{"00" if i < 10 else "0"}{i}E' for i in range(2, 12)]

msa_vars = (mean_inc)
tract_vars_2019 = (mean_inc, population)
# tract_vars_2000 = (name, num_public_transit)

c = Census(API_KEY)

# handle MSA-level data
msa_data = c.acs5.get(msa_vars, geo={"for": "metropolitan statistical area/micropolitan statistical area:*"}, year=2019)

with open('./data/msa_data.json', 'w') as f:
    json.dump(msa_data, f)

get_tract_data(c, tract_vars_2019, 2019)
# get_tract_data(c, tract_vars_2000, 2000)

