
import sys

#https://data.cityofnewyork.us/resource/bntt-wmh5.json
import os
from pathlib import Path

import geopandas as gpd
import pandas

import requests
import validators

from cartoframes.auth import Credentials
from cartoframes.auth import set_default_credentials
from cartoframes import to_carto
from cartoframes.utils import decode_geometry
from shapely.geometry import shape

set_default_credentials('creds.json')


def is_arg_file(file):
    try:
        return os.path.exists(file) and os.path.isfile(file)    
    except Exception as e:
        pass
    

def get_file(arg):
    #https://www.bilbao.eus/aytoonline/srvDatasetCamaras?formato=geojson
    data = requests.get(arg)
    return data.json()
    

def is_arg_url(arg):
    return validators.url(arg)
    
    

def split_and_load(arg, is_file=True, row_limit=10):
    if is_file and Path(arg).suffix == '.csv':
        frame = pandas.read_csv(arg,nrows=10)
        # geodataframe.crs = 'epsg:4326'
        geodataframe = gpd.GeoDataFrame(frame,geometry=decode_geometry(frame['the_geom']))
        geodataframe.crs = 'epsg:4326'
        geodataframe = geodataframe.head(10)
    
    if not is_file:
        geodataframe = gpd.GeoDataFrame.from_features(arg['features']).head(10)
        
        
        
    # partial = geodataframe.head(row_limit)
    
    return geodataframe
    

def main(args):
    print("Running ETL pipeline to Ingest Spatial Data")
    print('Number of arguments:', len(args), 'arguments.')
    for index,arg in enumerate(args):
        print("argument: " + str(arg) + " with index :" + str(index))
        
        is_file = is_arg_file(arg)
        is_url = is_arg_url(arg)
        
        if not is_file and not is_url:        
            raise Exception("Argument must be a local file or a url")
        
        if is_file:
            file = arg
        else: # It's a endpoint or request
            file = get_file(arg)
        
        
        geodataframe = split_and_load(file,is_file)
        
        to_carto(geodataframe, 'test2', if_exists='replace')
        
    


if __name__ == "__main__":
    main(sys.argv[1:])