# urban-economics-project
This started as a final Project for Econ 554: Urban Economics at Duke University. It is an extension of Jan Brucckner and Stuart Rosenthal's 2008 paper ["Gentrification and Neighborhood Housing Cycles: Will America's Future Downtowns Be Rich?"](https://direct.mit.edu/rest/article-abstract/91/4/725/57814/Gentrification-and-Neighborhood-Housing-Cycles?redirectedFrom=fulltext). This paper makes two main contributions: first it uses modern data (2000-2019) to test some of Bruckner and Rosenthal's predictions. Second, it tries some additional measures of city centrality and regression forms.

## Use
This project is released under the MIT License, but if you want to use any portion of it for any scholarly work, I would ask that you cite it as an unpublished paper written by Logan Cooper in 2023. If you have any questions, feel free to reach out to me.

## Setup

### Data Download
Most of the data needed for reproduction is packaged in the `/data` directory. The one exception is the ~8GB tract distance file, which can be downloaded from the NBER [here](https://www.nber.org/research/data/tract-distance-database). Note that the file used is the 50-mile data for 2010.

### Dependencies
The dependencies for this project are saved in `ENV.yml`. You can install them with `conda env create -n econ554 --file ENV.yml`.

## Navigation

- `/data`: This directory contains all of the data for this project.
- `/img`: This directory is for saving images from notebooks. Its contents are gitignored, so it should be empty.
- `/models`: This directory contains the summary printouts of all of the models defined in `reg.py`.
- `census-req.py`: This file has some code to populate `/data` with Census data. All of that data is committed, so there shouldn't be any reason to run it.
- `ENV.yml`: Conda environment definition.
- `LICENSE`: Licensing information.
- `notebook.ipynb`: The main file for this project. This notebook includes data cleaning, data wrangling, model evaluation, and visualization.
- `reg.py`: Python code for running the regressions. Separate from the notebook so modelling could be done in the cloud.
- `secrets.json.template`: If you want to use `census-req.py` you'll need to rename this to `secrets.json` and fill it in with a Census API code.
- `wilson_cbd_req.py`: Python script to get Census Tract FIPS code from latitude-longitude coordinates.