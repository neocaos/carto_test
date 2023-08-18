# 2.- Python Support Engineer Test

I've built a python solution to load both files or requests into Carto Previous platform

## Prerrequisites

- :snake: `python > 3.8` 

## Installation 

`pip install -r requirements.txt`

> :warning: The use of virtual environments  is strongly recommended in order to avoid conflicts in dependencies. 
>
> You can create it by `python -m venv ./.venv`
> 
> You can activate by using `source .venv/bin/activate` (Linux)
>
> or `source .venv/Scripts/activate` (Windows)

## Running

You should run the python solution including as many arguments you want to be processed. 

Any argument must be a url (http | https) or a local file (relativa or absolute paths are welcomed). 

All arguments will be processed before being cut on the tenth row (included), as a previous step before uploading to Carto.

E.g. 

```bash
python main.py nysd.csv \
    https://opendataexapmle/endpoint/fileexample.geojson```



