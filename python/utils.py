import os
import pandas
import requests
import validators
from cartoframes.utils import decode_geometry
from shapely.geometry import shape
from pathlib import Path
import geopandas as gpd


def is_arg_file(file):
    try:
        return os.path.exists(file) and os.path.isfile(file)
    except Exception as e:
        pass


def get_file(arg):
    data = requests.get(arg)
    return data.json()


def is_arg_url(arg):
    return validators.url(arg)


# We get the file with pandas, and translate into a GeoDataframe (geopandas) by setting up the Geometry using cartoframe.decode_geometry method
def get_geodataframe_from_file(arg):
    if Path(arg).suffix == ".csv":
        frame = pandas.read_csv(arg)
        geodataframe = gpd.GeoDataFrame(
            frame, geometry=decode_geometry(frame["the_geom"])
        )
        geodataframe.crs = "epsg:4326"
        return geodataframe
    else:
        raise Exception("Other formats distinct from CSV are not supported")


# We get the GeoDataFrame from geojson (dict) obtained from the Request
def get_geodataframe_from_geojson(arg):
    return gpd.GeoDataFrame.from_features(arg["features"])
